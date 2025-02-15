import asyncio
from datetime import datetime
import json
from typing import Coroutine
from uuid import uuid4
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiohttp import ClientSession, ClientTimeout
from fastapi import HTTPException

from backend.database.models.models import Purchase
from backend.dto.purchase_dto import PurchaseModel
from backend.dto.uc_code_dto import (
    BuyPointModel,
    BuyUCCodeCallbackModel, 
    BuyUCCodeUrlModel,
    UCActivateRequestModel,
    UCActivationError, 
    UCCodeGetBuyUrlModel,
)
from backend.repositories.uc_code_repository import UCCodeRepository
from backend.utils.config.config import BOT_TOKEN, CODEEPAY_API_KEY, PAYMENT_NOTIFICATION_CHAT, UCODEIUM_API_KEY


class PaymentService:
    def __init__(self, repository: UCCodeRepository, bot: Bot):
        self.codeepay_api_url = "https://codeepay.ru/initiate_payment"
        self.ucodeium_api_url = "https://ucodeium.com/api/activate"
        self.codeepay_api_key = CODEEPAY_API_KEY
        self.ucodeium_api_key = UCODEIUM_API_KEY
        self.repository = repository
        self.bot = bot

    async def format_purchase_data(self, purchase: Purchase) -> str:
        us_packs_info = []
        for uc_pack in json.loads(purchase.metadata_)['uc_packs']:
            errors = "\n" + "\n".join([
                "{uc_code} → {message}".format(uc_code=err['uc_code'], message=err['message'])
                for err in uc_pack['errors']
            ]) if uc_pack['errors'] else "Нет ошибок"

            pack_info = (
                f"<b>Сумма</b>: {uc_pack['total_sum']} ₽\n"
                f"<b>Количество UC</b>: {uc_pack['uc_amount']} UC x {uc_pack['quantity']}\n"
                f"<b>Количество активированных кодов</b>: {uc_pack['activated_codes']}\n"
                f"<b>Неуспешные Activation IDs</b>: {uc_pack.get('error_activation_ids')}\n"
                f"<b>Ошибки активации (Код → Ошибка)</b>: {errors}"
            ).strip()

            us_packs_info.append(pack_info)

        message_text = (
            f"<b>Заказ</b>: {purchase.payment_id}\n"
            f"<b>Игрок</b>: {purchase.player_id}\n"
            f"<b>Сумма UC</b>: {purchase.uc_sum} ₽\n"
            f"<b>Сумма заказа</b>: {purchase.price} ₽\n"
            f"<b>Метод оплаты</b>: {purchase.payment_method}\n"
            f"<b>Статус</b>: {purchase.status}\n\n"
            f"<b>Информация по UC-пакетам:</b>\n\n" + "\n\n".join(us_packs_info)
        ).strip()

        return message_text
    
    async def limited_post_request(
        self, 
        form: UCActivateRequestModel, 
        uc_amount: int,
        price: float,
        semaphore: asyncio.Semaphore
    ) -> dict[str, str]:
        async with semaphore:
            return await self._post_request(form, uc_amount, price)

    async def _post_request(
        self, 
        form: UCActivateRequestModel, 
        uc_amount: int,
        price: float,
    ) -> dict[str, str]:
        async with ClientSession(timeout=ClientTimeout(total=600)) as session:
            async with session.post(
                "test",
                headers={"X-Api-Key": self.ucodeium_api_key},
                json=form.model_dump(),
                ssl=False,
            ) as response:
                json_res = await response.json()
                if json_res.get("result_code") == 0:
                    return json_res
                return UCActivationError(
                    status_code=json_res.get("result_code"),
                    uc_code=form.uc_code,
                    uc_amount=uc_amount,
                    price=price,
                    message=(await response.json() or {}),
                    player_id=form.player_id
                )
            
    async def send_payment_notification(self, purchase: PurchaseModel) -> None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Связаться с покупателем",
                    url=f"t.me/{purchase.tg_id}"
                ),
                InlineKeyboardButton(
                    text="Изменить статус",
                    callback_data=f"change_status_from_notification_{purchase.payment_id}"
                )
            ]]
            )
        try:
            await self.bot.send_message(
                chat_id=PAYMENT_NOTIFICATION_CHAT,
                text=await self.format_purchase_data(purchase),
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            await self.bot.send_message(
                chat_id=PAYMENT_NOTIFICATION_CHAT,
                text=await self.format_purchase_data(purchase),
                reply_markup=keyboard,
                parse_mode="HTML"
            )

    async def activate_codes(self, payload: BuyUCCodeCallbackModel) -> None:
        any_error_is_raised = False
        semaphore = asyncio.Semaphore(10)

        for uc_pack in payload.metadata.uc_packs:
            tasks: list[Coroutine] = []
            activated = 0
            error_activation_ids = []

            uc_codes = await self.repository.get_activating_codes(
                uc_pack.uc_amount, 
                uc_pack.quantity
            )
            for uc_code in uc_codes:
                tasks.append(
                    self.limited_post_request(
                        UCActivateRequestModel(
                            uc_value=f"{uc_pack.uc_amount} UC",
                            uc_code=uc_code,
                            player_id=payload.metadata.player_id,
                        ),
                        uc_amount=uc_pack.uc_amount,
                        price=uc_pack.price_per_uc,
                        semaphore=semaphore
                    )
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            errors = []
            error_messages = {
                101: "Код уже активирован этим игроком",
                102: "Код уже активирован другим игроком",
                201: "Неверный формат кода",
                202: "Неверный формат Player ID",
                301: "Техническая проблема на сервере"
            }

            for response in responses:
                if isinstance(response, dict):
                    activated += 1
                elif isinstance(response, Exception):
                    errors.append({"message": f"Ошибка сервера {str(response)}"})
                else:
                    if isinstance(response, UCActivationError):
                        error_activation_ids.append(
                            int((response.message.get("activation_data") or {}).get("activation_id", 0))
                        )
                        errors.append({
                            **response.model_dump(),
                            "message": error_messages[response.status_code],
                        })
                    await self.repository.return_back_uc_code(
                        response.uc_code, 
                        response.uc_amount, 
                        response.price
                    )
            if len(errors) > 0:
                any_error_is_raised = True

            uc_pack.activated_codes = activated
            uc_pack.error_activation_ids = error_activation_ids
            uc_pack.errors = errors

        payload.metadata.response =( 
            {"detail": "Оплата прошла успешно, но возможно не все коды активировались"}
            if any_error_is_raised
            else {"detail": "Оплата прошла успешно"}
        )
        
    async def get_uc_payment_url(self, form: UCCodeGetBuyUrlModel, tg_id: int) -> BuyUCCodeUrlModel:
        internal_order_id = str(uuid4())
        response = await self.get_payment_url(
            payload={
                "method_slug": form.method_slug,
                "amount": form.amount - form.discount,
                "metadata": {
                    "tg_id": tg_id,
                    "player_id": form.player_id,
                    "uc_packs": [uc_pack.model_dump() for uc_pack in form.uc_packs],
                    "notification_url": "https://zeusucbot.shop/api/uc_code/buy/callback",
                    "internal_order_id": internal_order_id
                }
            }
        )
        return BuyUCCodeUrlModel(**response, internal_id=internal_order_id)
            
    async def get_payment_url(self, payload: UCCodeGetBuyUrlModel) -> dict[str, str]:
        async with ClientSession() as session:
            async with session.post(
                self.codeepay_api_url,
                headers={"X-Api-Key": self.codeepay_api_key},
                json=payload,
                ssl=False
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=(await response.json())["detail"],
                    )
                return await response.json()
            
    async def activate_code_without_callback(self, uc_amount: int, player_id: int) -> None:
        uc_code = await self.repository.get_activating_code(uc_amount)
        await self._post_request(
            UCActivateRequestModel(
                uc_value=f"{uc_amount} UC",
                uc_code=uc_code.code,
                player_id=player_id
            ),
            uc_amount=uc_amount,
            price=uc_code.price_per_uc.price
        )

    async def get_point_payment_url(self, form: BuyPointModel, tg_id: int) -> str:
        internal_order_id = str(uuid4())
        response = await self.get_payment_url(
            payload={
                "method_slug": form.method_slug,
                "amount": form.amount,
                "metadata": {
                    "tg_id": tg_id,
                    "point": form.point,
                    "notification_url": "https://zeusucbot.shop/api/user/buy/point/callback",
                    "internal_order_id": internal_order_id
                }
            }
        )
        return response["url"]
    
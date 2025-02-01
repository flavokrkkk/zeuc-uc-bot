import asyncio
from typing import Coroutine
from uuid import uuid4
from aiohttp import ClientSession, payload
from fastapi import HTTPException

from backend.dto.purchase_dto import PurchaseModel
from backend.dto.uc_code_dto import (
    BuyPointCallbackModel,
    BuyPointModel,
    BuyUCCodeCallbackModel, 
    BuyUCCodeUrlModel,
    UCActivateRequestModel, 
    UCActivationResult, 
    UCCodeGetBuyUrlModel, 
    UCPackModel
)
from backend.repositories.uc_code_repository import UCCodeRepository
from backend.utils.config.config import CODEEPAY_API_KEY


class PaymentService:
    def __init__(self, repository: UCCodeRepository):
        self.codeepay_api_url = "https://codeepay.ru/initiate_payment"
        self.ucodeium_api_url = "https://ucodeium.com/api/activate"
        self.codeepay_api_key = CODEEPAY_API_KEY
        self.ucodeium_api_key = "e158c8cb-e6cc-4cb7-b5fb-777abe0c2957"
        self.repository = repository

    async def _post_request(
        self, 
        form: UCActivateRequestModel, 
        uc_amount: int,
        price: float
    ) -> UCActivationResult:
        async with ClientSession() as session:
            async with session.post(
                self.ucodeium_api_url,
                headers={"X-Api-Key": self.ucodeium_api_key},
                json=form.model_dump(),
                ssl=False,
            ) as response:
                print(response.status)
                if response.status == 200:
                    api_response = await response.json()
                    return UCActivationResult(success=1, response=api_response)
                await self.repository.return_back_uc_code(form.uc_code, uc_amount, price)
                raise HTTPException(
                    status_code=response.status,
                    detail=await response.json(),
                )

    async def activate_codes(self, payload: BuyUCCodeCallbackModel) -> list[str]:
        for uc_pack in payload.metadata.uc_packs:
            tasks: list[Coroutine] = []
            activated = 0
            uc_codes = await self.repository.get_activating_codes(
                uc_pack.uc_amount, 
                uc_pack.quantity
            )
            for uc_code in uc_codes:
                tasks.append(
                    self._post_request(
                        UCActivateRequestModel(
                            uc_value=f"{uc_pack.uc_amount} UC",
                            uc_code=uc_code,
                            player_id=payload.metadata.player_id
                        ),
                        uc_amount=uc_pack.uc_amount,
                        price=uc_pack.price_per_uc
                    )
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for response in responses:
                if isinstance(response, UCActivationResult):
                    activated += 1
            uc_pack.activated_codes = activated
            activated = 0
        return payload
        
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
            
    async def get_payment_url(self, payload: UCCodeGetBuyUrlModel) -> dict:
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
        uc_code = (await self.repository.get_activating_codes(uc_amount, 1))[0]
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
                    "notification_url": "https://zeusucbot.shop/api/users/buy/point/callback",
                    "internal_order_id": internal_order_id
                }
            }
        )
        return response["url"]
    
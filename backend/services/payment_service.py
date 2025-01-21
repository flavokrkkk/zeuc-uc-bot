import asyncio
from uuid import uuid4
from aiohttp import ClientSession
from fastapi import HTTPException

from backend.dto.purchase_dto import PurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeCallbackModel, BuyUCCodeUrlModel, UCActivationResult, UCCodeGetBuyUrlModel


class PaymentService:
    def __init__(self):
        self.codeepay_api_url = "https://codeepay.ru/initiate_payment"
        self.ucodeium_api_url = "https://ucodeium.com/api/activate"
        self.codeepay_api_key = "e158c8cb-e6cc-4cb7-b5fb-777abe0c2957"

    async def _post_request(self, **kwargs) -> UCActivationResult:
        headers: dict[str, str] = {"X-Api-Key": self.ucodeium_api_key}
        async with ClientSession() as session:
            async with session.post(
                self.ucodeium_api_url,
                headers=headers,
                json=kwargs,
                ssl=False,
            ) as response:
                if response.status == 200:
                    api_response = await response.json()
                    return UCActivationResult(success=1, response=api_response)
                raise HTTPException(
                    status_code=response.status,
                    detail=await response.json(),
                )

    async def activate_codes(self, payload: BuyUCCodeCallbackModel) -> PurchaseModel:
        await asyncio.gather(
            *[
               await self._post_request(
                    uc_value=f"{uc_pack.ucinitial} UC",
                    uc_code=uc_pack.code,
                    player_id=payload.metadata.player_id
                )
                for uc_pack in payload.metadata.uc_packs
                for _ in range(uc_pack.count) 
            ],
            return_exceptions=True
        )       

    async def get_payment_url(self, form: UCCodeGetBuyUrlModel, tg_id: int) -> BuyUCCodeUrlModel:
        headers: dict[str, str] = {"X-Api-Key": self.codeepay_api_key}
        internal_order_id = str(uuid4())
        async with ClientSession() as session:
            async with session.post(
                self.codeepay_api_url,
                headers=headers,
                json={
                    "method_slug": form.method_slug,
                    "amount": form.amount,
                    "metadata": {
                        "tg_id": tg_id,
                        "player_id": form.player_id,
                        "uc_packs": [uc_pack.model_dump() for uc_pack in form.uc_packs],
                        "notification_url": "http://localhost:8000/api/uc_code/activate",
                        "internal_order_id": internal_order_id
                    }
                },
                ssl=False
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=(await response.json())["detail"],
                    )
                return BuyUCCodeUrlModel(**(await response.json()), internal_id=internal_order_id)
            
    # async def activate_code_without_callback(self, uc_pack) -> None:
    #     await asyncio.gather(
    #         *[
    #            await self._post_request(
    #                 uc_value=f"{uc_pack.ucinitial} UC",
    #                 uc_code=uc_pack.code,
    #                 player_id=player_id
    #             )
    #             for uc_pack in metadata.uc_packs
    #             for _ in range(uc_pack.count) 
    #         ],
    #         return_exceptions=True
    #     )
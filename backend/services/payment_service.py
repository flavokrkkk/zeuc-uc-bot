from aiohttp import ClientSession
from fastapi import HTTPException

from backend.dto.purchase_dto import PurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeCallbackModel, BuyUCCodeUrlModel, UCActivationResult, UCCodeGetBuyUrlModel


class PaymentService:
    def __init__(self):
        self.codeepay_api_url = "https://codeepay.ru/initiate_payment"
        self.ucodeium_api_url = "https://ucodeium.com/api/activate"

    async def _post_request(self, payload: dict[str, str | int]) -> UCActivationResult:
        
        headers: dict[str, str] = {"X-Api-Key": self.ucodeium_api_url}
        async with ClientSession() as session:
            async with session.post(
                self.ucodeium_api_url,
                headers=headers,
                json=payload,
                ssl=False,
            ) as response:
                if response.status == 200:
                    api_response = await response.json()
                    return UCActivationResult(success=1, response=api_response)
                raise HTTPException(status_code=response.status, detail="Something went wrong")

    async def activate_code(self, payload: BuyUCCodeCallbackModel) -> PurchaseModel:
        result = await self._post_request(payload.model_dump())
        return result.model_dump()

    async def get_payment_url(self, form: UCCodeGetBuyUrlModel, tg_id: int) -> BuyUCCodeUrlModel:
        async with ClientSession() as session:
            async with session.post(
                self.codeepay_api_url,
                json={
                    "method_slug": form.method_slug,
                    "amount": form.amount,
                    "metadata": {
                        "tg_id": tg_id,
                        "player_id": form.player_id,
                        "uc_packs": [uc_pack.model_dump() for uc_pack in form.uc_packs],
                        "notification_url": "http://localhost:8000/api/uc_code/activate"
                    }
                },
                ssl=False
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=(await response.json())["detail"],
                    )
                return BuyUCCodeUrlModel(**(await response.json()))
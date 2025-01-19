from aiohttp import ClientSession


class PaymentService:
    def __init__(self):
        self.api_url = "https://codeepay.ru/initiate_payment"

    async def get_payment_url(self, payment_id: str, payment_method: str) -> str:
        async with ClientSession() as session:
            async with session.post(
                self.api_url,
                json={
                    "method_slug": payment_method,
                    "amount": 0,
                    # "email": "string",
                    # "description": "",
                    "metadata": {
                        "notification_url": "http://localhost:8000/api/uc_code/buy",
                    }
                }
            ) as response:
                return response.url
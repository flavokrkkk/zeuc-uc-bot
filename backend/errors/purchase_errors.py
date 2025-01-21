from fastapi import HTTPException


class PurchaseNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Покупка не найдена",
        )
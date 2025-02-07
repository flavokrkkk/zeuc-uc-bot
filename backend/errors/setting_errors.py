from fastapi import HTTPException
from starlette import status


class StoreIsOffError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_423_LOCKED, 
            detail="В данный момент магазин закрыт"
        )
from fastapi import HTTPException


class ActivationNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Активация не найдена",
        )
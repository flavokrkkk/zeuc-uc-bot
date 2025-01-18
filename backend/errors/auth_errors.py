from fastapi import HTTPException
from starlette import status


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
        )


class UserAlreadyNotRegister(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с такими данными не найден!",
        )

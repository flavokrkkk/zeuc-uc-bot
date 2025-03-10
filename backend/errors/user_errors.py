from fastapi import HTTPException
from starlette import status


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )


class UserFriendNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У пользователя нет такого друга",
        )


class UserAlreadyHaveThisFriend(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже находится в друзьях",
        )


class UserAlreadyreadMessage(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже прочитал сообщение",
        )


class UserReferalCodeNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Реферальный код не найден",
        )


class UserAlreadyActivateReferal(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь уже активировал реферальный код",
        )


class UserDiscountNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Скидка не найдена",
        )


class UserNotHaveEnoughBonuses(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="У пользователя недостаточно бонусов",
        )

class UserInBlackList(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail="Пользователь в черном списке",
        )
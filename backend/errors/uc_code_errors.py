from fastapi import HTTPException


class UCCodeAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="UC код уже существует",
        )


class UCCodeNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="UC код не найден"
        )

class UCPackNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="UC пак не найден"
        )


class InvalidUcPackData(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Неверные данные пака"
        )
from fastapi import HTTPException


class RewardCantBeTaken(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Невозможно забрать награду")
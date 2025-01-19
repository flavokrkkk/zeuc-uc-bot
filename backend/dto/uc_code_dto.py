from pydantic import BaseModel


class UCCodePrice(BaseModel):
    price: float
    point: int


class CreateUCCodeModel(BaseModel):
    code: str
    ucinitial: int
    price_per_uc: int


class UCCodeModel(BaseModel):
    code: str
    ucinitial: int
    price_per_uc: UCCodePrice
    total_sum: int = 0
    multiplication_uc: int = 0
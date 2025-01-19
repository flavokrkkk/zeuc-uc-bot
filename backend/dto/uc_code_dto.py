from pydantic import BaseModel


class CreateUCCodeModel(BaseModel):
    code: str
    ucinitial: int
    price_per_uc: int


class UCCodeModel(BaseModel):
    code: str
    ucinitial: int    
    price_per_uc: int
    total_sum: int = 0
    multiplication_uc: int = 0
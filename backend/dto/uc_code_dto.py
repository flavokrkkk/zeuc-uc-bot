from pydantic import BaseModel


class CreateUCCodeModel(BaseModel):
    code: str
    value: int

class UCCodeModel(BaseModel):
    code: str
    value: int    

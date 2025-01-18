from pydantic import BaseModel, field_validator


class UserModel(BaseModel):
    username: str
    tg_id: int
    is_admin: bool

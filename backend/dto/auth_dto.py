from pydantic import BaseModel


class LoginUserModel(BaseModel):
    tg_id: int
    username: str | None = None
from datetime import datetime
from fastapi import UploadFile
from pydantic import BaseModel, field_validator


class BaseUserModel(BaseModel):
    pass

class UpdateUserModel(BaseModel):
    pass
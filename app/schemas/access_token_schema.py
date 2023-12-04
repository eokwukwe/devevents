from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.user_schema import UserBase


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateAccessToken(BaseModel):
    token: str
    user_id: int
    expires_at: datetime


class AccessTokenOut(BaseModel):
    id: str
    user_id: int
    token: str
    user: UserBase
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

from typing_extensions import Annotated


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserOut(UserBase):
    password: SecretStr = Field(min_length=8, exclude=True)
    bio: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class UserPasswordUpdate(BaseModel):
    password: str
    new_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# class Vote(BaseModel):
#     post_id: int
#     dir: Annotated[int, Field(ge=0, le=1)]

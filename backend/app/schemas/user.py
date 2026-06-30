from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    code: str = Field(..., min_length=6, max_length=6)


class UserLoginPassword(UserBase):
    password: str


class UserLoginCode(UserBase):
    code: str = Field(..., min_length=6, max_length=6)


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    user: UserResponse


class SendCodeRequest(BaseModel):
    email: EmailStr

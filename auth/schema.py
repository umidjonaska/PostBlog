from datetime import datetime
from typing import Union, Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class Refresh(BaseModel):
    token: str


class TokenData(BaseModel):
    gmail: str = None


class User(BaseModel):
    gmail: str
    telefon: str = None
    ism: str = None

class UserResponse(BaseModel):
    id: str
    gmail: str
    ism: str = None
    telefon: str = None
    role: str
    telegram_id: int
    rasm: str = None


class TokenResponse(BaseModel):
    user: UserResponse
    role: str
    token_type: str
    access_token: str
    refresh_token: str


class ImmResponse(BaseModel):
    gmail: str

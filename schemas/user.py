from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserCreate(BaseModel):

    username: str
    email: EmailStr
    role: UserRole
    password_hash: str
    

class UserResponse(UserCreate):
    id: int
    updated_at: datetime
    created_at: datetime
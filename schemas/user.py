from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = 'admin'

class UserCreate(BaseModel):

    username: str
    email: EmailStr
    role: UserRole.admin
    password : str
    

class UserResponse(UserCreate):
    id: int
    updated_at: datetime
    created_at: datetime
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):

    username: str
    email: EmailStr
    password : str
    

class UserResponse(UserCreate):
    id: int
    updated_at: datetime
    created_at: datetime
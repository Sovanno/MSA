from pydantic import BaseModel, EmailStr
from typing import Optional


# Users
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str] = ""
    image: Optional[str] = ""
    token: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None
    password: Optional[str] = None

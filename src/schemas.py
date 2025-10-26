from pydantic import BaseModel, EmailStr, Field, constr
from typing import List, Optional


# Users
class UserCreate(BaseModel):
    email: EmailStr
    username: str
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


# Articles
class ArticleCreate(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = ""
    body: Optional[str] = ""
    tagList: List[str] = Field(default_factory=list)


class ArticleUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    body: Optional[str] = None


class ArticleResponse(BaseModel):
    slug: str
    title: str
    description: Optional[str]
    body: Optional[str]
    tagList: List[str]
    author: str

    class Config:
        orm_mode = True


# Comments
class CommentCreate(BaseModel):
    body: constr(min_length=1)


class CommentResponse(BaseModel):
    id: int
    body: str
    author: str

    class Config:
        orm_mode = True

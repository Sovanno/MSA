from pydantic import BaseModel, Field, constr
from typing import List, Optional


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


class TokenPayload(BaseModel):
    user_id: int
    username: str
    exp: Optional[int] = None

    class Config:
        from_attributes = True
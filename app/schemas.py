from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# class Post(BaseModel):
#     id: Optional[int] = None
#     title: str
#     content: str
#     is_publish: bool = False


class PostBase(BaseModel):
    title: str
    content: str
    is_publish: bool = False


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    # class config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # class config:
    #     orm_mode = True


class CurrentUser():
    id: int
    email: EmailStr
    created_at: datetime
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

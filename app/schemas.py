from pydantic import BaseModel
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

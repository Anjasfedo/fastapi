from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    is_publish: bool = False
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}


@app.get("/posts")
def get_posts():
    return {"data": "Yer post"}


@app.post("/createposts")
def create_post(post: Post):
    print(post)
    print(post.model_dump())
    return {"new_post": post.model_dump()}

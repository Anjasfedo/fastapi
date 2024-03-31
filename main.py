from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional
from random import randrange

app = FastAPI()

MY_POSTS = []


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    is_publish: bool = False
    rating: Optional[int] = None


def find_post(id):
    for post in MY_POSTS:
        if post["id"] == id:
            return post


def find_index_post(id):
    for index, post in enumerate(MY_POSTS):
        if post["id"] == id:
            return index


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}


@app.get("/posts")
def get_posts():
    return {"data": MY_POSTS}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.model_dump()
    new_post["id"] = randrange(0, 10000)

    MY_POSTS.append(new_post)

    return {"data": new_post}


@app.get("/posts/latest")
def get_post():
    post = MY_POSTS[len(MY_POSTS) - 1]
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"data": post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if not index and index != 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    post_dict = post.model_dump()
    post_dict["id"] = id

    MY_POSTS[index] = post_dict

    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if not index and index != 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    MY_POSTS.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

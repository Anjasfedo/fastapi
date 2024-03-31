from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from .koneksi import engine, connect_db
from . import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    is_publish: bool = False


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(connect_db)):
    return {"status": "succeed"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    post = cursor.fetchone()

    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id, ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.model_dump()

    cursor.execute("""INSERT INTO posts (title, content, is_publish) VALUES (%s, %s, %s) RETURNING *""",
                   (post["title"], post["content"], post["is_publish"]))
    created_post = cursor.fetchone()
    conn.commit()

    return {"data": created_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post = post.model_dump()

    cursor.execute("""UPDATE posts SET title = %s, content = %s, is_publish = %s WHERE id = %s RETURNING *""",
                   (post["title"], post["content"], post["is_publish"], id))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (id, ))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

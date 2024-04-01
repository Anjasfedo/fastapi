from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .koneksi import engine, connect_db
from .schemas import PostCreate
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}


@app.get("/posts")
def get_posts(db: Session = Depends(connect_db)):
    posts = db.query(models.Post).all()

    return {"data": posts}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(connect_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(connect_db)):
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(connect_db)):
    created_post = models.Post(**post.model_dump())

    db.add(created_post)
    db.commit()

    db.refresh(created_post)

    return {"data": created_post}


@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(connect_db)):
    post_query = db.query(models.Post).filter(
        models.Post.id == id).one_or_none()

    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    for attr, value in post.model_dump().items():
        if attr != 'id':  # Skip updating the id column
            setattr(post_query, attr, value)
    db.commit()

    db.refresh(post_query)

    return {"data": post_query}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(connect_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

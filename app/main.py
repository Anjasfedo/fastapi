from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .koneksi import engine, connect_db
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from . import models
from .utils import hash_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(connect_db)):
    posts = db.query(models.Post).all()

    return posts


@app.get("/posts/latest", response_model=PostResponse)
def get_latest_post(db: Session = Depends(connect_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return post


@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(connect_db)):
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(connect_db)):
    created_post = models.Post(**post.model_dump())

    db.add(created_post)
    db.commit()

    db.refresh(created_post)

    return created_post


@app.put("/posts/{id}", response_model=PostResponse)
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

    return post_query


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(connect_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(connect_db)):
    check_user = db.query(models.User).filter(models.User.email == user.email)

    if check_user.first() != None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"user with email {user.email} already exists")
        
    user.password = hash_password(user.password)

    created_user = models.User(**user.model_dump())

    db.add(created_user)
    db.commit()

    db.refresh(created_user)

    return created_user

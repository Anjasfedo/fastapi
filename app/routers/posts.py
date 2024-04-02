from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..koneksi import connect_db
from ..schemas import PostCreate, PostResponse, CurrentUser
from .. import models
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user), limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id) # Return Post with id same as logged users

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.get("/latest", response_model=PostResponse)
def get_latest_post(db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    return post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    created_post = models.Post(user_id=current_user.id, **post.model_dump())

    db.add(created_post)
    db.commit()

    db.refresh(created_post)

    return created_post


@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: PostCreate, db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(
        models.Post.id == id).one_or_none()

    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
        
    if post_query.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform action")

    for attr, value in post.model_dump().items():
        if attr != 'id':  # Skip updating the id column
            setattr(post_query, attr, value)

    db.commit()

    db.refresh(post_query)

    return post_query


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
        
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

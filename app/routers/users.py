from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..koneksi import connect_db
from ..schemas import UserCreate, UserResponse, CurrentUser
from .. import models
from ..utils import hash_password
from ..oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
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


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(connect_db), current_user: CurrentUser = Depends(get_current_user)):
    user = db.query(models.User).get(id)

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")

    return user

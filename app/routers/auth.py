from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..koneksi import connect_db
from ..schemas import UserLogin
from .. import models
from ..utils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_crendentials: UserLogin, db: Session = Depends(connect_db)):
    user = db.query(models.User).filter(models.User.email ==
                                        user_crendentials.email).one_or_none()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    if not verify_password(user_crendentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")

    return {"token": "example_token"}

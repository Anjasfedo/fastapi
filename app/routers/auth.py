from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..koneksi import connect_db
from ..schemas import Token
from .. import models
from ..utils import verify_password
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_crendentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(connect_db)):
    user = db.query(models.User).filter(models.User.email ==
                                        user_crendentials.username).one_or_none()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    if not verify_password(user_crendentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

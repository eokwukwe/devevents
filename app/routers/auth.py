from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.utils import hashing
from app.database import models
from app.database.connection import get_db
from app.schemas.user_schema import UserLogin
from app.schemas.access_token_schema import Token
from app.utils.auth_checker import create_token, get_current_user, delete_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    if not hashing.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")

    token = create_token(user.id, db)

    return {"access_token": token, "token_type": "bearer"}


@router.delete('/logout', status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_current_user)])
def logout(user: models.User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    delete_token(user, db)

    return

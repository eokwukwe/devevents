import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from app.utils import hashing
from app.utils import http_helper
from app.database import models
from app.schemas import user_schema, event_schema
from app.database.connection import get_db
from app.utils.auth_checker import get_current_user, delete_token


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependency for getting a user resource
fetch_user = http_helper.get_resource(models.User)
# Dependency for checking if a user email exists
check_email_exists = http_helper.check_duplicate(models.User, "email")


@router.get('/events',
            description='Fetch events for logged in user',
            response_model=List[event_schema.EventOnly])
def auth_user_events(user: models.User = Depends(get_current_user)):
    return user.events


@router.post(
    '', status_code=status.HTTP_201_CREATED, response_model=user_schema.UserOut
)
async def create_user(payload: user_schema.UserCreate,
                      db: Session = Depends(get_db),
                      _=Depends(check_email_exists)):

    new_user = models.User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=hashing.create(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=user_schema.UserOut,
            dependencies=[Depends(get_current_user)])
def get_user(user: models.User = Depends(fetch_user),
             _=Depends(get_current_user)):
    return user


@router.get('', response_model=List[user_schema.UserOut])
def get_users(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    users = db.query(models.User).limit(limit).offset(skip).all()
    return users


@router.put('/{id}', response_model=user_schema.UserOut)
def update_user(payload: user_schema.UserUpdate,
                db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    '''
    If the user is updating their email, check if the new email already exists.
    '''
    if payload.email and payload.email != user.email:
        email_exists = db.query(models.User).filter(
            models.User.email == payload.email).first()

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={'email': "This email already exists"}
            )
        user.email = payload.email

    user.first_name = payload.first_name or user.first_name
    user.last_name = payload.last_name or user.last_name
    user.bio = payload.bio or user.bio
    user.updated_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user


@router.put('/{id}/password')
def update_password(payload: user_schema.UserPasswordUpdate,
                    db: Session = Depends(get_db),
                    user: models.User = Depends(get_current_user)):

    if not hashing.verify(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'password': "Incorrect old password"}
        )

    user.password = hashing.create(payload.new_password)

    db.commit()

    return {"message": "Password update successful"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    delete_token(user, db)
    db.delete(user)
    db.commit()
    return


@router.get('/{id}/events', response_model=event_schema.UserEvents)
def get_user_events(user: models.User = Depends(fetch_user),
                    _=Depends(get_current_user)):
    return user

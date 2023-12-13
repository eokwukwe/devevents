from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, HTTPException, Security, status
from itsdangerous import BadSignature, URLSafeTimedSerializer

from app.database import models
from app.schemas import user_schema
from app.utils.config import settings
from app.database.connection import get_db

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def http_401_response(detail: str):
    return {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": detail,
        "headers": {"WWW-Authenticate": "Bearer"}
    }


def token_serializer(secret: str, salt: str = 'authtoken'):
    return URLSafeTimedSerializer(secret, salt=salt)


def create_token(user_id: int, db: Session):
    '''
    Create a token for the user and return it.

    Args:
        user_id (int): The user's id.
        db (Session): The database session.

    Returns:
        str: The token.
    '''
    serializer = token_serializer(settings.secret_key)
    token = serializer.dumps(user_id)
    expires_at = datetime.utcnow() + timedelta(
        seconds=settings.access_token_expire_seconds)

    access_token = models.AccessToken(user_id=user_id,
                                      token=token,
                                      expires_at=expires_at)

    # Add access_token to database and commit
    db.add(access_token)
    db.commit()
    db.refresh(access_token)

    return access_token.token


def delete_token(user: user_schema.UserBase, db: Session):
    db.query(models.AccessToken).filter(
        models.AccessToken.user_id == user.id).delete()
    db.commit()


def validate_token(token: str, db: Session):
    '''
    Validate the token by loading it and checking if it's expired. 
    If it's valid, return the user.

    Args:
        token (str): The token.
        db (Session): The database session.

    Returns:
        User: The user.
    '''
    serializer = token_serializer(settings.secret_key)
    try:
        # 1 week = 604800 seconds
        serializer.loads(token, max_age=settings.access_token_expire_seconds)

        access_token = db.query(models.AccessToken).filter(
            models.AccessToken.token == token).first()

        if not access_token or access_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                **http_401_response('Invalid or expired token'))
    except BadSignature:
        raise HTTPException(**http_401_response('Invalid or expired token'))

    return access_token.user


def check_for_token(bearer_token: str):
    if not bearer_token:
        raise HTTPException(
            **http_401_response("Authorization header not provided"))

    if not bearer_token.startswith("Bearer "):
        raise HTTPException(
            **http_401_response("Invalid authorization header. Must start with Bearer"))

    token = bearer_token.split(" ")[1]

    if not token:
        raise HTTPException(
            **http_401_response("Missing or invalid authentication token"))

    return token

# def check_auth(bearer_token: str = Security(api_key_header)):
#     validate_token(token=check_for_token(bearer_token), db=get_db())
#     pass


def get_current_user(db: Session = Depends(get_db), bearer_token: str = Security(api_key_header)):

    token = check_for_token(bearer_token)
    user = validate_token(token=token, db=db)
    return user

import os
import jwt

from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.exceptions import AuthenticationException
from app.models import get_db, User
from app.repository import user_repository

ACCESS_TOKEN_EXPIRE_MINUTES = 100000
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


token_router = APIRouter(
    prefix="/token",
    tags=["token"],
)


def authenticate_user(db, email: str, password: str):
    user: User = user_repository.get_user_by_email(db, email.lower())

    if not user:
        return False

    if not user.verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@token_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username.lower(), form_data.password)

    if not user:
        raise AuthenticationException(
            "Incorrect username or password",
            {"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

import os
from datetime import datetime

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
import jwt

from app.models import get_db
from app.repository import user_repository
from app.exceptions import AuthenticationException

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_access_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = AuthenticationException(
        "Incorrect username or password",
        {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp: datetime = datetime.fromtimestamp(payload.get("exp"))

        if exp <= datetime.utcnow():
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token expired")
    except Exception:
        raise credentials_exception


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = AuthenticationException(
        "Incorrect username or password",
        {"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"))

        if email is None:
            raise credentials_exception

        if exp <= datetime.utcnow():
            raise AuthenticationException("token expired")
    except Exception:
        raise credentials_exception

    user = user_repository.get_user_by_email(db, email)

    if user is None:
        raise credentials_exception

    return user

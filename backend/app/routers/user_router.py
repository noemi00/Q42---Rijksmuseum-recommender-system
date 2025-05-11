from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.depenencies import get_current_user, verify_access_token
from app.exceptions import (
    ValidationException,
)
from app.models import get_db, User, UserClick, UserRefresh
from app.repository import user_repository, painting_repository


from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    password: str
    email: str


class UserClickSchema(BaseModel):
    painting_id: str
    frontend_click: Optional[bool]
    recommendation_feature: Optional[int]


class UserRefreshSchema(BaseModel):
    painting_id: Optional[str]
    frontpage: bool


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user_create: UserSchema, db: Session = Depends(get_db)):
    try:
        user = User()
        password = user.get_password_hash(user_create.password)
        user.password = password
        user.email = user_create.email.lower()
        created_user = user_repository.save(db, user)
        return created_user
    except IntegrityError:
        raise ValidationException("A user with this e-mail address already exist.")


@user_router.post(
    "/click/",
    status_code=status.HTTP_201_CREATED,
)
async def register_user_click(
    user_create: UserClickSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    painting = painting_repository.get_painting_by_object_number(db, user_create.painting_id)

    if not painting:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Painting not found")

    uc = UserClick()
    uc.painting_id = painting.id
    uc.user_id = user.id
    uc.frontpage_click = user_create.frontend_click
    uc.recommendation_feature = user_create.recommendation_feature
    uc = user_repository.save_user_click(db, uc)
    return uc


@user_router.post(
    "/refresh/",
    status_code=status.HTTP_201_CREATED,
)
async def register_user_refresh(
    user_create: UserRefreshSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    uc = UserRefresh()

    if user_create.painting_id:
        painting = painting_repository.get_painting_by_object_number(db, user_create.painting_id)

        if not painting:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Painting not found")

        uc.painting_id = painting.id

    uc.user_id = user.id
    uc.front_page_refresh = user_create.frontpage
    uc = user_repository.save_user_refresh(db, uc)
    return uc


@user_router.get(
    "/paintings/overview/",
)
async def register_user(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_clicks = user_repository.get_user_clicks(db, user.id)

    if len(user_clicks) == 0:
        return painting_repository.get_random_paintings_for_dashboard(db)

    

    return painting_repository.get_random_paintings_for_dashboard(db)

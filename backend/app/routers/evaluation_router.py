from time import time

from app.models import get_db, User, UserEvaluation, UserEvaluationResults
from app.depenencies import get_current_user
from app.repository import painting_repository, user_repository

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from pydantic import BaseModel


evaluation_router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"],
)


class UserEvaluationClickSchema(BaseModel):
    painting_id: str
    actual_recommendation_feature: int


class UserEvaluationAnswersSchema(BaseModel):
    result: list


@evaluation_router.post(
    "/click/",
    status_code=status.HTTP_201_CREATED,
)
async def register_user_click(
    user_create: UserEvaluationClickSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    painting = painting_repository.get_painting_by_object_number(
        db, user_create.painting_id
    )

    if not painting:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Painting not found")

    uc = UserEvaluation()
    uc.painting_id = painting.id
    uc.recommendation_feature = user_create.actual_recommendation_feature
    uc.user_id = user.id
    uc = user_repository.save_user_evaluation(db, uc)
    return uc


@evaluation_router.post(
    "/answers/",
)
async def register_user_click(
    user_create: UserEvaluationAnswersSchema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for list in user_create.result:
        value = list[1]
        p = painting_repository.get_painting_by_object_number(db, list[0])

        urr = UserEvaluationResults()
        urr.painting_id = p.id
        urr.user_evaluation_id = list[3]
        urr.Score = value
        urr.feature = list[2]
        user_repository.save_user_evaluation_result(db, urr)


@evaluation_router.get(
    "/total/",
)
async def register_user_click(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_eval = user_repository.get_user_evaluations(db, user.id)

    if len(user_eval) > 20:
        return True

    return False
from sqlalchemy.orm import Session

from app.models import User, UserClick, UserRefresh, UserEvaluation, UserEvaluationResults


def save(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_user_click(db: Session, user: UserClick):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_user_refresh(db: Session, user: UserRefresh):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_user_evaluation(db: Session, user: UserEvaluation):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_user_evaluation_result(db: Session, user: UserEvaluationResults):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



def delete(db: Session, user: User):
    db.delete(user)
    db.commit()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def get_user_clicks(db: Session, user_id: int):
    return db.query(UserClick).filter(UserClick.user_id == user_id).all()


def get_user_refresh(db: Session, user_id: int):
    return db.query(UserRefresh).filter(UserRefresh.user_id == user_id).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).one_or_none()


def get_user_evaluation(db: Session, id: int):
    return db.query(UserEvaluation).filter(UserEvaluation.id == id).one_or_none()


def get_user_evaluations(db: Session, id: int):
    return db.query(UserEvaluation).filter(UserEvaluation.user_id == id).all()


def get_user_evaluations_without_answer(db: Session, user_id: int):
    return (
        db.query(UserEvaluation)
        .filter(
            UserEvaluation.user_id == user_id,
            UserEvaluation.recommendation_feature == None,
        )
        .one_or_none()
    )

def get_user_evaluations_without_answer(db: Session, user_id: int):
    return (
        db.query(UserEvaluation)
        .filter(
            UserEvaluation.user_id == user_id,

        )
        .all()
    )


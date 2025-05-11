from sqlalchemy.orm import Session

from app.models import Painting

import random

def save(db: Session, painting: Painting):
    db.add(painting)
    db.commit()
    db.refresh(painting)
    return painting


def delete(db: Session, painting: Painting):
    db.delete(painting)
    db.commit()


def get_painting(db: Session, painting_id: int):
    return db.query(Painting).filter(Painting.id == painting_id).one_or_none()


def get_random_painting(db: Session):
    while True:
        id = random.randrange(0, 4397)
        painting: Painting = get_painting(db, id)

        if not painting:
            continue

        return painting


def get_painting_by_object_number(db: Session, painting_id: int):
    return db.query(Painting).filter(Painting.object_number == painting_id).one_or_none()


def get_all_paintings(db: Session):
    return db.query(Painting).filter(Painting.description == None).all()


def get_random_paintings_for_dashboard(db: Session):
    ids = []

    while True:
        id = random.randrange(0, 4397)
        painting: Painting = get_painting(db, id)

        if not painting:
            continue

        ids.append(painting)

        if len(ids) == 21:
            break

    return ids
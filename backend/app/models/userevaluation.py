from .base import BaseEntity, Base

from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer


class UserEvaluation(Base, BaseEntity):
    """
    User Clicks Tracking model
    """

    __tablename__ = "userevaluations"

    user_id = Column(Integer, ForeignKey("users.id"))
    painting_id = Column(Integer, ForeignKey("paintings.id"))
    recommendation_feature = Column(Integer)

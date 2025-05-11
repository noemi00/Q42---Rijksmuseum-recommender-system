from .base import BaseEntity, Base

from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer


class UserEvaluationResults(Base, BaseEntity):
    """
    User Clicks Tracking model
    """

    __tablename__ = "userevaluationresults"

    user_evaluation_id = Column(Integer, ForeignKey("userevaluations.id"))
    painting_id = Column(Integer, ForeignKey("paintings.id"))
    feature = Column(Integer)
    Score = Column(Integer)

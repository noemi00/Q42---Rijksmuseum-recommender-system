from .base import BaseEntity, Base

from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, Boolean


class UserClick(Base, BaseEntity):
    """
    User Clicks Tracking model
    """

    __tablename__ = "userclicks"

    painting_id = Column(Integer, ForeignKey("paintings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    frontpage_click = Column(Boolean)
    recommendation_feature = Column(Integer)


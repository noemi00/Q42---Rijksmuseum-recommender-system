from .base import BaseEntity, Base

from sqlalchemy import ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer

class UserRefresh(Base, BaseEntity):
    """
    User Clicks Tracking model
    """

    __tablename__ = "userrefresh"

    painting_id = Column(Integer, ForeignKey("paintings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    front_page_refresh = Column(Boolean)

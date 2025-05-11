from .base import BaseEntity, Base

from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Enum

from app.enum import ArtStyles


class Painting(Base, BaseEntity):
    """
    Painting model
    """

    __tablename__ = "paintings"

    object_number = Column(String(256))
    title = Column(String(1024))
    maker = Column(String(256))
    year = Column(String(256))
    url = Column(String(256))

    description = Column(String(4096))
    color = Column(String(16))
    art_style = Column(String(256))

    @property
    def get_art_style(self):
        return ArtStyles(int(self.art_style)).name


from datetime import datetime, timezone

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseEntity:
    """Base model for database models"""

    id = Column(Integer, primary_key=True)
    created: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    modified: datetime = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

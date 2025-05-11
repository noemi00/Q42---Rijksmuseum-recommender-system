import os
from time import time

import jwt
from passlib.hash import bcrypt
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from .base import BaseEntity, Base

SECRET_KEY = os.environ["SECRET_KEY"]


class User(Base, BaseEntity):
    """User database model"""

    __tablename__ = "users"

    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return bcrypt.hash(password)

    def get_password_reset_token(self, expires_in=1800):
        return jwt.encode(
            {"user_id": self.id, "exp": time() + expires_in},
            SECRET_KEY,
            algorithm="HS256",
        )

    def verify_reset_token(token):
        return jwt.decode(token, SECRET_KEY, algorithms="HS256")

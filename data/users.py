# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.db_session import __db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re


class User(__db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    email: Mapped[str] = mapped_column(unique=True)
    hashed_passwd: Mapped[str]

    username: Mapped[str] = mapped_column(unique=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    total_posts: Mapped[int] = mapped_column(default=0)
    total_comments: Mapped[int] = mapped_column(default=0)

    __PASSWD_PATTERN = "^[a-zA-Z0-9!@#$%^&*_+=]{8,16}$"
    __USERNAME_PATTERN = "^[a-zA-Z0-9_]{3,16}$"

    @classmethod
    def validate_password(cls, password: str) -> bool:
        if re.fullmatch(User.__PASSWD_PATTERN, password):
            return True
        return False

    @classmethod
    def validate_username(cls, username: str) -> bool:
        if re.fullmatch(User.__USERNAME_PATTERN, username):
            return True
        return False

    def set_password(self, password: str) -> None:
        self.hashed_passwd = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_passwd, password)



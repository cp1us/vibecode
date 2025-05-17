# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.db_session import __db


class Post(__db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    op_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    op_username: Mapped[int] = mapped_column(ForeignKey("users.username"))
    header: Mapped[str]
    text: Mapped[str] = mapped_column(nullable=True)

    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())

    locked: Mapped[bool] = mapped_column(default=False)

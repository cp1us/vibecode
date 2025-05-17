# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.db_session import __db


class Comment(__db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    op_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    op_username: Mapped[int] = mapped_column(ForeignKey("users.username"))

    text: Mapped[str]

    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())

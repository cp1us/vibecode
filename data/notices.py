import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.db_session import __db


class Notice(__db.Model):
    __tablename__ = "notices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    op_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)

    post_header: Mapped[int] = mapped_column(ForeignKey("posts.header"))
    sender_username: Mapped[int] = mapped_column(ForeignKey("users.username"))

    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.now())

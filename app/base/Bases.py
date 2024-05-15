from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommends: Mapped[int]
    url: Mapped[str] = mapped_column(String(255))
    ip: Mapped[str] = mapped_column(String(255))
    views: Mapped[int]
    date: Mapped[DateTime] = mapped_column(DateTime())
    subject: Mapped[str] = mapped_column(String(255))
    writer: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))

from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommends: Mapped[int]
    url: Mapped[str] = mapped_column(String(255))
    ip: Mapped[str] = mapped_column(String(50))
    views: Mapped[int]
    date: Mapped[DateTime] = mapped_column(DateTime())
    subject: Mapped[str] = mapped_column(String(255))
    writer: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(20))
    crawling_log_id: Mapped[int] = mapped_column(ForeignKey("crawling_log.id"))
    crawling_log: Mapped["CrawlingLog"] = relationship("CrawlingLog", back_populates="posts")


class CrawlingLog(Base):
    __tablename__ = "crawling_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    gallery_id: Mapped[str] = mapped_column(String(100))
    crawled_at: Mapped[DateTime] = mapped_column(DateTime())
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="crawling_log", cascade="all, delete-orphan")

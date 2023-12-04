from typing import List
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from sqlalchemy import DateTime, ForeignKey, Column, Table, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass


event_attendees = Table(
    "event_attendees",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    access_tokens: Mapped[List["AccessToken"]] = relationship(
        "AccessToken", back_populates="user")
    events: Mapped[List["Event"]] = relationship(
        'Event', back_populates="user")
    attending_events: Mapped[List["Event"]] = relationship(
        "Event", secondary=event_attendees, back_populates="attendees"
    )


class AccessToken(Base):
    __tablename__ = "access_tokens"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now() + interval '1 week'"))
    user: Mapped["User"] = relationship("User", back_populates="access_tokens")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    events: Mapped[List["Event"]] = relationship('Event')


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    attendee_total: Mapped[int] = mapped_column(nullable=False)
    cover_image: Mapped[str] = mapped_column(nullable=True)
    venue: Mapped[str] = mapped_column(nullable=False)
    venue_lat: Mapped[float] = mapped_column(nullable=False)
    venue_lng: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="events")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="events")
    attendees: Mapped[List["User"]] = relationship(
        "User", secondary=event_attendees, back_populates="attending_events"
    )

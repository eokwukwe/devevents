from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.schemas import user_schema


class Category(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Event(BaseModel):
    id: int
    title: str
    description: str
    attendee_total: int
    cover_image: Optional[str]
    venue: str
    venue_lat: float
    venue_lng: float
    date: datetime
    created_at: datetime
    updated_at: datetime
    user: user_schema.UserBase
    category: Category
    attendees: list[user_schema.UserBase]

    model_config = ConfigDict(from_attributes=True)


class EventOnly(BaseModel):
    id: int
    title: str
    description: str
    attendee_total: int
    cover_image: Optional[str]
    venue: str
    venue_lat: float
    venue_lng: float
    date: datetime
    created_at: datetime
    category: Category
    attendees: list[user_schema.UserBase]

    model_config = ConfigDict(from_attributes=True)


class CreateEvent(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=1000)
    attendee_total: int = Field(ge=0)
    venue: str = Field(min_length=3, max_length=255)
    venue_lat: float
    venue_lng: float
    date: datetime
    category_id: int


class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    attendee_total: Optional[int] = None
    venue: Optional[str] = None
    venue_lat: Optional[float] = None
    venue_lng: Optional[float] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None


class UserEvents(user_schema.UserBase):
    events: list[EventOnly]

    model_config = ConfigDict(from_attributes=True)

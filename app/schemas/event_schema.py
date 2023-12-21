from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas import user_schema


class Category(BaseModel):
    id: int
    name: str

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


class Event(EventOnly):
    user: user_schema.UserBase

    model_config = ConfigDict(from_attributes=True)


class CreateEvent(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=1000)
    attendee_total: int = Field(ge=0)
    venue: str = Field(min_length=3, max_length=255)
    date: datetime
    category_id: int

    @field_validator('date')
    def date_must_not_be_in_past(cls, v):
        if v < datetime.now():
            raise ValueError('date must not be in the past')
        return v


class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    attendee_total: Optional[int] = None
    venue: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator('date')
    def date_must_not_be_in_past(cls, v):
        if v < datetime.now():
            raise ValueError('date must not be in the past')
        return v


class UserEvents(user_schema.UserBase):
    events: list[EventOnly]

    model_config = ConfigDict(from_attributes=True)

import datetime
import uuid
from pydantic import BaseModel, ConfigDict, Field

from app.utils import tz_now


class UserProfile(BaseModel):
    id: int = Field(description="유저 아이디", examples=[1])
    name: str = Field(description="이름", examples=["홍길동"])
    email: str = Field(description="이메일", examples=["user@email.com"])
    created_at: datetime.datetime = Field(description="생성일시", examples=[tz_now()])
    updated_at: datetime.datetime = Field(description="변경일시", examples=[tz_now()])


class UserInput(BaseModel):
    name: str | None = None
    email: str | None = None


class ContactInput(BaseModel):
    name: str
    organization: str | None = None
    position: str | None = None
    phone: str | None = None
    email: str | None = None
    category: str | None = None  # Enum
    profile_image_url: str | None = None
    content: str | None = None
    is_important: bool = False
    repeat_interval: str | None = None  # Enum
    repeat_base_date: datetime.datetime | None = None


class CalendarInput(BaseModel):
    name: str
    start_dt: datetime.datetime
    end_dt: datetime.datetime | None = None
    is_all_day: bool = False
    remind_interval: int | None = None
    is_important: bool = False
    content: str | None = None
    is_complete: bool = False
    completed_at: datetime.datetime | None = None
    is_repeat: bool = False
    tags: list[str] | None = None
    calendar_recurring_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None


class CalendarRecurringInput(BaseModel):
    start_dt: datetime.datetime
    end_dt: datetime.datetime
    interval: int
    frequency: str


class ContactOutput(BaseModel):
    id: uuid.UUID
    name: str
    organization: str | None = None
    position: str | None = None
    phone: str | None = None
    email: str | None = None
    category: str | None = None  # Enum
    profile_image_url: str | None = None
    content: str | None = None
    is_important: bool = False
    repeat_interval: str | None = None  # Enum
    repeat_base_date: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CalendarOutput(BaseModel):
    id: uuid.UUID
    name: str
    start_dt: datetime.datetime
    end_dt: datetime.datetime | None = None
    is_all_day: bool = False
    remind_interval: int | None = None
    is_important: bool = False
    content: str | None = None
    is_complete: bool = False
    completed_at: datetime.datetime | None = None
    is_repeat: bool = False
    tags: list[str] | None = None
    calendar_recurring_id: uuid.UUID | None = None
    contact_id: uuid.UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class CalendarRecurringOutput(BaseModel):
    id: uuid.UUID
    start_dt: datetime.datetime
    end_dt: datetime.datetime
    interval: int
    frequency: str

    model_config = ConfigDict(from_attributes=True)

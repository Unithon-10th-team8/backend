import datetime
from typing import Any
import uuid
from pydantic import BaseModel, ConfigDict, Field

from app.utils import tz_now


class UserProfile(BaseModel):
    id: int = Field(description="유저 아이디", examples=[1])
    name: str = Field(description="이름", examples=["홍길동"])
    email: str = Field(description="이메일", examples=["user@email.com"])
    profile_image_url: Any = Field(
        description="프로필 이미지 URL",
        examples=["https://www.google.com"],
        default=None,
    )
    created_at: datetime.datetime = Field(description="생성일시", examples=[tz_now()])
    updated_at: datetime.datetime = Field(description="변경일시", examples=[tz_now()])


class UserInput(BaseModel):
    name: str | None = None
    email: str | None = None


class ContactInput(BaseModel):
    name: str = Field(description="연락처 이름", examples=["홍길동"])
    organization: str | None = Field(
        description="소속",
        examples=["00회사"],
        default=None,
    )
    position: str | None = Field(
        description="직급",
        examples=["대리"],
        default=None,
    )
    phone: str | None = Field(
        description="전화번호",
        examples=["01012345678"],
        default=None,
    )
    email: str | None = Field(
        description="이메일",
        examples=["email@gmail.com"],
        default=None,
    )
    category: str = Field(
        description="카테고리",
        examples=["직장", "거래처", "고객", "기타"],
    )
    profile_image_url: str | None = Field(
        description="프로필 이미지 URL",
        examples=["https://www.google.com"],
        default=None,
    )
    content: str | None = Field(
        description="메모",
        examples=["메모내용"],
        default=None,
    )
    is_important: bool = Field(
        description="중요여부",
        examples=[True],
        default=False,
    )
    repeat_interval: str | None = Field(
        description="반복주기(개월)",
        examples=["1", "3", "6", "12"],
        default=None,
    )
    repeat_base_date: datetime.datetime | None = Field(
        description="반복기준일",
        examples=[tz_now()],
        default=None,
    )


class CalendarInput(BaseModel):
    name: str = Field(description="일정 이름", examples=["홍길동"])
    start_dt: datetime.datetime = Field(
        description="일정 시작일시",
        examples=[tz_now()],
    )
    end_dt: datetime.datetime | None = Field(
        description="일정 종료일시",
        examples=[tz_now()],
        default=None,
    )
    is_all_day: bool = Field(
        description="하루종일 여부",
        examples=[True],
        default=False,
    )
    remind_interval: int | None = Field(
        description="리마인드 간격(분)",
        examples=[10, 30, 60],
        default=None,
    )
    is_important: bool = Field(
        description="중요여부",
        examples=[True],
        default=False,
    )
    content: str | None = Field(
        description="메모",
        examples=["메모내용"],
        default=None,
    )
    is_complete: bool = Field(
        description="일정 완료여부",
        examples=[True],
        default=False,
    )
    completed_at: datetime.datetime | None = Field(
        description="일정 완료일시",
        examples=[tz_now()],
        default=None,
    )
    is_repeat: bool = Field(
        description="반복여부",
        examples=[True],
        default=False,
    )
    tags: list[str] | None = Field(
        description="태그 배열",
        examples=[["태그1", "태그2"]],
        default=None,
    )


class CalendarRecurringInput(BaseModel):
    start_dt: datetime.datetime = Field(
        description="반복 시작일시",
        examples=[tz_now()],
    )
    end_dt: datetime.datetime = Field(
        description="반복 종료일시",
        examples=[tz_now()],
    )
    interval: int = Field(
        description="반복 간격(개월)",
        examples=[1, 3, 6, 12],
    )
    frequency: str = Field(
        description="반복 주기",
        examples=["일", "월", "년"],
    )


class ContactOutput(BaseModel):
    id: uuid.UUID = Field(description="연락처 아이디", examples=[uuid.uuid4()])
    name: str = Field(description="연락처 이름", examples=["홍길동"])
    organization: str | None = Field(
        description="소속",
        examples=["00회사"],
        default=None,
    )
    position: str | None = Field(
        description="직급",
        examples=["대리"],
        default=None,
    )
    phone: str | None = Field(
        description="전화번호",
        examples=["01012345678"],
        default=None,
    )
    email: str | None = Field(
        description="이메일",
        examples=["email@gmail.com"],
        default=None,
    )
    category: str | None = Field(
        description="카테고리",
        examples=["직장", "거래처", "고객", "기타"],
        default=None,
    )
    profile_image_url: str | None = Field(
        description="프로필 이미지 URL",
        examples=["https://www.google.com"],
        default=None,
    )
    content: str | None = Field(description="메모", examples=["메모내용"], default=None)
    is_important: bool = Field(
        description="중요여부",
        examples=[True],
        default=False,
    )
    repeat_interval: str | None = Field(
        description="반복주기(개월)",
        examples=["1", "3", "6", "12"],
        default=None,
    )
    repeat_base_date: datetime.datetime | None = Field(
        description="반복기준일",
        examples=[tz_now()],
        default=None,
    )

    model_config = ConfigDict(from_attributes=True)


class CalendarOutput(BaseModel):
    id: uuid.UUID = Field(description="일정 아이디", examples=[uuid.uuid4()])
    name: str = Field(description="일정 이름", examples=["홍길동"])
    start_dt: datetime.datetime = Field(
        description="일정 시작일시",
        examples=[tz_now()],
    )
    end_dt: datetime.datetime | None = Field(
        description="일정 종료일시",
        examples=[tz_now()],
        default=None,
    )
    is_all_day: bool = Field(
        description="하루종일 여부",
        examples=[True],
        default=False,
    )
    remind_interval: int | None = Field(
        description="리마인드 간격(분)",
        examples=[10, 30, 60],
        default=None,
    )
    is_important: bool = Field(
        description="중요여부",
        examples=[True],
        default=False,
    )
    content: str | None = Field(
        description="메모",
        examples=["메모내용"],
        default=None,
    )
    is_complete: bool = Field(
        description="일정 완료여부",
        examples=[True],
        default=False,
    )
    completed_at: datetime.datetime | None = Field(
        description="일정 완료일시",
        examples=[tz_now()],
        default=None,
    )
    is_repeat: bool = Field(
        description="반복여부",
        examples=[True],
        default=False,
    )
    tags: list[str] | None = Field(
        description="태그 배열",
        examples=[["태그1", "태그2"]],
        default=None,
    )
    calendar_recurring_id: uuid.UUID | None = Field(
        description="반복 일정 아이디",
        examples=[uuid.uuid4()],
        default=None,
    )
    contact_id: uuid.UUID | None = Field(
        description="연락처 아이디",
        examples=[uuid.uuid4()],
        default=None,
    )

    model_config = ConfigDict(from_attributes=True)


class CalendarRecurringOutput(BaseModel):
    id: uuid.UUID = Field(
        description="반복 일정 아이디",
        examples=[uuid.uuid4()],
    )
    start_dt: datetime.datetime = Field(
        description="반복 시작일시",
        examples=[tz_now()],
    )
    end_dt: datetime.datetime = Field(
        description="반복 종료일시",
        examples=[tz_now()],
    )
    interval: int = Field(
        description="반복 간격(개월)",
        examples=[1, 3, 6, 12],
    )
    frequency: str = Field(
        description="반복 주기",
        examples=["일", "월", "년"],
    )

    model_config = ConfigDict(from_attributes=True)


class CalendarContactOutput(BaseModel):
    calendar: CalendarOutput
    contacts: list[ContactOutput]

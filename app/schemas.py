import datetime
from pydantic import BaseModel, Field

from app.utils import tz_now


class User(BaseModel):
    id: int


class UserInCreate(BaseModel):
    ...


class UserProfile(BaseModel):
    id: int = Field(description="유저 아이디", examples=[1])
    email: str = Field(description="이메일", examples=["user@email.com"])
    created_at: datetime.datetime = Field(description="생성일시", examples=[tz_now()])
    updated_at: datetime.datetime = Field(description="변경일시", examples=[tz_now()])

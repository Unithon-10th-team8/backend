from __future__ import annotations


import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
import uuid
from app.base.db import TimestampBase
from app.schemas import UserProfile


class User(TimestampBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    uid: Mapped[str] = mapped_column(sa.String(128), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        sa.Text, nullable=True, default=None
    )  # 이메일이 null 이라면 필수로 받아야 함.

    # relationship
    contacts: Mapped[set[Contact]] = relationship(
        back_populates="user", collection_class=set
    )

    @property
    def profile(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            email=self.email,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Contact(TimestampBase):
    __tablename__ = "contact"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    organization: Mapped[str] = mapped_column(
        sa.String(100), nullable=True, default=None
    )
    position: Mapped[str] = mapped_column(sa.String(100), nullable=True, default=None)
    phone: Mapped[str] = mapped_column(sa.String(30), nullable=True, default=None)
    email: Mapped[str] = mapped_column(sa.Text, nullable=True, default=None)
    category: Mapped[str] = mapped_column(sa.String(100), nullable=True, default=None)
    profile_image_url: Mapped[str] = mapped_column(sa.Text, nullable=True, default=None)
    content: Mapped[str] = mapped_column(sa.String(1000), nullable=True, default=None)
    is_important: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False
    )
    repeat_interval: Mapped[str] = mapped_column(sa.Text, nullable=True, default=None)
    repeat_base_date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True, default=None
    )
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)

    __table_args__ = (sa.Index("contact_user_id_idx", user_id, unique=False),)

    # relationship
    calendars: Mapped[set[Calendar]] = relationship(
        back_populates="contact", collection_class=set
    )


class Calendar(TimestampBase):
    __tablename__ = "calendar"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    start_dt: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    end_dt: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True, default=None
    )
    is_all_day: Mapped[bool] = mapped_column(sa.Boolean, nullable=True, default=None)
    remind_interval: Mapped[int] = mapped_column(
        sa.Integer, nullable=True, default=None
    )  # 분 단위
    is_important: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False
    )
    content: Mapped[str] = mapped_column(sa.String(1000), nullable=True, default=None)
    is_complete: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    completed_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True, default=None
    )
    is_repeat: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    tags: Mapped[list[str]] = mapped_column(
        sa.ARRAY(sa.String(30)), nullable=True, default=None
    )
    calendar_recurring_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("calendar_recurring.id"), nullable=True, default=None
    )
    contact_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("contact.id"), nullable=False
    )

    __table_args__ = (sa.Index("calendar_contact_id_idx", contact_id, unique=False),)


class CalendarRecurring(TimestampBase):
    __tablename__ = "calendar_recurring"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    start_dt: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False
    )
    end_dt: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    interval: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    frequency: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        sa.Index("calendar_recurring_user_id_idx", user_id, unique=False),
    )


class CalendarContact(TimestampBase):
    __tablename__ = "calendar_contact"

    id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    calendar_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("calendar.id"), nullable=False
    )
    contact_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("contact.id"), nullable=False
    )

from app.base.db import TimestampBase
from app.schemas import UserProfile


import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class User(TimestampBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    uid: Mapped[str] = mapped_column(sa.String(128), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    @property
    def profile(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

import datetime
from pydantic import BaseModel
from app.schemas import UserProfile

from app.utils import tz_now


class User(BaseModel):
    id: int
    uid: int | str
    provider: str
    is_active: bool = True
    created_at: datetime.datetime = tz_now()
    updated_at: datetime.datetime = tz_now()

    @property
    def profile(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

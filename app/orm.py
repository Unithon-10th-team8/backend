import datetime
from pydantic import BaseModel
from app.schemas import UserOutput

from app.utils import tz_now


class User(BaseModel):
    id: int
    uid: int | str
    provider: str
    is_active: bool = True
    created_at: datetime.datetime = tz_now()
    updated_at: datetime.datetime = tz_now()

    def to_output(self) -> UserOutput:
        return UserOutput(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

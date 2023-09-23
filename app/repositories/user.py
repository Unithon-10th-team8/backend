import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import User
from app.schemas import UserInput
from app.utils import tz_now


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: int) -> User:
        query = sa.select(User).where(
            sa.and_(User.id == user_id, User.deleted_at.is_(None))
        )
        res = await self._session.execute(query)
        return res.scalar()

    async def get_by_uid(self, uid: str) -> User:
        query = sa.select(User).where(User.uid == uid)
        res = await self._session.execute(query)
        return res.scalar()

    async def fetch(self, offset: int, limit: int) -> list[User]:
        query = (
            sa.select(User).where(User.deleted_at.is_(None)).offset(offset).limit(limit)
        )
        res = await self._session.execute(query)
        return list(res.scalars())

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user

    async def update(self, user_id: int, user_input: UserInput) -> User:
        query = (
            sa.update(User)
            .where(sa.and_(User.id == user_id, User.deleted_at.is_(None)))
            .values(user_input.model_dump())
        )
        await self._session.execute(query)
        await self._session.flush()
        updated_user = await self._session.execute(
            sa.select(User).where(
                sa.and_(User.id == user_id, User.deleted_at.is_(None))
            )
        )
        return updated_user.scalar_one_or_none()

    async def delete(self, user_id: int) -> None:
        query = sa.update(User).where(User.id == user_id).values(deleted_at=tz_now())
        await self._session.execute(query)

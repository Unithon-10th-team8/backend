import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: int) -> User:
        query = sa.select(User).where(User.id == user_id)
        res = await self._session.execute(query)
        return res.scalar()

    async def get_by_uid(self, uid: str) -> User:
        query = sa.select(User).where(User.uid == uid)
        res = await self._session.execute(query)
        return res.scalar()

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user

    async def delete(self, user_id: int) -> None:
        query = sa.delete(User).where(User.id == user_id)
        await self._session.execute(query)

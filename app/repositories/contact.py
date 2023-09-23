from uuid import UUID
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app import orm
from app.schemas import ContactInput
from app.utils import tz_now
from sqlalchemy.orm import selectinload


class ContactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, contact_id: UUID) -> orm.Contact:
        query = (
            sa.select(orm.Contact)
            .where(
                sa.and_(orm.Contact.id == contact_id, orm.Contact.deleted_at.is_(None))
            )
            .options(selectinload(orm.Contact.calendars))
        )
        res = await self._session.execute(query)
        return res.scalar()

    async def fetch(self, user_id: int, offset: int, limit: int) -> list[orm.Contact]:
        query = (
            sa.select(orm.Contact)
            .where(
                sa.and_(
                    orm.Contact.user_id == user_id, orm.Contact.deleted_at.is_(None)
                )
            )
            .offset(offset)
            .limit(limit)
            .order_by(orm.Contact.updated_at.desc())
        )
        res = await self._session.execute(query)
        return list(res.scalars())

    async def create(self, contact: orm.Contact) -> orm.Contact:
        self._session.add(contact)
        await self._session.flush()
        return contact

    async def update(
        self, contact_id: UUID, contact_input: ContactInput
    ) -> orm.Contact:
        query = (
            sa.update(orm.Contact)
            .where(
                sa.and_(
                    orm.Contact.id == contact_id,
                    orm.Contact.deleted_at.is_(None),
                )
            )
            .values(contact_input.model_dump())
        )
        await self._session.execute(query)
        await self._session.flush()
        updated_contact = await self._session.execute(
            sa.select(orm.Contact).where(
                sa.and_(orm.Contact.id == contact_id, orm.Contact.deleted_at.is_(None))
            )
        )
        return updated_contact.scalar_one_or_none()

    async def delete(self, contact_id: UUID) -> None:
        query = (
            sa.update(orm.Contact)
            .where(orm.Contact.id == contact_id)
            .values(deleted_at=tz_now())
        )
        await self._session.execute(query)

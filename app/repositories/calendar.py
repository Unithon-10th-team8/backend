from datetime import datetime
from uuid import UUID
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app import orm
from app.schemas import CalendarInput
from app.utils import tz_now


class CalendarRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, calendar_id: UUID) -> orm.Calendar:
        query = sa.select(orm.Calendar).where(
            sa.and_(
                orm.Calendar.id == calendar_id, orm.Calendar.deleted_at.is_(None)
            )  # TODO: 연락처 중간 테이블로 조인하기
        )
        res = await self._session.execute(query)
        return res.scalar()

    async def fetch(
        self, contact_id: UUID, offset: int, limit: int
    ) -> list[orm.Calendar]:
        query = (
            sa.select(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.contact_id == contact_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .offset(offset)
            .limit(limit)
        )
        res = await self._session.execute(query)
        return list(res.scalars())

    async def fetch_user_calendars(
        self, user_id: int, year: int | None, month: int | None, offset: int, limit: int
    ) -> list[orm.Calendar]:
        query = (
            sa.select(orm.Calendar)
            .join(orm.Contact)
            .where(
                sa.and_(
                    orm.Contact.user_id == user_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
        )

        # year가 None인 경우, 올해 연도로 설정
        if year is None:
            year = datetime.now().year

        query = query.where(sa.extract("year", orm.Calendar.start_dt) == year)

        # month가 주어진 경우, 쿼리에 추가
        if month is not None:
            query = query.where(sa.extract("month", orm.Calendar.start_dt) == month)

        query = query.offset(offset).limit(limit)
        res = await self._session.execute(query)
        return list(res.scalars())

    async def create(self, calendar: orm.Calendar) -> orm.Calendar:
        self._session.add(calendar)
        await self._session.flush()
        return calendar

    async def update(
        self, calendar_id: UUID, calendar_input: CalendarInput
    ) -> orm.Calendar:
        query = (
            sa.update(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .values(calendar_input.model_dump())
        )
        await self._session.execute(query)
        await self._session.flush()
        updated_calendar = await self._session.execute(
            sa.select(orm.Calendar).where(
                sa.and_(
                    orm.Calendar.id == calendar_id, orm.Calendar.deleted_at.is_(None)
                )
            )
        )
        return updated_calendar.scalar_one_or_none()

    async def update_calendar_completion(
        self, calendar_id: UUID, is_complete: bool
    ) -> orm.Calendar:
        query = (
            sa.update(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .values(is_complete=is_complete)
        )
        await self._session.execute(query)
        await self._session.flush()
        updated_calendar = await self._session.execute(
            sa.select(orm.Calendar).where(
                sa.and_(
                    orm.Calendar.id == calendar_id, orm.Calendar.deleted_at.is_(None)
                )
            )
        )
        return updated_calendar.scalar_one_or_none()

    async def update_calendar_importance(
        self, calendar_id: UUID, is_important: bool
    ) -> orm.Calendar:
        query = (
            sa.update(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .values(is_important=is_important)
        )
        await self._session.execute(query)
        await self._session.flush()
        updated_calendar = await self._session.execute(
            sa.select(orm.Calendar).where(
                sa.and_(
                    orm.Calendar.id == calendar_id, orm.Calendar.deleted_at.is_(None)
                )
            )
        )
        return updated_calendar.scalar_one_or_none()

    async def delete(self, calendar_id: UUID) -> None:
        query = (
            sa.update(orm.Calendar)
            .where(orm.Calendar.id == calendar_id)
            .values(deleted_at=tz_now())
        )
        await self._session.execute(query)

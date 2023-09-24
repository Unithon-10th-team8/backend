from datetime import datetime
from uuid import UUID
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app import orm
from app.exceptions import NotFoundError
from app.schemas import CalendarInput
from app.utils import tz_now
from sqlalchemy.orm import subqueryload


class CalendarRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, calendar_id: UUID) -> orm.Calendar:
        """일정을 조회합니다."""
        query = (
            sa.select(orm.Calendar)
            .options(
                subqueryload(orm.Calendar.calendar_contacts).joinedload(
                    orm.CalendarContact.contact
                )
            )
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id, orm.Calendar.deleted_at.is_(None)
                )
            )
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
            .order_by(orm.Calendar.start_dt.asc())
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

        query = query.offset(offset).limit(limit).order_by(orm.Calendar.start_dt.asc())
        res = await self._session.execute(query)
        return list(res.scalars())

    async def create(self, contact_id: UUID, calendar: orm.Calendar) -> orm.Calendar:
        self._session.add(calendar)
        await self._session.flush()

        calendar_contact = orm.CalendarContact(
            contact_id=contact_id, calendar_id=calendar.id
        )
        self._session.add(calendar_contact)
        await self._session.flush()
        return calendar

    async def create_recurring(
        self, recurring: orm.CalendarRecurring
    ) -> orm.CalendarRecurring:
        self._session.add(recurring)
        await self._session.flush()

        return recurring

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
            .values(
                name=calendar_input.name,
                start_dt=calendar_input.start_dt,
                end_dt=calendar_input.end_dt,
                content=calendar_input.content,
                is_all_day=calendar_input.is_all_day,
                is_repeat=calendar_input.is_repeat,
                is_complete=calendar_input.is_complete,
                is_important=calendar_input.is_important,
                remind_interval=calendar_input.remind_interval,
                completed_at=calendar_input.completed_at,
                tags=calendar_input.tags,
            )
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

    async def update_calendar_completion(self, calendar_id: UUID) -> orm.Calendar:
        query = (
            sa.select(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .with_for_update()
        )
        res = await self._session.execute(query)
        calendar = res.scalar_one_or_none()
        if not calendar:
            raise NotFoundError("존재하지 않는 일정입니다.")
        calendar.is_complete = not calendar.is_complete
        return calendar

    async def update_calendar_importance(self, calendar_id: UUID) -> orm.Calendar:
        query = (
            sa.select(orm.Calendar)
            .where(
                sa.and_(
                    orm.Calendar.id == calendar_id,
                    orm.Calendar.deleted_at.is_(None),
                )
            )
            .with_for_update()
        )
        res = await self._session.execute(query)
        calendar = res.scalar_one_or_none()
        if not calendar:
            raise NotFoundError("존재하지 않는 일정입니다.")
        calendar.is_important = not calendar.is_important
        return calendar

    async def delete(self, calendar_id: UUID) -> None:
        query = (
            sa.update(orm.Calendar)
            .where(orm.Calendar.id == calendar_id)
            .values(deleted_at=tz_now())
        )
        await self._session.execute(query)

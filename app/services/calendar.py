from uuid import UUID
from app import schemas
from app.exceptions import NotFoundError, ValidationError
from app import orm
from app.repositories.calendar import CalendarRepository
import logging

# 로깅 설정 (출력 레벨은 DEBUG)
logging.basicConfig(level=logging.DEBUG)


class CalendarService:
    def __init__(self, calendar_repo: CalendarRepository) -> None:
        self._calendar_repo = calendar_repo

    async def get(self, calendar_id: UUID) -> schemas.CalendarOutput:
        """일정을 조회합니다."""
        calendar = await self._calendar_repo.get(calendar_id)
        if calendar is None:
            raise NotFoundError("일정이 존재하지 않습니다.")

        return schemas.CalendarContactOutput(
            contacts=[
                schemas.ContactOutput.model_validate(contact.contact)
                for contact in calendar.calendar_contacts
            ],
            calendar=schemas.CalendarOutput.model_validate(calendar),
        )

    async def fetch(
        self, contact_id: UUID, offset: int, limit: int
    ) -> list[schemas.CalendarOutput]:
        """복수 일정을 조회합니다."""
        calendars = await self._calendar_repo.fetch(contact_id, offset, limit)
        return [
            schemas.CalendarOutput.model_validate(calendar) for calendar in calendars
        ]

    async def fetch_user_calendars(
        self, user_id: int, year: int | None, month: int | None, offset: int, limit: int
    ) -> list[schemas.CalendarOutput]:
        """유저의 모든 일정을 조회합니다."""
        calendars = await self._calendar_repo.fetch_user_calendars(
            user_id, year, month, offset, limit
        )
        return [
            schemas.CalendarOutput.model_validate(calendar) for calendar in calendars
        ]

    async def create(
        self, user_id: int, contact_id: UUID, calendar_input: schemas.CalendarInput
    ) -> schemas.CalendarOutput:
        """복수 일정을 조회합니다."""
        if calendar_input.is_repeat:
            try:
                recurring = await self._calendar_repo.create_recurring(
                    orm.CalendarRecurring(
                        **calendar_input.recurring_input.model_dump(), user_id=user_id
                    )
                )
            except Exception as e:
                logging.debug(f"반복 설정 생성 실패 {e}")
                raise ValidationError("반복 설정이 잘못되었습니다.")
        else:
            recurring = None

        calendar = orm.Calendar(
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
            contact_id=contact_id,
            calendar_recurring_id=recurring.id if recurring else None,
        )

        calendar = await self._calendar_repo.create(contact_id, calendar)
        return schemas.CalendarOutput.model_validate(calendar)

    async def update(
        self, calendar_id: UUID, calendar_input: schemas.CalendarInput
    ) -> schemas.CalendarOutput:
        """일정을 수정합니다."""
        calendar = await self._calendar_repo.update(calendar_id, calendar_input)
        if calendar is None:
            raise NotFoundError("일정이 존재하지 않습니다.")

        return schemas.CalendarOutput.model_validate(calendar)

    async def delete(self, calendar_id: UUID) -> None:
        """일정을 삭제합니다."""
        await self._calendar_repo.delete(calendar_id)

    async def update_calendar_completion(
        self, calendar_id: UUID
    ) -> schemas.CalendarOutput:
        """일정 완료 여부를 수정합니다."""
        calendar = await self._calendar_repo.update_calendar_completion(calendar_id)
        if calendar is None:
            raise NotFoundError("일정이 존재하지 않습니다.")

        return schemas.CalendarOutput.model_validate(calendar)

    async def update_calendar_importance(
        self, calendar_id: UUID
    ) -> schemas.CalendarOutput:
        """일정 중요여부를 수정합니다."""
        calendar = await self._calendar_repo.update_calendar_importance(calendar_id)
        if calendar is None:
            raise NotFoundError("일정이 존재하지 않습니다.")

        return schemas.CalendarOutput.model_validate(calendar)

from uuid import UUID
from app import schemas
from app.exceptions import NotFoundError
from app import orm
from app.repositories.calendar import CalendarRepository


class CalendarService:
    def __init__(self, calendar_repo: CalendarRepository) -> None:
        self._calendar_repo = calendar_repo

    async def get(self, calendar_id: UUID) -> schemas.CalendarOutput:
        """일정을 조회합니다."""
        calendar = await self._calendar_repo.get(calendar_id)
        if calendar is None:
            raise NotFoundError("일정이 존재하지 않습니다.")

        return schemas.CalendarOutput.model_validate(calendar)

    async def fetch(
        self, contact_id: UUID, offset: int, limit: int
    ) -> list[schemas.CalendarOutput]:
        """복수 일정을 조회합니다."""
        calendars = await self._calendar_repo.fetch(contact_id, offset, limit)
        return [
            schemas.CalendarOutput.model_validate(calendar) for calendar in calendars
        ]

    async def create(
        self, contact_id: UUID, calendar_input: schemas.CalendarInput
    ) -> schemas.CalendarOutput:
        """복수 일정을 조회합니다."""
        # TODO: 반복일정 생성 추가
        calendar = orm.Calendar(**calendar_input.model_dump(), contact_id=contact_id)
        calendar = await self._calendar_repo.create(calendar)
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

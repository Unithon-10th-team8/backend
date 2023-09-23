from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, schemas
from app.services.calendar import CalendarService

router = APIRouter()


@router.get(
    "/contacts/{contact_id}/calendars",
    status_code=HTTP_200_OK,
    response_model=list[schemas.CalendarOutput],
)
async def fetch_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_service: CalendarService = Depends(deps.calendar_service),
    offset: int = 0,
    limit: int = 100,
) -> list[schemas.CalendarOutput]:
    """복수 연락처를 조회합니다."""
    calendar = await calendar_service.fetch(contact_id, offset=offset, limit=limit)
    return calendar


@router.get(
    "/contacts/{contact_id}/calendars/{calendar_id}",
    status_code=HTTP_200_OK,
    response_model=None,
)
async def get_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_id: UUID,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    """연락처를 조회합니다."""
    calendar = await calendar_service.get(calendar_id)
    return calendar


@router.post(
    "/contacts/{contact_id}/calendars",
    status_code=HTTP_200_OK,
    response_model=schemas.CalendarOutput,
)
async def create_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_input: schemas.CalendarInput,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    calendar = await calendar_service.create(contact_id, calendar_input)
    return calendar


@router.post(
    "/contacts/{contact_id}/calendars/{calendar_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.CalendarOutput,
)
async def update_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_id: UUID,
    calendar_input: schemas.CalendarInput,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    calendar = await calendar_service.update(calendar_id, calendar_input)
    return calendar


@router.delete(
    "/contacts/{contact_id}/calendars/{calendar_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_id: UUID,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> None:
    await calendar_service.delete(calendar_id)

from uuid import UUID

from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, schemas
from app.services.calendar import CalendarService

router = APIRouter()


@router.get(
    "/calendars",
    status_code=HTTP_200_OK,
    response_model=list[schemas.CalendarOutput],
)
async def fetch_user_calendars(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    user_id: int,
    year: int | None = None,
    month: int | None = None,
    offset: int = 0,
    limit: int = 10,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> list[schemas.CalendarOutput]:
    """유저의 모든 캘린더를 가져옵니다."""
    calendars = await calendar_service.fetch_user_calendars(
        user_id, year, month, offset, limit
    )
    return calendars


@router.post(
    "/calendars/{calendar_id}/completion",
    status_code=HTTP_200_OK,
    response_model=schemas.CalendarOutput,
)
async def update_calendar_completion(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    calendar_id: UUID,
    is_complete: bool = Body(..., embed=True),
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    """일정을 완료 처리합니다."""
    calendar = await calendar_service.update_calendar_completion(
        calendar_id, is_complete
    )
    return calendar


@router.patch(
    "/calendars/{calendar_id}/importance",
    status_code=HTTP_200_OK,
    response_model=schemas.CalendarOutput,
)
async def update_calendar_importance(
    calendar_id: UUID,
    is_important: bool = Body(..., embed=True),
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    """일정의 '중요함' 상태를 업데이트합니다."""
    calendar = await calendar_service.update_calendar_importance(
        calendar_id, is_important
    )
    return calendar


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
    """복수 캘린더를 조회합니다."""
    calendar = await calendar_service.fetch(contact_id, offset=offset, limit=limit)
    return calendar


@router.get(
    "/contacts/{contact_id}/calendars/{calendar_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.CalendarOutput,
)
async def get_calendar(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    calendar_id: UUID,
    calendar_service: CalendarService = Depends(deps.calendar_service),
) -> schemas.CalendarOutput:
    """캘린더를 조회합니다."""
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
    """캘린더를 생성합니다."""
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
    """캘린더를 수정합니다."""
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
    """캘린더를 삭제합니다."""
    await calendar_service.delete(calendar_id)

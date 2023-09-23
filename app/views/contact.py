from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, schemas
from app.services.contact import ContactService

router = APIRouter()


@router.get(
    "/contacts",
    status_code=HTTP_200_OK,
    response_model=list[schemas.ContactOutput],
)
async def fetch_contact(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_service: ContactService = Depends(deps.contact_service),
    offset: int = 0,
    limit: int = 100,
) -> list[schemas.ContactOutput]:
    """복수 연락처를 조회합니다."""
    user_id = 1  # TODO: 로그인 기능 추가하면 제거
    contact = await contact_service.fetch(user_id, offset=offset, limit=limit)
    return contact


@router.get(
    "/contacts/{contact_id}",
    status_code=HTTP_200_OK,
    response_model=None,
)
async def get_contact(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    contact_service: ContactService = Depends(deps.contact_service),
) -> schemas.ContactOutput:
    """연락처를 조회합니다."""
    contact = await contact_service.get(contact_id)
    return contact


@router.post(
    "/contacts",
    status_code=HTTP_200_OK,
    response_model=schemas.ContactOutput,
)
async def create_contact(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_input: schemas.ContactInput,
    contact_service: ContactService = Depends(deps.contact_service),
) -> schemas.ContactOutput:
    user_id = 1  # TODO: 로그인 기능 추가하면 제거
    contact = await contact_service.create(user_id, contact_input)
    return contact


@router.post(
    "/contacts/{contact_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.ContactOutput,
)
async def update_contact(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    contact_input: schemas.ContactInput,
    contact_service: ContactService = Depends(deps.contact_service),
) -> schemas.ContactOutput:
    contact = await contact_service.update(contact_id, contact_input)
    return contact


@router.delete(
    "/contacts/{contact_id}",
    status_code=HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_contact(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_id: UUID,
    contact_service: ContactService = Depends(deps.contact_service),
) -> None:
    await contact_service.delete(contact_id)

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
    current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_service: ContactService = Depends(deps.contact_service),
    offset: int = 0,
    limit: int = 100,
) -> list[schemas.ContactOutput]:
    """복수 연락처를 조회합니다."""
    contact = await contact_service.fetch(current_user.id, offset=offset, limit=limit)
    return contact


@router.get(
    "/contacts/{contact_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.ContactOutput,
)
async def get_contact(
    contact_id: UUID,
    current_user: schemas.UserProfile = Depends(deps.current_user),
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
    contact_input: schemas.ContactInput,
    current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_service: ContactService = Depends(deps.contact_service),
) -> schemas.ContactOutput:
    contact = await contact_service.create(current_user.id, contact_input)
    return contact


@router.post(
    "/contacts/{contact_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.ContactOutput,
)
async def update_contact(
    contact_id: UUID,
    contact_input: schemas.ContactInput,
    current_user: schemas.UserProfile = Depends(deps.current_user),
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
    contact_id: UUID,
    current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_service: ContactService = Depends(deps.contact_service),
) -> None:
    await contact_service.delete(contact_id)


@router.post(
    "/contacts/{contact_id}/importance",
    status_code=HTTP_200_OK,
    response_model=schemas.ContactOutput,
)
async def update_contact_importance(
    contact_id: UUID,
    current_user: schemas.UserProfile = Depends(deps.current_user),
    contact_service: ContactService = Depends(deps.contact_service),
) -> schemas.ContactOutput:
    """연락처의 '중요함' 상태를 업데이트합니다."""
    contact = await contact_service.update_contact_importance(contact_id)
    return contact

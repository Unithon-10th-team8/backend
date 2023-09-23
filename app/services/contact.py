from uuid import UUID
from app import schemas
from app.exceptions import NotFoundError
from app import orm
from app.repositories.contact import ContactRepository


class ContactService:
    def __init__(self, contact_repo: ContactRepository) -> None:
        self._contact_repo = contact_repo

    async def get(self, contact_id: UUID) -> schemas.ContactOutput:
        """연락처를 조회합니다."""
        contact = await self._contact_repo.get(contact_id)
        if contact is None:
            raise NotFoundError("연락처가 존재하지 않습니다.")

        return schemas.ContactOutput.model_validate(contact)

    async def fetch(
        self, user_id: int, offset: int, limit: int
    ) -> list[schemas.ContactOutput]:
        """복수 연락처를 조회합니다."""
        contacts = await self._contact_repo.fetch(user_id, offset, limit)
        return [schemas.ContactOutput.model_validate(contact) for contact in contacts]

    async def create(
        self, user_id: int, contact_input: schemas.ContactInput
    ) -> schemas.ContactOutput:
        """복수 연락처를 조회합니다."""
        contact = orm.Contact(**contact_input.model_dump(), user_id=user_id)
        contact = await self._contact_repo.create(contact)
        return schemas.ContactOutput.model_validate(contact)

    async def update(
        self, contact_id: UUID, contact_input: schemas.ContactInput
    ) -> schemas.ContactOutput:
        """연락처를 수정합니다."""
        contact = await self._contact_repo.update(contact_id, contact_input)
        if contact is None:
            raise NotFoundError("연락처가 존재하지 않습니다.")

        return schemas.ContactOutput.model_validate(contact)

    async def delete(self, contact_id: UUID) -> None:
        """연락처를 삭제합니다."""
        await self._contact_repo.delete(contact_id)

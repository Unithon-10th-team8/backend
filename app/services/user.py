from app import schemas
from app.exceptions import NotFoundError
from app.orm import User
from app.repositories.user import UserRepository
from app.base.provider import GoogleProviderUserInfo


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def get_or_create_user(self, provider: str, provider_data: GoogleProviderUserInfo) -> schemas.UserProfile:
        """유저를 가져오거나 생성합니다."""
        user = await self._user_repo.get_by_uid(provider_data['uid'])
        if user:
            return user.profile
        else:
            user = await self._user_repo.create(
                User(uid=provider_data['uid'], provider=provider, name=provider_data['name'],
                     email=provider_data['email'], profile_image_url=provider_data['picture'],
                     google_access_token=provider_data['access_token'],
                     google_refresh_token=provider_data['refresh_token']))
            return user.profile

    async def get(self, user_id: int) -> schemas.UserProfile:
        """유저를 조회합니다."""
        user = await self._user_repo.get(user_id)
        return user.profile

    async def fetch(self, offset: int, limit: int) -> list[schemas.UserProfile]:
        """복수 유저를 조회합니다."""
        users = await self._user_repo.fetch(offset, limit)
        return [user.profile for user in users]

    async def update(
            self, user_id: int, user_input: schemas.UserInput
    ) -> schemas.UserProfile:
        """유저를 수정합니다."""
        user = await self._user_repo.update(user_id, user_input)
        if user is None:
            raise NotFoundError("유저가 존재하지 않습니다.")

        return user.profile

    async def delete(self, user_id: int) -> None:
        """유저를 삭제합니다."""
        await self._user_repo.delete(user_id)

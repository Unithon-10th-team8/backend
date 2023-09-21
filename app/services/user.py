from app import schemas
from app.orm import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def get_or_create_user(self, provider: str, uid: str) -> schemas.UserProfile:
        """유저를 가져오거나 생성합니다."""
        user = await self._user_repo.get_by_uid(uid)
        if user:
            return user.profile
        else:
            user = await self._user_repo.create(User(uid=uid, provider=provider))
            return user.profile

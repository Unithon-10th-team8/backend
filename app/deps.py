from fastapi import Cookie

from app.base.auth import decode_token
from app.repositories.user import UserRepository
from app.schemas import User
from app.services.user import UserService
from app.exceptions import NotFoundError, PermissionError


async def current_user(
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
) -> User:
    if access_token and refresh_token:
        try:
            result = decode_token(access_token)
        except Exception:
            result = decode_token(refresh_token)
            # TODO: refresh_token 이 정상이라면 access_token 재발급

        user_repo = UserRepository()
        user = await user_repo.get(result["user_id"])
        if user:
            return user.to_output()

        raise NotFoundError(f"{result['user_id']} 유저는 존재하지 않습니다.")
    else:
        raise PermissionError(
            f"{access_token=}, {refresh_token=} 토큰이 유효하지 않습니다."
        )  # noqa


def user_service() -> UserService:
    user_repo = UserRepository()
    return UserService(user_repo)

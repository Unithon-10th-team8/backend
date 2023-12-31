from app.repositories.calendar import CalendarRepository
from app.services.calendar import CalendarService
from app.services.contact import ContactService
from fastapi import Cookie, Depends, Request

from app.base.auth import decode_token
from app.repositories.contact import ContactRepository
from app.repositories.user import UserRepository
from app.schemas import UserProfile
from app.services.user import UserService
from app.exceptions import NotFoundError, PermissionError
from sqlalchemy.ext.asyncio import AsyncSession


def session(request: Request) -> AsyncSession:
    return request.state.session


async def current_user(
    session: AsyncSession = Depends(session),
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
) -> UserProfile:
    if access_token and refresh_token:
        try:
            result = decode_token(access_token)
        except Exception:
            result = decode_token(refresh_token)

        user_repo = UserRepository(session)
        user = await user_repo.get(result["user_id"])
        if user:
            return user.profile

        raise NotFoundError(f"{result['user_id']} 유저는 존재하지 않습니다.")
    else:
        raise PermissionError(
            f"{access_token=}, {refresh_token=} 토큰이 유효하지 않습니다."
        )  # noqa


def user_repo(session: AsyncSession = Depends(session)) -> UserRepository:
    return UserRepository(session)


def user_service(user_repo: UserRepository = Depends(user_repo)) -> UserService:
    return UserService(user_repo)


def contact_repo(session: AsyncSession = Depends(session)) -> ContactRepository:
    return ContactRepository(session)


def contact_service(
    contact_repo: ContactRepository = Depends(contact_repo),
) -> ContactService:
    return ContactService(contact_repo)


def calendar_repo(session: AsyncSession = Depends(session)) -> CalendarRepository:
    return CalendarRepository(session)


def calendar_service(
    calendar_repo: CalendarRepository = Depends(calendar_repo),
) -> CalendarService:
    return CalendarService(calendar_repo)

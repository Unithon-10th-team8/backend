from typing import Literal

from fastapi import APIRouter, Body, Depends, Response
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, schemas
from app.base.auth import login
from app.base.provider import KakaoAuthProvider

from app.exceptions import ValidationError
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/social-login/{provider}",
    status_code=HTTP_200_OK,
    response_model=schemas.UserProfile,
)
async def social_login(
    response: Response,
    provider: Literal["kakao", "apple"],
    token: str = Body(embed=True),
    user_service: UserService = Depends(deps.user_service),
) -> schemas.UserProfile:
    """소셜 로그인을 합니다."""
    if provider == "kakao":
        kakao_provider = KakaoAuthProvider(token)
        user_info = kakao_provider.get_user_info()
    else:
        raise ValidationError(f"지원하지 않는 소셜 플랫폼입니다. '{provider}'")
    user = await user_service.get_or_create_user(provider, user_info["uid"])
    login(response, user)
    return user


# TODO: 로그인 구현 후 활성화
@router.get(
    "/users/me",
    status_code=HTTP_200_OK,
    response_model=None,
)
async def get_me(
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> None:
    """내 정보를 조회합니다. (로그인 필요 후 활성화 예정)"""
    return None
    # user_profile = await user_service.get(current_user.id)
    # return user_profile


@router.get(
    "/users",
    status_code=HTTP_200_OK,
    response_model=list[schemas.UserProfile],
)
async def fetch_users(
    user_service: UserService = Depends(deps.user_service),
    offset: int = 0,
    limit: int = 100,
) -> list[schemas.UserProfile]:
    """복수 유저를 조회합니다."""
    user_profiles = await user_service.fetch(offset=offset, limit=limit)
    return user_profiles


@router.post(
    "/users/{user_id}",
    status_code=HTTP_200_OK,
    response_model=schemas.UserProfile,
)
async def update_user(
    user_id: int,
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    user_input: schemas.UserInput = Body(..., embed=True),
    user_service: UserService = Depends(deps.user_service),
) -> schemas.UserProfile:
    """내 정보를 수정합니다."""
    # TODO: 로그인 구현 후 유저 유효성 검사
    await user_service.update(user_id, user_input)
    user_profile = await user_service.get(user_id)
    return user_profile


@router.delete(
    "/users/{user_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    # current_user: schemas.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> None:
    """내 정보를 삭제합니다.(회원 탈퇴)"""
    await user_service.delete(user_id)

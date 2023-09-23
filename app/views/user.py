from typing import Literal

from fastapi import APIRouter, Body, Depends, Response
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, schemas
from app.base.auth import login
from app.base.config import config
from app.base.provider import GoogleAuthProvider

from app.exceptions import ValidationError
from app.services.user import UserService

router = APIRouter()


@router.get(
    "/social-login/{provider}",
    status_code=HTTP_200_OK,
    response_model=schemas.UserProfile,
)
async def social_login(
    provider: Literal["kakao", "google"],
) -> schemas.UserProfile:
    # redirect to kakao / google login page
    if provider == "kakao":
        raise ValidationError("아직 구현되지 않은 소셜 플랫폼입니다. 'kakao'")
    elif provider == "google":
        provider_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": config.google_client_id,
            "redirect_uri": config.google_redirect_uri,
            "response_type": "code",
            "scope": "email profile",
            "access_type": "offline",
        }
        param_string = "&".join([f"{key}={value}" for key, value in params.items()])
        redirect_url = f"{provider_url}?{param_string}"

    return RedirectResponse(redirect_url)


@router.get(
    "/social-login/{provider}/callback",
    status_code=HTTP_200_OK,
    response_model=schemas.UserProfile,
)
async def social_login_callback(
    response: Response,
    provider: Literal["kakao", "google"],
    code: str,
    user_service: UserService = Depends(deps.user_service),
) -> schemas.UserProfile:
    """소셜 로그인을 합니다."""
    if provider == "kakao":
        raise ValidationError("아직 구현되지 않은 소셜 플랫폼입니다. 'kakao'")
        # kakao_provider = KakaoAuthProvider(token)
        # user_info = kakao_provider.get_user_info()
    elif provider == "google":
        google_provider = GoogleAuthProvider(code)
        google_provider.get_access_token()
        user_info = google_provider.get_user_info()
    else:
        raise ValidationError(f"지원하지 않는 소셜 플랫폼입니다. '{provider}'")
    user = await user_service.get_or_create_user(provider, user_info)
    login(response, user)

    return RedirectResponse(config.frontend_url)


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
    current_user: schemas.UserProfile = Depends(deps.current_user),
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
    current_user: schemas.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> None:
    """내 정보를 삭제합니다.(회원 탈퇴)"""
    if current_user.id != user_id:
        raise ValidationError("본인만 탈퇴할 수 있습니다.")
    await user_service.delete(user_id)

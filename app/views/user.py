from typing import Literal

from fastapi import APIRouter, Body, Depends, Response
from starlette.status import HTTP_200_OK

from app import deps, schemas
from app.base.auth import login
from app.base.provider import KakaoAuthProvider

from app.exceptions import ValidationError
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/social-login/{provider}",
    status_code=HTTP_200_OK,
    response_model=schemas.UserOutput,
)
async def social_login(
    response: Response,
    provider: Literal["kakao", "apple"],
    token: str = Body(embed=True),
    user_service: UserService = Depends(deps.user_service),
) -> schemas.UserOutput:
    """소셜 로그인을 합니다."""
    if provider == "kakao":
        kakao_provider = KakaoAuthProvider(token)
        user_info = kakao_provider.get_user_info()
    else:
        raise ValidationError(f"지원하지 않는 소셜 플랫폼입니다. '{provider}'")
    user = await user_service.get_or_create_user(provider, user_info["uid"])
    login(response, user)
    return user

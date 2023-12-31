import datetime
from typing import Any
from app import schemas

from fastapi import Response
from app.base.config import config

import jwt

from app.utils import tz_now

issuer = "team8"  # 추후 변경


def create_token(
    payload: dict[str, Any],
    expires_delta: datetime.timedelta,
    algorithm: str = "HS256",
) -> str:
    """토큰을 생성합니다."""
    payload["iss"] = issuer
    payload["iat"] = iat = tz_now()
    payload["exp"] = iat + expires_delta
    return jwt.encode(payload, config.secret_key, algorithm=algorithm)


def decode_token(token: str, algorithm: str = "HS256") -> dict[str, Any]:
    """토큰을 디코딩합니다."""
    options = {"verify_exp": True, "verify_iss": True}
    return jwt.decode(
        token,
        config.secret_key,
        options=options,
        issuer=issuer,
        algorithms=[algorithm],
    )


def login(response: Response, user: schemas.UserProfile) -> None:
    """쿠키를 응답하여 자동 로그인합니다."""
    payload = {"user_id": user.id}
    access_token = create_token(payload, datetime.timedelta(hours=1))
    refresh_token = create_token(payload, datetime.timedelta(days=21))
    _set_cookie(response, key="access_token", value=access_token)
    _set_cookie(response, key="refresh_token", value=refresh_token)


def _set_cookie(response: Response, key: str, value: str) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=60 * 60 * 24 * 30,  # 30일
        domain="haenu.dev",
        path="/",
        # domain=config.frontend_domain,
        httponly=True,
        secure=True,
    )

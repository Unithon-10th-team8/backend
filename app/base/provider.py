from typing import TypedDict
from app.exceptions import ValidationError
import requests
from app.base.config import config


class ProviderUserInfo(TypedDict):
    uid: str


class GoogleProviderUserInfo(TypedDict):
    uid: str
    email: str
    name: str
    picture: str
    access_token: str = ''
    refresh_token: str = ''


class KakaoAuthProvider:
    def __init__(self, token: str) -> None:
        self._token = token

    def get_user_info(self) -> ProviderUserInfo:
        res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        if res.status_code != 200:
            try:
                message = res.json()["msg"]
            except KeyError:
                message = f"Something went wrong while getting user information\
                    {res.status_code}"
            raise ValidationError(message)

        data = res.json()
        user_info = ProviderUserInfo(uid=str(data["id"]))
        return user_info


class GoogleAuthProvider:
    def __init__(self, code: str = '', access_token: str = '', refresh_token: str = '') -> None:
        self._code = code
        self._access_token = access_token
        self._refresh_token = refresh_token

    def get_access_token(self) -> str:
        data = {
            "code": self._code,
            "client_id": config.google_client_id,
            "client_secret": config.google_client_secret,
            "redirect_uri": config.google_redirect_uri,
            "grant_type": "authorization_code",
        }
        res = requests.post(
            "https://oauth2.googleapis.com/token",
            data=data,
        )
        if res.status_code != 200:
            try:
                message = res.json()["error_description"]
            except KeyError:
                message = f"Something went wrong while getting access token\
                    {res.status_code}"
            raise ValidationError(message)

        data = res.json()
        self._access_token = data["access_token"]
        self._refresh_token = data["refresh_token"]
        return self._access_token

    def get_user_info(self) -> GoogleProviderUserInfo:
        res = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        if res.status_code != 200:
            try:
                message = res.json()["msg"]
            except KeyError:
                message = f"Something went wrong while getting user information\
                    {res.status_code}"
            raise ValidationError(message)

        data = res.json()
        user_info = GoogleProviderUserInfo(uid=str(data["id"]), email=data["email"], name=data["name"],
                                           picture=data["picture"], access_token=self._access_token,
                                           refresh_token=self._refresh_token)
        return user_info

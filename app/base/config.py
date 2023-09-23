from pydantic_settings import BaseSettings


class Config(BaseSettings):
    secret_key: str
    db_url: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    frontend_url: str
    frontend_domain: str

    class Config:
        env_file = "./secrets/.env"
        env_file_encoding = "utf-8"
        extra = "allow"


config = Config()

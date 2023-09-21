from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: str
    DB_URL: str

    class Config:
        env_file = "./secrets/.env"
        env_file_encoding = "utf-8"


config = Config()

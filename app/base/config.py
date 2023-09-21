from pydantic_settings import BaseSettings


class Config(BaseSettings):
    secret_key: str
    db_url: str

    class Config:
        env_file = "./secrets/.env"
        env_file_encoding = "utf-8"


config = Config()

from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    filename: str
    mode: Literal['full']

    class Config:
        env_file = 'dev_env'


settings = Settings()
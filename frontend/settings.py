from typing import List, Optional, Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FRONENT_PORT: str = "5000"
    MODE: str = "production" # production, debug

settings = Settings()

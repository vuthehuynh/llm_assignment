from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, validator


class Settings(BaseSettings):
    FRONENT_PORT: str = "8000"
    MODE: str = "debug" # DEVELOPMENT, PRODUCTION

settings = Settings()
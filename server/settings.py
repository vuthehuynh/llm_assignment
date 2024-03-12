from typing import List, Optional, Union

from pydantic_setting import BaseSettings


class Settings(BaseSettings):
    API_VERSION_STR: str = "/api/v1"
    API_PORT: int = 5000

    PROJECT_NAME: str = "LLMQnA"


settings = Settings()

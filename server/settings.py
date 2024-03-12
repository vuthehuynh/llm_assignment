from typing import List, Optional, Union

from pydantic_setting import BaseSettings


class Settings(BaseSettings):
    # API_SECRET_KEY: str = "MySecretKey"
    API_VERSION_STR: str = "/api/v1"
    # SERVER_NAME: str = "LLMQnA"
    # SERVER_HOST: AnyHttpUrl = None
    API_PORT: int = 8000
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.ftech.ai"]'
    # BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    PROJECT_NAME: str = "LLMQnA"
    # SENTRY_DSN: Union[HttpUrl, None] = None

    class Config:
        # case_sensitive = True
        env_file = ".env"
        # env_file_encoding = "utf-8"


settings = Settings()

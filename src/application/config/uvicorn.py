from pydantic import BaseSettings, Field


class UvicornConfigModel(BaseSettings):
    worker_count: int = Field(env="UVICORN_WORKER_COUNT", default=1)

from pydantic import BaseSettings, Field


DEFAULT_NAME: str = "DEFAULT"
DEFAULT_URL: str = "redis://localhost:6379"
DEFAULT_DB_INDEX: int = 0
DEFAULT_POOL_MINSIZE: int = 10
DEFAULT_POOL_MAXSIZE: int = 20


class RedisConfig(BaseSettings):
    name: str = DEFAULT_NAME
    url: str = Field(env=f"REDIS_{DEFAULT_NAME}_URL", default=DEFAULT_URL)
    db_index: int = Field(env=f"REDIS_{DEFAULT_NAME}_DB_INDEX", default=DEFAULT_DB_INDEX)
    pool_minsize: int = Field(env=f"REDIS_{DEFAULT_NAME}_POOL_MINSIZE",default=DEFAULT_POOL_MINSIZE)
    pool_maxsize: int = Field(env=f"REDIS_{DEFAULT_NAME}_POOL_MAXSIZE", default=DEFAULT_POOL_MAXSIZE)

from pydantic import BaseSettings, Field
import os
import logging

logger = logging.getLogger(__package__)


DEFAULT_NAME: str = "DEFAULT"
DEFAULT_URL: str = "redis://localhost:6379"
DEFAULT_DB_INDEX: int = 0
DEFAULT_POOL_MINSIZE: int = 10
DEFAULT_POOL_MAXSIZE: int = 20
DEFAULT_REDIS_PASSWORD_FILE_PATH = "/var/run/secrets/redis/password"


def redis_config_password_factory():
    _redis_password_path = os.getenv("REDIS_DEFAULT_PASSWORD_PATH", default=DEFAULT_REDIS_PASSWORD_FILE_PATH)
    if os.path.isfile(path=_redis_password_path):
        with open(file=_redis_password_path, mode="r") as _file:
            _password = _file.read()
        return _password
    else:
        logger.debug("No File")
        return None

class RedisConfig(BaseSettings):
    name: str = DEFAULT_NAME
    url: str = Field(env=f"REDIS_{DEFAULT_NAME}_URL", default=DEFAULT_URL)
    password: str = Field(env=f"REDIS_{DEFAULT_NAME}_PASSWORD", default_factory=redis_config_password_factory)
    db_index: int = Field(env=f"REDIS_{DEFAULT_NAME}_DB_INDEX", default=DEFAULT_DB_INDEX)
    pool_minsize: int = Field(env=f"REDIS_{DEFAULT_NAME}_POOL_MINSIZE",default=DEFAULT_POOL_MINSIZE)
    pool_maxsize: int = Field(env=f"REDIS_{DEFAULT_NAME}_POOL_MAXSIZE", default=DEFAULT_POOL_MAXSIZE)

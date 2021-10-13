from contextlib import asynccontextmanager
from typing import AsyncContextManager
from aioredis import ConnectionPool
from aioredis import Redis
import logging

from application.service.health import HealthService
from .config.redis import RedisConfig
logger=logging.getLogger(__package__)


class Cache:

    ENCODING = "UTF-8"

    redis_config: RedisConfig
    health_service: HealthService

    _name: str
    _redis_pool: ConnectionPool = None

    def __init__(self, redis_config: RedisConfig, application_instance_name: str, health_service: HealthService) -> None:
        self.redis_config = redis_config
        self.health_service = health_service
        self._name = f"{application_instance_name}-redis-{self.redis_config.name}"

    async def init_connection_pool(self) -> None:
        try:
            ConnectionPool()
            self._redis_pool = ConnectionPool(
                encoding=self.ENCODING,
                address=self.redis_config.url,
                db=self.redis_config.db_index,
                minsize=self.redis_config.pool_minsize,
                maxsize=self.redis_config.pool_maxsize)
        except Exception as e:
            self.health_service.set_cache_health(cache_health=False)
            logger.critical(f"Redis {self._name} Engine Unable to be created")
            logger.exception(e)
        else:
            self.health_service.set_cache_health(cache_health=True)
            logger.info(f"Redis {self._name=} Engine Creation Success")

    @asynccontextmanager
    async def acquire(self) -> AsyncContextManager[Redis]:
        try:
            _redis_connection = await self._redis_pool.acquire()
        except Exception as e:
            logger.critical(msg=f"Unable to acquire RedisConnection from {self._name}")
            logger.exception(e)
        else:
            _redis = Redis(_redis_connection)
            yield _redis
            self._redis_pool.release(_redis_connection)

    async def close_connection_pool(self) -> None:
        if self._redis_pool is not None:
            await self._redis_pool.disconnect()
            
            logger.info(f"Redis {self._name=} Engine Close Success")
        else:
            logger.warning(f"Redis {self._name=} Engine Already Close Warning")
        #
        self.health_service.set_cache_health(cache_health=False)
        self._redis_pool = None

    def is_connected(self) -> bool:
        if self._redis_pool is not None:
            return self._redis_pool.closed == False
        else:
            return False

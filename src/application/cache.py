from contextlib import asynccontextmanager
from typing import AsyncContextManager
from aioredis import Redis, create_redis_pool, ConnectionsPool
import logging

from application.service.health import HealthService
from .config.redis import RedisConfig
logger=logging.getLogger(__package__)


class Cache:

    ENCODING = "UTF-8"

    redis_config: RedisConfig
    health_service: HealthService

    _name: str
    _redis_pool: ConnectionsPool = None

    def __init__(self, redis_config: RedisConfig, application_instance_name: str, health_service: HealthService) -> None:
        self.redis_config = redis_config
        self.health_service = health_service
        self._name = f"{application_instance_name}-redis-{self.redis_config.name}"

    async def init_connection_pool(self) -> None:
        try:
            self._redis_pool = await create_redis_pool(
                encoding=self.ENCODING,
                address=self.redis_config.url,
                password=self.redis_config.password,
                db=self.redis_config.db_index,
                maxsize=self.redis_config.pool_maxsize,
                minsize=self.redis_config.pool_minsize
            )
            print(self._redis_pool)
        except Exception as e:
            self.health_service.set_cache_health(cache_health=False)
            logger.error(self.redis_config)
            logger.critical(f"Redis {self._name} Engine Unable to be created")
            logger.exception(e)
        else:
            self.health_service.set_cache_health(cache_health=True)
            logger.info(f"Redis {self._name=} Engine Creation Success")

    @asynccontextmanager
    async def acquire(self) -> AsyncContextManager[Redis]:
        try:
            _redis_connection = await self._redis_pool.connection.acquire()
        except Exception as e:
            logger.critical(msg=f"Unable to acquire RedisConnection from {self._name}")
            logger.exception(e)
        else:
            _redis = Redis(_redis_connection)
            yield _redis
            self._redis_pool.connection.release(_redis_connection)
            del _redis

    async def close_connection_pool(self) -> None:
        if self._redis_pool is not None:
            self._redis_pool.close()
            await self._redis_pool.wait_closed()
            
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

from asyncio.tasks import Task
from fastapi import WebSocket
from typing import Dict, List, Union
import logging
import datetime
import asyncio

from application.cache import Cache
from application.service.device.model import Application


logger = logging.getLogger(__package__)

class ConnectionManager:
    """
    Connection Manager is responsible to manage and store reference of device's connection
    """

    PREFIX_KEY_DEVICE = "device_connected:"
    PREFIX_KEY_APPLICATION = "application_instance:"

    # DEVICE Set TTL in Seconds
    DEVICE_CONNECTION_REGISTER_TTL = 60
    # APPLICATION Set TTL in Seconds
    APPLICATION_CONNECTION_REGISTER_TTL = 30
    # Delta TTL in Seconds for Re-declaration
    DELTA_TTL =1 

    cache: Cache
    application_instance_name: str
    refresh_want_running: bool = False
    refresh_task = None

    local_device_store: Dict[str, WebSocket]

    def __init__(self, cache: Cache, application_instance_name: str) -> None:
        self.accept_connection = True
        self.cache = cache
        self.application_instance_name = application_instance_name
        self.local_device_store = dict()
        self.refresh_want_running = False

    async def _refresh_application_registration(self):
        while self.refresh_want_running:
            await asyncio.sleep(self.APPLICATION_CONNECTION_REGISTER_TTL - self.DELTA_TTL)
            logger.info("Refresh Registration")
            await self.register_application(launch_refresh_task=False)

    async def register_application(self, launch_refresh_task: bool = True) -> bool:
        """
        Register the Application
        """
        # TODO : Put the Instance Name to Redis
        try:
            async with self.cache.acquire() as _connection:
                if _connection is not None:
                    await _connection.set(
                        key=f"{self.PREFIX_KEY_APPLICATION}{self.application_instance_name}",
                        value=datetime.datetime.utcnow().timestamp(),
                        expire=self.APPLICATION_CONNECTION_REGISTER_TTL
                    )
                else:
                    return False
        except RuntimeError as e:
            return False
        else:
            if launch_refresh_task:
                self.refresh_want_running = True
                self.refresh_task = asyncio.ensure_future(self._refresh_application_registration())
            
            return True

    async def unregister_application(self) -> None:
        """
        Unregister the Application
        """
        # TODO : Remove the Instance Name from Redis
        # TODO : How manage the crash of application ? (liveness probing)
        async with self.cache.acquire() as _connection:
            if _connection is not None:
                await _connection.delete(
                    key=f"{self.PREFIX_KEY_APPLICATION}{self.application_instance_name}"
                )
                self.refresh_want_running = False
                await self.refresh_task
            else:
                logger.critical("Unable to acquire connection from pool")

    async def get_application_list(self) -> Union[List[str], None]:
        """
        Get Application
        """
        _application_list = list()
        async with self.cache.acquire() as _connection:
            if _connection is not None:
                _list = await _connection.keys(f"{self.PREFIX_KEY_APPLICATION}*")
                for _key in _list:
                    logger.debug(_key)
                    _utc_timestamp = await _connection.get(
                        key=_key
                    )
                    _application = Application(
                        name=str(_key).replace(self.PREFIX_KEY_APPLICATION, ""),
                        last_register=_utc_timestamp
                    )
                    _application_list.append(_application)
            else:
                logger.critical("Unable to acquire connection from pool")
                return None
        
        return _application_list
                

    def _get_device_key(self, device_id: str) -> str:
        """
        Format Device Key for Redis.

        Returns:
            String representing the Key in Redis for a device.
        """
        return f"{self.PREFIX_KEY_DEVICE}{device_id}"

    async def register_connection(self, websocket: WebSocket, device_id: str) -> bool:
        """
        Register Connection for Device Connected to this specific instance.

        Returns:
            Success Execution
        """
        try:
            async with self.cache.acquire() as _connection:
                if _connection is not None:
                    await _connection.set(
                        key=self._get_device_key(device_id=device_id), 
                        value=self.application_instance_name
                    )
                    self.local_device_store[device_id] = websocket
                else:
                    logger.critical("Unable to acquire connection from pool")
                    return False
        except RuntimeError as e:
            logger.exception(e)
            return False
        else:
            return True

    async def unregister_connection(self, websocket: WebSocket, device_id: str) -> bool:
        """
        Unregister Connection for Device Connected to this specific instance
        Returns:
            Success Execution
        """
        try:
            if self.local_device_store.get(device_id, None) is not None:
                del self.local_device_store[device_id]
                async with self.cache.acquire() as _connection:
                    if _connection is not None:
                        await _connection.delete(key=self._get_device_key(device_id=device_id))
                    else:
                        logger.critical("Unable to acquire connection from the pool")
                        return False
        except RuntimeError as e:
            logger.exception(e)
            return False
        else:
            return True

    async def get_device_connected(self) -> List[str]:
        """
        Get device connected to this instance
        Returns:
            List of string representing the device_id
        """

        _device_id_list = list()
        for _device_id, _ in self.local_device_store.items():
            _device_id_list.append(_device_id)

        return _device_id_list

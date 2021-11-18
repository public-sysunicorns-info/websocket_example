from fastapi import WebSocket
from typing import Dict
import logging

from application.cache import Cache


logger = logging.getLogger(__package__)

class ConnectionManager:
    """
    Connection Manager is responsible to manage and store reference of device's connection
    """

    PREFIX_KEY_DEVICE = "device_connected:"

    cache: Cache
    application_instance_name: str

    local_device_store: Dict[str, WebSocket]

    def __init__(self, cache: Cache, application_instance_name: str) -> None:
        self.accept_connection = True
        self.cache = cache
        self.application_instance_name = application_instance_name
        self.local_device_store = dict()

    async def register_application(self) -> None:
        """
        Register the Application
        """
        # TODO : Put the Instance Name to Redis
        pass

    async def unregister_application(self) -> None:
        """
        Unregister the Application
        """
        # TODO : Remove the Instance Name from Redis
        # TODO : How manage the crash of application ? (liveness probing)
        pass

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
            async with self.cache.acquire() as _cache_connection:
                await _cache_connection.set(
                    key=self._get_device_key(device_id=device_id), 
                    value=self.application_instance_name
                )
            self.local_device_store[device_id] = websocket
        except RuntimeError as e:
            logger.exception(e)
            return False
        else:
            return True

    async def unregister_connection(self, websocket: WebSocket, device_id: str):
        """
        Unregister Connection for Device Connected to this specific instance
        """
        if self.local_device_store.get(device_id, None) is not None:
            del self.local_device_store[device_id]
            async with self.cache.acquire() as _cache_connection:
                await _cache_connection.delete(key=self._get_device_key(device_id=device_id))

from fastapi import WebSocket
from typing import Dict
from asyncio import gather

from application.cache import Cache


class ConnectionManager:

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
        pass

    async def unregister_application(self) -> None:
        pass

    def _get_device_key(self, device_id: str):
        return f"{self.PREFIX_KEY_DEVICE}{device_id}"

    async def register_connection(self, websocket: WebSocket, device_id: str):
        async with self.cache.acquire() as _cache_connection:
            await _cache_connection.set(
                key=self._get_device_key(device_id=device_id), 
                value=self.application_instance_name
            )
        self.local_device_store[device_id] = websocket

    async def unregister_connection(self, websocket: WebSocket, device_id: str):
        if self.local_device_store.get(device_id, None) is not None:
            del self.local_device_store[device_id]
            async with self.cache.acquire() as _cache_connection:
                await _cache_connection.delete(key=self._get_device_key(device_id=device_id))

from typing import Dict, Tuple, Union
from fastapi import WebSocket

from application.cache import Cache
from .model import Device

from .connection_manager import ConnectionManager

__all__ = (
    "DeviceService",
    "ConnectionManager"
)

class DeviceService:

    device_store: Dict[str, Device]

    device_secret: Dict[str, str]

    cache: Cache
    connection_manager: ConnectionManager

    def __init__(self, cache: Cache, connection_manager: ConnectionManager) -> None:

        self.cache = cache
        self.connection_manager = connection_manager

        # Init Device Store for POC
        self.device_store = {
            "device_01": Device(device_id="device_01"),
            "device_02": Device(device_id="device_02"),
            "device_03": Device(device_id="device_03"),
            "device_04": Device(device_id="device_04"),
            "device_05": Device(device_id="device_05")
        }
        # Init Device Secret for POC
        self.device_secret = {
            "NkBBRDdxZnkhMQ": "device_01",
            "eWJGMiZtMjloMg": "device_02",
            "SEAzQDYyN1l5Mw": "device_03",
            "MyohQXozaFMkNA": "device_04",
            "UjdRc3hkIyM5NQ": "device_05"
        }

    async def authenticate_device(self, device_api_key: str) -> Tuple[bool, Union[Device, None]]:
        _device_id = self.device_secret.get(device_api_key, None)
        if _device_id is None:
            return False, None
        else:
            return True, self.device_store.get(_device_id, None)

    async def connect_device(self, device: Device, websocket: WebSocket) -> bool:
        await self.connection_manager.register_connection(websocket=websocket, device_id=device.device_id)

    async def get_device_by_websocket(self, websocket: WebSocket) -> Union[Device, None]:
        pass

    async def get_websocket_by_device(self, device: Device) -> Tuple[bool, Union[WebSocket, None]]:
        pass

    async def disconnect_device(self, device: Device, websocket: WebSocket) -> bool:
        await self.connection_manager.unregister_connection(websocket=websocket, device_id=device.device_id)

    async def disconnect_device_by_websocket(self, websocket: WebSocket) -> bool:
        _device = self.get_device_by_websocket(websocket=websocket)
        if _device is not None:
            return self.disconnect_device(device=_device, websocket=websocket)
        else:
            return False

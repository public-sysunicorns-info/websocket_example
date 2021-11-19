from typing import Dict, Tuple, Union, List
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

        # TODO : Create Device Store

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
        """
        Return True, False for the authentication and return Device object correspondingg
        """
        _device_id = self.device_secret.get(device_api_key, None)
        if _device_id is None:
            return False, None
        else:
            return True, self.device_store.get(_device_id, None)

    async def connect_device(self, device: Device, websocket: WebSocket) -> bool:
        """
        Handle connection of the device and rely to the conenction manager
        """
        return await self.connection_manager.register_connection(websocket=websocket, device_id=device.device_id)

    async def send_event(device: Device, message: str) -> bool:
        """
        Send event to the device
        Detect if device is connected to this instance or rely on another or disconnected
        """
        # TODO : Detect if and where the device is connected 
        # TODO : Put the message in the instance of the device
        # TODO : Create the worker part that listen for message to be send.
        return False

    async def get_device_by_device_id(self, device_id: str) -> Union[Device, None]:
        """
        Return Device Object from the device store
        """
        return self.device_store.get(device_id, default=None)

    async def _get_websocket_by_device(self, device: Device) -> Tuple[bool, Union[WebSocket, None]]:
        """
        Internal function to retrieve websocket connection of the device
        """
        _wesocket = await self.connection_manager.get_websocket_by_device(device=device)

    async def disconnect_device(self, device: Device, websocket: WebSocket) -> bool:
        """
        Handle device disconnection for device link to this instance.
        Returns:
            Success Execution
        """
        return await self.connection_manager.unregister_connection(websocket=websocket, device_id=device.device_id)

    async def get_device_connected(self, instance_only: bool = False) -> List[Device]:
        """
        Return Device Connected globally or on this instance
        Returns:
            Return List of Device
        """
        if instance_only:
            _device_list = list()
            for _device_id in await self.connection_manager.get_device_connected():
                _device_list.append(Device(device_id=_device_id))
            return _device_list
        else:
            
            return list()

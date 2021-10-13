from fastapi import WebSocket, Depends, APIRouter
from dependency_injector.wiring import inject, Provide
from starlette.websockets import WebSocketDisconnect
from application import api
from application.container import ApplicationContainer
import logging

from application.service.device import DeviceService

logger = logging.getLogger(__package__)

ws_router_device = APIRouter()

@ws_router_device.websocket(
    "/ws/devices/{api_key}"
)
@inject
async def websocket_device_endpoint(
    websocket: WebSocket, 
    api_key: str,
    device_service: DeviceService = Depends(Provide[ApplicationContainer.device_service])
):
    print(device_service)
    _authenticated, _device = await device_service.authenticate_device(device_api_key=api_key)

    if _authenticated:
        await websocket.accept()
        _connected = await device_service.connect_device(device=_device, websocket=websocket)
        logger.info(f"{_device=} {api_key=} Connected")
        await websocket.send_json({"device_id": _device.device_id})
        try:
            while True:
                data = await websocket.receive_json()
                print(data)
        except WebSocketDisconnect as e:
            await device_service.disconnect_device(device=_device, websocket=websocket)
        except RuntimeError as e:
            await device_service.disconnect_device(device=_device, websocket=websocket)
    else:
        await websocket.close()
        logger.info(f"{api_key=} Force Disconnected")

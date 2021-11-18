from fastapi import WebSocket, Depends, APIRouter
from dependency_injector.wiring import inject, Provide
from starlette.websockets import WebSocketDisconnect
import logging

from application.container import ApplicationContainer
from application.service.device import DeviceService


# Instanciate Logger
logger = logging.getLogger(__package__)

# Instanciate Router for FastAPI
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
    """
    Websocket Endpoint that take api_key as path params and handle the device connection
    """
    # Authenticate the device base on api_key
    _authenticated, _device = await device_service.authenticate_device(device_api_key=api_key)

    if _authenticated:
        # Handshake the connection of websocket if authentication success
        await websocket.accept()

        # Register the connection of the device
        _connected = await device_service.connect_device(device=_device, websocket=websocket)
        logger.info(f"{_device=} {api_key=} Connected")

        # Send hello payload
        # TODO : Issue #14 - Create better hello payload with more information for the device 
        # ( https://github.com/public-sysunicorns-info/websocket_example/issues/14 )
        await websocket.send_json({"device_id": _device.device_id})
        
        # Loop to wait reception of message from the device
        try:
            while True:
                data = await websocket.receive_json()
                logger.debug(f"{_device.device_id=} {data=}")
        except WebSocketDisconnect as e:
            # Websocket disconnect from the device or path
            await device_service.disconnect_device(device=_device, websocket=websocket)
        except RuntimeError as e:
            # Unattented Runtime Error trigger device connection to force establisment of a new connection
            await device_service.disconnect_device(device=_device, websocket=websocket)
            logger.exception(e)
    else:
        # Close the connection due to authentication failed
        await websocket.close()
        logger.info(f"Disconnected by authentication failed {api_key=}")

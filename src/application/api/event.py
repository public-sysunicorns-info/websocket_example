from fastapi import Depends, APIRouter, Response
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject
from http import HTTPStatus

from pydantic.networks import HttpUrl

from application.container import ApplicationContainer
from application.service.device import DeviceService
from .model.event import EventStatus, EventModelResponse
from .model import ErrorResponseModel

event_api_router = APIRouter()

@event_api_router.post(
    path="/device/{device_id}/event",
    tags=["device","event"],
    summary="Create Event for a dedicated Device",
    description="",
    responses={
        HTTPStatus.OK.value: {"model": EventModelResponse},
        HTTPStatus.NOT_FOUND.value: {"model": ErrorResponseModel},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"model": ErrorResponseModel}
    }
)
@inject
async def post_event_to_device(
    response: Response,
    device_id: str,
    device_service: DeviceService = Depends(Provide[ApplicationContainer.device_service])
):
    _device = device_service.get_device_by_device_id(device_id=device_id)

    if _device is None:
        response.status_code = HTTPStatus.NOT_FOUND.value
        return ErrorResponseModel()
    else:
        if await device_service.send_event(device=_device, message="Force"):
            _status = EventStatus.OK
        else:
            _status = EventStatus.ERROR

        response.status_code = HTTPStatus.OK.value
        return EventModelResponse(
            device=_device,
            event_status=_status
        )


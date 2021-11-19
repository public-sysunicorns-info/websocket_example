from fastapi import Depends, APIRouter, Response
from dependency_injector.wiring import Provide, inject
from http import HTTPStatus
import logging
from application.api.model import ErrorResponseModel
from application.api.model.device import DeviceListModel

from application.container import ApplicationContainer
from application.service.device import DeviceService


logger = logging.getLogger(__package__)
device_api_router = APIRouter()


@device_api_router.post(
    path="/device/connected/instance",
    tags=["device"],
    summary="Return the list of device connected to this instance",
    description="",
    responses={
        HTTPStatus.OK.value: {"model": None},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"model": None}
    }
)
@inject
async def get_device_instance_connected(
    response: Response,
    device_service: DeviceService = Depends(Provide[ApplicationContainer.device_service])
):
    _device_list = await device_service.get_device_connected(instance_only=True)
    return DeviceListModel(
        devices=_device_list
    )


@device_api_router.post(
    path="/device/connected",
    tags=["device"],
    summary="Return the list of device connected to all instance",
    description="",
    responses={
        HTTPStatus.OK.value: {"model": DeviceListModel},
        HTTPStatus.INTERNAL_SERVER_ERROR.value: {"model": ErrorResponseModel}
    }
)
@inject
async def get_device_connected(
    response: Response,
    device_service: DeviceService = Depends(Provide[ApplicationContainer.device_service])
):
    _device_list = await device_service.get_device_connected(instance_only=False)
    return DeviceListModel(
        devices=_device_list
    )

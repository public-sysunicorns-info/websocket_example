from fastapi import APIRouter, Response, Depends
from dependency_injector.wiring import Provide, inject


from application.container import ApplicationContainer
from application.service import device
from application.service.device import DeviceService
from .model.application import ApplicationListResponse

application_api_router = APIRouter()

@application_api_router.get(
    path="/application",
    summary="",
    description=""
)
@inject
async def get_application_instance_list(
    response: Response,
    device_service: DeviceService = Depends(Provide[ApplicationContainer.device_service])
):
    return ApplicationListResponse(application_list=await device_service.get_application_list())

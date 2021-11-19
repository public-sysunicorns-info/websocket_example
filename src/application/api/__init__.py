from fastapi import APIRouter

from .health import router_api_health
from .event import event_api_router
from .device import device_api_router

API_PREFIX="/api"

api_router = APIRouter(
    prefix=API_PREFIX
)

api_router.include_router(router=router_api_health)
api_router.include_router(router=event_api_router)
api_router.include_router(router=device_api_router)

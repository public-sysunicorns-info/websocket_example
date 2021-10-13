from fastapi import APIRouter

from .health import router_api_health

API_PREFIX="/api"

api_router = APIRouter(
    prefix=API_PREFIX
)

api_router.include_router(router=router_api_health)

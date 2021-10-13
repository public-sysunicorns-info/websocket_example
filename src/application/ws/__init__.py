from fastapi import APIRouter
from .device import ws_router_device

ws_router = APIRouter()

ws_router.include_router(ws_router_device)

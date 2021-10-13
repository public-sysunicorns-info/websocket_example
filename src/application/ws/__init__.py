from fastapi import APIRouter

API_PREFIX="/ws"

api_router = APIRouter(
    prefix=API_PREFIX
)

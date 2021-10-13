from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from fastapi.responses import Response
from http import HTTPStatus
from pydantic import BaseModel, Field

from application.service.health import HealthService
from application.container import ApplicationContainer
from .model.health import HealthModel, LivenessModel, ReadinessModel, HealthDependenciesModel
from  application.version import get_version

router_api_health = APIRouter()

@router_api_health.get(
    path="/health",
    tags=["health"],
    description="",
    response_model=HealthModel,
    responses={
        HTTPStatus.OK.value: {"model": HealthModel},
        HTTPStatus.NOT_FOUND.value: {"model": HealthModel}
    }
)
@inject
async def api_health(
    response: Response,
    health_service: HealthService = Depends(Provide[ApplicationContainer.health_service])
):
    _health_model = HealthModel(
        health=health_service.health,
        liveness=health_service.liveness,
        readiness=health_service.readiness,
        version=get_version(False),
        version_long=get_version(True),
        dependencies=HealthDependenciesModel(
            cache_health=health_service.cache_health
        )
    )
    
    if health_service.health:
        response.status_code = HTTPStatus.OK
    else:
        response.status_code = HTTPStatus.NOT_FOUND
    
    return _health_model


@router_api_health.get(
    path="/health/liveness",
    tags=["health"],
    description="",
    response_model=LivenessModel,
    responses={
        HTTPStatus.OK.value: {"model": LivenessModel},
        HTTPStatus.NOT_FOUND.value: {"model": LivenessModel}
    }
)
@inject
async def api_health_liveness(
    response: Response,
    health_service: HealthService = Depends(Provide[ApplicationContainer.health_service])
):
    _liveness_model = LivenessModel(liveness=health_service.liveness)

    if health_service.liveness:
        response.status_code = HTTPStatus.OK
    else:
        response.status_code = HTTPStatus.NOT_FOUND
    
    return _liveness_model

@router_api_health.get(
    path="/health/readiness",
    tags=["health"],
    description="",
    response_model=ReadinessModel,
    responses={
        HTTPStatus.OK.value: {"model": ReadinessModel},
        HTTPStatus.NOT_FOUND.value: {"model": ReadinessModel}
    }
)
@inject
async def api_health_readiness(
    response: Response,
    health_service: HealthService = Depends(Provide[ApplicationContainer.health_service])
):
    _readiness_model = ReadinessModel(readiness=health_service.readiness)

    if health_service.readiness:
        response.status_code = HTTPStatus.OK
    else:
        response.status_code = HTTPStatus.NOT_FOUND

    return _readiness_model

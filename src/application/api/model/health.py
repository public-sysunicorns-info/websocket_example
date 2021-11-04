from pydantic import BaseModel, Field

from application.config.kube import KubeConfigModel


class HealthDependenciesModel(BaseModel):
    cache_health: bool = Field(description="")

class HealthModel(BaseModel):
    name: str = Field(description="Application Instance Name")
    health: bool = Field(description="Health of the Application")
    liveness: bool = Field(description="Liveness of the Application")
    readiness: bool = Field(description="Readiness of the Application")
    version: str = Field(description="Version of the Application")
    version_long: str = Field(description="Version with Commit of the Application")
    dependencies: HealthDependenciesModel = Field(description="")
    kube_config: KubeConfigModel

class LivenessModel(BaseModel):
    liveness: bool

class ReadinessModel(BaseModel):
    readiness: bool

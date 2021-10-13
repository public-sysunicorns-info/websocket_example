from pydantic import BaseModel, Field


class HealthDependenciesModel(BaseModel):
    cache_health: bool = Field(description="")

class HealthModel(BaseModel):
    health: bool = Field(description="Health of the Application")
    liveness: bool = Field(description="Liveness of the Application")
    readiness: bool = Field(description="Readiness of the Application")
    version: str = Field(description="Version of the Application")
    version_long: str = Field(description="Version with Commit of the Application")
    dependencies: HealthDependenciesModel = Field(description="")

class LivenessModel(BaseModel):
    liveness: bool

class ReadinessModel(BaseModel):
    readiness: bool

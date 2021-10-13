# 
import uuid
from pydantic import BaseSettings, Field

# 
from .uvicorn import UvicornConfigModel
from .logging import LoggingConfigModel
from .ssl import SSLConfig
from ..version import get_version

class ApplicationConfigModel(BaseSettings):
    application_name: str = Field(env="APPLICATION_NAME", default="fastapi")
    application_description: str = Field(env="APPLICATION_DESCRIPTION", default="")
    application_version: str = Field(env="APPLICATION_VERSION", default=get_version(full=False))
    server_host: str = Field(env="SERVER_HOST", default="0.0.0.0")
    server_port: int = Field(env="SERVER_PORT", default=8080)
    uvicorn_config = UvicornConfigModel()
    ssl_config = SSLConfig()
    logging_config = LoggingConfigModel()


def application_config_factory() -> ApplicationConfigModel:
    # Introduce to inject more programatic
    return ApplicationConfigModel()

def application_instance_name(application_config: ApplicationConfigModel) -> str:
    return f"{application_config.application_name}-{str(uuid.uuid4())[0:8]}"

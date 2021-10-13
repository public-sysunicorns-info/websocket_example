
from dependency_injector import providers, containers

from .config.redis import RedisConfig
from .config import ApplicationConfigModel, application_config_factory, application_instance_name

from .cache import Cache

from .service.health import HealthService


class ApplicationContainer(containers.DeclarativeContainer):

    # Config
    application_config: providers.Singleton[ApplicationConfigModel] = providers.Singleton(application_config_factory)
    application_instance_name: providers.Singleton[str] = providers.Singleton(application_instance_name, application_config=application_config)

    redis_config: providers.Singleton[RedisConfig] = providers.Singleton(RedisConfig)

    # Technical
    health_service: providers.Singleton[HealthService] = providers.Singleton(
        HealthService
    )
    cache: providers.Singleton[Cache] = providers.Singleton(
        Cache,
        redis_config=redis_config,
        application_instance_name=application_instance_name,
        health_service=health_service
    )
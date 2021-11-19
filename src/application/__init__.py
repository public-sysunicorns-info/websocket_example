from fastapi import FastAPI
from starlette.types import Receive, Scope, Send
from asyncio import gather
import logging


from application.container import ApplicationContainer
from .api import api_router
from .ws import ws_router
from application import api

logger = logging.getLogger(__package__)


class Application:

    container: ApplicationContainer = ApplicationContainer()
    fastapi: FastAPI = None

    def __init__(self) -> None:
        
        # Init Dependency Injection
        self.container.wire(packages=[api, ws])
        
        # Grab FastAPI
        self.fastapi = FastAPI(
            title=self.container.application_config().application_name,
            description=self.container.application_config().application_description,
            version=self.container.application_config().application_version
        )

        # Include Router add api
        self.fastapi.include_router(router=api_router)
        self.fastapi.include_router(router=ws_router)

        # Register handler
        self.fastapi.add_event_handler(event_type="startup", func=self.on_init)
        self.fastapi.add_event_handler(event_type="shutdown", func=self.on_close)

    async def on_init(self) -> None:
        # Technical Resource initialization
        await gather(
            self.container.cache().init_connection_pool()
        )
        # Need previous initialization before launch
        await gather(
            self.container.device_connection_manager().register_application()
        )

        logger.debug(self.container.kube_config())

    async def on_close(self) -> None:
        await gather(
            self.container.cache().close_connection_pool()
        )
        await gather(
            self.container.device_connection_manager().unregister_application()
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        return await self.fastapi.__call__(scope=scope, receive=receive, send=send)

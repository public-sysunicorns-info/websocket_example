from fastapi import FastAPI
from starlette.types import Receive, Scope, Send
from asyncio import gather


from application.container import ApplicationContainer
from .api import api_router
from application import api

class Application:

    container: ApplicationContainer = ApplicationContainer()
    fastapi: FastAPI = None

    def __init__(self) -> None:
        
        # Init Dependency Injection
        self.container.wire(packages=[api])
        
        # Grab FastAPI
        self.fastapi = FastAPI(
            title=self.container.application_config().application_name,
            description=self.container.application_config().application_description,
            version=self.container.application_config().application_version
        )

        # Include Router add api
        self.fastapi.include_router(router=api_router)

        # Register handler
        self.fastapi.add_event_handler(event_type="startup", func=self.on_init)
        self.fastapi.add_event_handler(event_type="shutdown", func=self.on_close)

    async def on_init(self) -> None:
        await gather(
            self.container.cache().init_connection_pool()
        )

    async def on_close(self) -> None:
        await gather(
            self.container.cache().close_connection_pool()
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        return await self.fastapi.__call__(scope=scope, receive=receive, send=send)

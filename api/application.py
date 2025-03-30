"""Application initialization and configuration."""

import fastapi

import contextlib
import typing

import fastapi
from that_depends.providers import DIContextMiddleware

from api.ioc import IOCContainer
from api.middleware import catch_exceptions_middleware
from api.adapters.http import health


@contextlib.asynccontextmanager
async def lifespan(_: typing.Any) -> typing.AsyncIterator[None]:  # noqa: ANN401
    await IOCContainer.init_resources()
    try:
        yield
    finally:
        await IOCContainer.tear_down()


APP: fastapi.FastAPI = fastapi.FastAPI(lifespan=lifespan)

APP.middleware("http")(catch_exceptions_middleware)
APP.add_middleware(DIContextMiddleware)

# Include your routers here
APP.include_router(health.ROUTER, tags=["SERVICE"])

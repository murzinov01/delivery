"""Application initialization and configuration."""

import contextlib
import typing

import fastapi
from that_depends.providers import DIContextMiddleware

from api.adapters.http import health, delivery
from api.ioc import IOCContainer
from api.middleware import catch_exceptions_middleware


@contextlib.asynccontextmanager
async def lifespan(_: typing.Any) -> typing.AsyncIterator[None]:  # noqa: ANN401
    await IOCContainer.init_resources()
    try:
        yield
    finally:
        await IOCContainer.tear_down()


APP: fastapi.FastAPI = fastapi.FastAPI(
    lifespan=lifespan,
    version="1.0.0",
    title="Swagger Delivery",
    description="Отвечает за учет курьеров, деспетчеризацию доставкуов, доставку",
)

APP.add_middleware(DIContextMiddleware)

# Include your routers here
APP.include_router(health.ROUTER, tags=["SERVICE"])
APP.include_router(delivery.ROUTER, tags=["DELIVERY"])

"""Application initialization and configuration."""

import contextlib
import typing

import fastapi
from api.adapters.background_jobs.scheduler import start_async_scheduler
from api.adapters.http import delivery, health
from api.ioc import IOCContainer
from fastapi.middleware.cors import CORSMiddleware
from that_depends.providers import DIContextMiddleware


if typing.TYPE_CHECKING:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler


@contextlib.asynccontextmanager
async def lifespan(_: typing.Any) -> typing.AsyncIterator[None]:  # noqa: ANN401
    # Init resources
    await IOCContainer.init_resources()

    # Start async sheduler process
    async_sheduler: AsyncIOScheduler = await start_async_scheduler()

    yield

    # Shutdown async sheduler process
    async_sheduler.shutdown()

    # Clean up resources
    await IOCContainer.tear_down()


APP: fastapi.FastAPI = fastapi.FastAPI(
    lifespan=lifespan,
    version="1.0.0",
    title="Swagger Delivery",
    description="Отвечает за учет курьеров, деспетчеризацию доставкуов, доставку",
)


APP.add_middleware(DIContextMiddleware)
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include your routers here
APP.include_router(health.ROUTER, tags=["SERVICE"])
APP.include_router(delivery.ROUTER, tags=["DELIVERY"])

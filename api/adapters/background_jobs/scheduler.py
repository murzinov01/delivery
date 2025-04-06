"""Scheduler jobs configuration."""

from api.adapters.background_jobs.assign_orders_job import assign_orders_job
from api.adapters.background_jobs.move_couriers_job import move_couriers_job
from api.settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger


async def start_async_scheduler() -> AsyncIOScheduler:
    logger.info("Start async scheduler process.")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        assign_orders_job,
        trigger=IntervalTrigger(seconds=settings.jobs.assign_orders_run_every_sec),
        id=settings.jobs.assign_orders_job_id,
        max_instances=1,
    )
    scheduler.add_job(
        move_couriers_job,
        trigger=IntervalTrigger(seconds=settings.jobs.move_couriers_run_every_sec),
        id=settings.jobs.move_couriers_job_id,
        max_instances=1,
    )

    scheduler.start()
    logger.info("Async scheduler successfully started.")
    return scheduler

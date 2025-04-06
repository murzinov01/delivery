"""Move couriers job."""

from api.ioc import IOCContainer
from loguru import logger
from that_depends import Provide, inject

from core.application.use_cases.commands.move_couriers.command import MoveCouriersCommand
from core.application.use_cases.commands.move_couriers.handler import MoveCouriersHandler


@inject
async def move_couriers_job(
    couriers_handler: MoveCouriersHandler = Provide[IOCContainer.move_couriers_handler],
) -> None:
    move_couriers_command = MoveCouriersCommand()
    try:
        await couriers_handler.handle(move_couriers_command)
    except MoveCouriersHandler.NoAssignedOrdersError as exc:
        logger.info(exc)

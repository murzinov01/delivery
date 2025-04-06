"""Assign orders job."""

from api.ioc import IOCContainer
from loguru import logger
from that_depends import Provide, inject

from core.application.use_cases.commands.assign_order.command import AssignOrderCommand
from core.application.use_cases.commands.assign_order.handler import AssignOrderHandler


@inject
async def assign_orders_job(orders_handler: AssignOrderHandler = Provide[IOCContainer.assign_order_handler]) -> None:
    assign_orders_command = AssignOrderCommand()

    try:
        await orders_handler.handle(assign_orders_command)
    except AssignOrderHandler.NoAvailableCouriersError as error:
        logger.info(error)
    except AssignOrderHandler.NoOrderToProcessError as error:
        logger.info(error)

"""Assign order command handler."""

from typing import TYPE_CHECKING

from core.application.use_cases.commands.assign_order.command import AssignOrderCommand
from core.domain.services.dispatch_service import DispatchService
from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from loguru import logger


if TYPE_CHECKING:
    from core.domain.model.courier_aggregate.courier import Courier
    from core.domain.model.order_aggregate.order import Order


class AssignOrderHandler:

    class NoAvailableCouriersError(Exception):
        def __init__(self) -> None:
            super().__init__("There are no available couriers at the moment.")

    class NoOrderToProcessError(Exception):
        def __init__(self) -> None:
            super().__init__("There is no order to process.")

    def __init__(
        self,
        courier_repository: CourierRepository,
        order_repository: OrderRepository,
        unit_of_work: UnitOfWork,
        dispatch_service: DispatchService,
    ) -> None:
        self._courier_repository: CourierRepository = courier_repository
        self._order_repository: OrderRepository = order_repository
        self._unit_of_work: UnitOfWork = unit_of_work
        self._dispatch_service: DispatchService = dispatch_service

    async def handle(self, message: AssignOrderCommand) -> None:
        # Восстанавливаем аггрегаты
        free_couriers: list[Courier] = await self._courier_repository.fetch_all_in_free_status()
        order: Order | None = await self._order_repository.fetch_first_order_in_created_status()

        # Делаем проверки
        if len(free_couriers) == 0:
            raise self.NoAvailableCouriersError
        if order is None:
            raise self.NoOrderToProcessError

        # Распределяем заказ на одного из свободных курьеров
        courier: Courier = self._dispatch_service.dispatch(order, free_couriers)
        logger.info(f"Dispatch {order!r} to {courier!r}")

        # Сохраняем
        await self._courier_repository.update(courier)
        await self._unit_of_work.save_changes()

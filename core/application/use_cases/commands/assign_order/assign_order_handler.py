"""Assign order command handler."""

from core.application.use_cases.commands.assign_order.assign_order_command import AssignOrderCommand
from core.domain.services.dispatch_service import DispatchService
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.domain.model.order_aggregate.order import Order
    from core.domain.model.courier_aggregate.courier import Courier


class AssignOrderHandler:

    class NoAvailableCouriersError(Exception):
        def __init__(self) -> None:
            super().__init__("There are no available couriers at the moment.")

    class NoOrderToProcessError(Exception):
        def __init__(self) -> None:
            super().__init__("There is no order to process.")

    def __init__(self, unit_of_work: UnitOfWork, dispatch_service: DispatchService) -> None:
        self._unit_of_work: UnitOfWork = unit_of_work
        self._dispatch_service: DispatchService = dispatch_service

    async def handle(self, message: AssignOrderCommand) -> None:
        async with self._unit_of_work.start() as repository:
            # Восстанавливаем аггрегаты
            free_couriers: list[Courier] = await repository.courier.fetch_all_in_free_status()
            order: Order | None = await repository.order.fetch_first_order_in_created_status()

            # Делаем проверки
            if len(free_couriers) == 0:
                raise self.NoAvailableCouriersError
            if order is None:
                raise self.NoAvailableCouriersError

            # Распределяем заказ на одного из свободных курьеров
            courier: Courier = self._dispatch_service.dispatch(order, free_couriers)

            # Сохраняем
            await repository.courier.update(courier)

"""Move couriers command handler."""

from typing import TYPE_CHECKING

from core.application.use_cases.commands.move_couriers.command import MoveCouriersCommand
from core.domain.model.order_aggregate.order import Order
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository


if TYPE_CHECKING:
    from core.domain.model.courier_aggregate.courier import Courier


class MoveCouriersHandler:

    class NoAssignedOrdersError(Exception):
        def __init__(self) -> None:
            super().__init__("There are no assigned orders to process")

    class OrdersCourierNotFoundError(Exception):
        def __init__(self, order: Order) -> None:
            super().__init__(f"Courier with id {order.courier_id} of the {order=} not found.")

    def __init__(
        self, courier_repository: CourierRepository, order_repository: OrderRepository, unit_of_work: UnitOfWork,
    ) -> None:
        self._courier_repository: CourierRepository = courier_repository
        self._order_repository: OrderRepository = order_repository
        self._unit_of_work: UnitOfWork = unit_of_work

    async def handle(self, message: MoveCouriersCommand) -> None:
        # Восстанавливем аггрегаты
        assigned_orders: list[Order] = await self._order_repository.fetch_all_in_assigned_status()

        # Делаем проверки
        if len(assigned_orders) == 0:
            raise self.NoAssignedOrdersError

        for order in assigned_orders:
            if order.courier_id is None:
                raise TypeError

            # Восстанавливем курьера, назначенного на заказ
            courier: Courier = await self._courier_repository.fetch_courier_by_id(order.courier_id)
            if courier is None:
                raise self.OrdersCourierNotFoundError(order)

            # Перемещаем курьера
            courier.move(target_location=order.location)

            # Если курьер дошел до точки заказа - завершаем заказ, освобождаем курьера
            if order.location == courier.location:
                order.complete()
                courier.set_free()

            # Сохраняем
            await self._courier_repository.update(courier)
            await self._order_repository.update(order)
            await self._unit_of_work.save_changes()

"""Move couriers command handler."""

from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCouriersCommand
from core.domain.model.order_aggregate.order import Order
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.domain.model.courier_aggregate.courier import Courier


class MoveCouriersHandler:

    class NoAssignedOrdersError(Exception):
        def __init__(self) -> None:
            super().__init__("There are no assigned orders to process")

    class OrdersCourierNotFoundError(Exception):
        def __init__(self, order: Order) -> None:
            super().__init__(f"Courier with id {order.courier_id} of the {order=} not found.")

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work: UnitOfWork = unit_of_work

    async def handle(self, message: MoveCouriersCommand) -> None:
        async with self._unit_of_work.start() as repository:
            # Восстанавливем аггрегаты
            assigned_orders: list[Order] = await repository.order.fetch_all_in_assigned_status()

            # Делаем проверки
            if len(assigned_orders) == 0:
                raise self.NoAssignedOrdersError

            for order in assigned_orders:
                if order.courier_id is None:
                    raise TypeError

                # Восстанавливем курьера, назначенного на заказ
                courier: Courier = repository.courier.fetch_courier_by_id(order.courier_id)
                if courier is None:
                    raise self.OrdersCourierNotFoundError(order)

                # Перемещаем курьера
                courier.move(target_location=order.location)

                # Если курьер дошел до точки заказа - завершаем заказ, освобождаем курьера
                if order.location == courier.location:
                    order.complete()
                    courier.set_free()

                # Сохраняем
                await repository.courier.update(courier)
                await repository.order.update(order)

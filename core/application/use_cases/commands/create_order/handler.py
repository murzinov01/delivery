"""Create order command handler."""

from uuid import UUID

from core.application.use_cases.commands.create_order.command import CreateOrderCommand
from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


class CreateOrderHandler:

    class AlreadyCreatedOrderError(Exception):
        def __init__(self, basket_id: UUID) -> None:
            super().__init__(f"Order with {basket_id=} already created")

    def __init__(self, unit_of_work: UnitOfWork, order_repository: OrderRepository) -> None:
        self._unit_of_work: UnitOfWork = unit_of_work
        self._order_repository: OrderRepository = order_repository

    async def handle(self, message: CreateOrderCommand) -> None:
        # Проверяем на случай, когда заказ с таким basket_id уже существует
        if await self._order_repository.fetch_order_by_id(message.basket_id):
            raise self.AlreadyCreatedOrderError(message.basket_id)

        # Получаем геопозицию из Geo (пока ставим фэйковое значение)
        location = Location.random()

        # Создаем заказ
        order = Order(order_id=message.basket_id, location=location)

        # Сохраняем заказ
        await self._order_repository.add(order)
        await self._unit_of_work.save_changes()

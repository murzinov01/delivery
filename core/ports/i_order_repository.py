"""Order repository interface."""

from uuid import UUID
from typing import Protocol

from core.domain.model.order_aggregate.order import Order


class IOrderRepository(Protocol):

    async def add(self, order: Order) -> None:
        pass

    async def update(self, order: Order) -> None:
        pass

    async def fetch_by_order_id(self, order_id: UUID) -> Order | None:
        pass

    async def fetch_one_order_in_created_status(self) -> Order | None:
        pass

    async def fetch_all_in_assigned_status(self) -> list[Order]:
        pass

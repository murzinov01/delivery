"""Order Repository."""

from core.domain.model.order_aggregate.order import Order, OrderStatus
from infrastructure.adapters.postgres.repositories.base import BasePostgresRepository
import sqlalchemy as sa

from uuid import UUID


class OrderRepository(BasePostgresRepository):

    async def add(self, order: Order) -> None:
        self._session.add(order)

    async def update(self, order: Order) -> None:
        self._session.merge(order)

    async def fetch_by_order_id(self, order_id: UUID) -> Order | None:
        return await self._session.get(Order, order_id)

    async def fetch_one_order_in_created_status(self) -> Order | None:
        query_stmt = sa.select(Order).filter_by(status=OrderStatus.CREATED).limit(1)
        return (await self._session.execute(query_stmt)).scalar_one_or_none()

    async def fetch_all_in_assigned_status(self) -> list[Order]:
        query_stmt = sa.select(Order).filter_by(status=OrderStatus.ASSIGNED)
        return list((await self._session.execute(query_stmt)).scalars().all())

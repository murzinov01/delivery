"""Get incomplete orders query handler."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection

from core.application.use_cases.queries.get_incomplete_orders.query import (
    GetIncompleteOrdersQuery,
)
from core.application.use_cases.queries.get_incomplete_orders.response import OrderDTO
from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order_status import OrderStatus


if TYPE_CHECKING:
    from collections.abc import Sequence


class GetIncompleteOrdersHandler:

    def __init__(self, db_connection: AsyncConnection) -> None:
        self._db_connection: AsyncConnection = db_connection

    async def handle(self, message: GetIncompleteOrdersQuery) -> list[OrderDTO]:
        query: str = """
            SELECT id, location_x, location_y
            FROM public.orders
            WHERE status = :created_status OR status = :assigned_status
        """
        query_result: Sequence[sa.Row] = (
            await self._db_connection.execute(
                statement=sa.text(query),
                parameters={"created_status": OrderStatus.CREATED, "assigned_status": OrderStatus.ASSIGNED},
            )
        ).fetchall()
        return [OrderDTO(id=row.id, location={"x": row.location_x, "y": row.location_y}) for row in query_result]

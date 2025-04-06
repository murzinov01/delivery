"""Get busy couriers query handler."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection

from core.application.use_cases.queries.get_busy_couriers.query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_busy_couriers.response import CourierDTO
from core.domain.model.courier_aggregate.courier_status import CourierStatus


if TYPE_CHECKING:
    from collections.abc import Sequence


class GetBusyCouriersHandler:

    def __init__(self, db_connection: AsyncConnection) -> None:
        self._db_connection: AsyncConnection = db_connection

    async def handle(self, message: GetBusyCouriersQuery) -> list[CourierDTO]:
        query: str = """
            SELECT id, name, location_x, location_y, transport_id
            FROM public.couriers
            WHERE status = :target_status
        """
        query_result: Sequence[sa.Row] = (
            await self._db_connection.execute(
                statement=sa.text(query),
                parameters={"target_status": CourierStatus.BUSY},
            )
        ).fetchall()
        return [CourierDTO(**row._mapping) for row in query_result]  # noqa: SLF001

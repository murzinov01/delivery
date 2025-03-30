"""Courier Repository."""

from uuid import UUID

import sqlalchemy as sa
import sqlalchemy.orm as so

from core.domain.model.courier_aggregate.courier import Courier, CourierStatus
from infrastructure.adapters.postgres.repositories.base import BasePostgresRepository


class CourierRepository(BasePostgresRepository):

    async def add(self, courier: Courier) -> None:
        self._session.add(courier)

    async def update(self, courier: Courier) -> None:
        self._session.merge(courier)

    async def fetch_by_courier_id(self, courier_id: UUID) -> Courier | None:
        return await self._session.get(Courier, courier_id, options=[so.joinedload(Courier.transport)])

    async def fetch_all_in_free_status(self) -> list[Courier]:
        query_stmt = sa.select(Courier).filter_by(status=CourierStatus.FREE).options(so.joinedload(Courier.transport))
        return list((await self._session.execute(query_stmt)).scalars().all())

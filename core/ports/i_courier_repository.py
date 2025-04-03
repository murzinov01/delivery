"""Courier repository interface."""

from typing import Protocol
from uuid import UUID

from core.domain.model.courier_aggregate.courier import Courier


class ICourierRepository(Protocol):

    async def add(self, courier: Courier) -> None:
        pass

    async def update(self, courier: Courier) -> None:
        pass

    async def fetch_by_courier_id(self, courier_id: UUID) -> Courier | None:
        pass

    async def fetch_all_in_free_status(self) -> list[Courier]:
        pass

"""Unit of work pattern for making db changes via several repositories in one transaction."""

import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository


class UnitOfWork:

    def __init__(self, database_session: AsyncSession) -> None:
        self._database_session: typing.Final = database_session

        self.courier: typing.Final = CourierRepository(self._database_session)
        self.order: typing.Final = OrderRepository(self._database_session)

    @contextlib.asynccontextmanager
    async def start(self) -> typing.AsyncIterator[typing.Self]:
        try:
            yield self
        except Exception:
            await self._database_session.rollback()
            raise
        else:
            await self._database_session.commit()

    async def save_changes(self) -> None:
        await self._database_session.commit()

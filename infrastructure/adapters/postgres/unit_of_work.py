"""Unit of work pattern for making db changes via several repositories in one transaction."""

import typing

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:

    def __init__(self, database_session: AsyncSession) -> None:
        self.database_session: typing.Final = database_session

    async def save_changes(self) -> None:
        await self.database_session.commit()

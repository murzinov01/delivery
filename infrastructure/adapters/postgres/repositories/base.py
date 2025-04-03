"""Base class for all postgres repositories."""

from sqlalchemy.ext.asyncio import AsyncSession


class BasePostgresRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

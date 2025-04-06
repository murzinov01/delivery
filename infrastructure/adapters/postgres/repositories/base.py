"""Base class for all postgres repositories."""

from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from infrastructure.adapters.postgres.models import mapper_registry
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BasePostgresRepository:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._session: AsyncSession = unit_of_work.database_session

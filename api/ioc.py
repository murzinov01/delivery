"""Container with dependencies."""

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession
from that_depends import BaseContainer, ContextScopes, providers

from api.settings import settings
from core.ports.i_courier_repository import ICourierRepository
from core.ports.i_order_repository import IOrderRepository
from infrastructure.adapters.postgres.connection import (
    create_async_database_engine,
    create_async_db_connection,
    create_async_session,
)
from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


class IOCContainer(BaseContainer):
    default_scope = ContextScopes.ANY

    # ------------------------------------- Application resources -------------------------------------

    database_engine: AsyncEngine = providers.Resource(
        create_async_database_engine,
        database_dsn=settings.database.dsn,
        pool_min_size=settings.database.pool_min_size,
        pool_max_overflow_size=settings.database.pool_max_overflow_size,
        pool_pre_ping=settings.database.pool_pre_ping,
    )
    database_session: AsyncSession = providers.ContextResource(
        create_async_session,
        engine=database_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    database_connection: AsyncConnection = providers.ContextResource(create_async_db_connection, engine=database_engine)

    # ------------------------------------- DB repositories -------------------------------------
    order_repository: IOrderRepository = providers.Factory(OrderRepository, session=database_session)
    courier_repository: ICourierRepository = providers.Factory(CourierRepository, session=database_session)

    unit_of_work: UnitOfWork = providers.Factory(UnitOfWork, database_session=database_session)

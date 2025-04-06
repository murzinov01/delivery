"""Container with dependencies."""

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession
from that_depends import BaseContainer, ContextScopes, providers

from api.settings import settings
from core.application.use_cases.commands.assign_order.handler import AssignOrderHandler
from core.application.use_cases.commands.create_order.handler import CreateOrderHandler
from core.application.use_cases.commands.move_couriers.handler import MoveCouriersHandler
from core.application.use_cases.queries.get_busy_couriers.handler import GetBusyCouriersHandler
from core.application.use_cases.queries.get_incomplete_orders.handler import GetIncompleteOrdersHandler
from core.domain.services.dispatch_service import DispatchService
from core.domain.services.i_dispatch_service import IDispatchService
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
    unit_of_work: UnitOfWork = providers.Factory(UnitOfWork, database_session=database_session)

    # ------------------------------------- DB repositories -------------------------------------
    order_repository: IOrderRepository = providers.Factory(OrderRepository, unit_of_work=unit_of_work)
    courier_repository: ICourierRepository = providers.Factory(CourierRepository, unit_of_work=unit_of_work)

    # ------------------------------------- Domain Services -------------------------------------
    dispatch_service: IDispatchService = providers.Singleton(DispatchService)

    # ------------------------------------- Use Cases -------------------------------------
    create_order_handler: CreateOrderHandler = providers.Factory(
        CreateOrderHandler, order_repository=order_repository, unit_of_work=unit_of_work,
    )
    assign_order_handler: AssignOrderHandler = providers.Factory(
        AssignOrderHandler,
        order_repository=order_repository,
        courier_repository=courier_repository,
        unit_of_work=unit_of_work,
        dispatch_service=dispatch_service,
    )
    move_couriers_handler: MoveCouriersHandler = providers.Factory(
        MoveCouriersHandler,
        order_repository=order_repository,
        courier_repository=courier_repository,
        unit_of_work=unit_of_work,
    )
    get_busy_couriers_handler: GetBusyCouriersHandler = providers.Factory(
        GetBusyCouriersHandler,
        db_connection=database_connection,
    )
    get_incomplete_orders_handler: GetIncompleteOrdersHandler = providers.Factory(
        GetIncompleteOrdersHandler,
        db_connection=database_connection,
    )

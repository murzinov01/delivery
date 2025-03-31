import uuid

from assertpy import assert_that
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.order_aggregate.order import Order, OrderStatus
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.postgres.repositories.order_repository import OrderRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


class TestOrderRepository:

    async def test_add_order(self, test_db_session: AsyncSession):
        order = Order(order_id=uuid.uuid4(), location=Location(x=1, y=1))
        order_repository = OrderRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await order_repository.add(order)
        await unit_of_work.save_changes()

        order_from_db = await order_repository.fetch_order_by_id(order.id)

        assert_that(order_from_db).is_equal_to(order)

    async def test_update_order(self, test_db_session: AsyncSession):
        order = Order(order_id=uuid.uuid4(), location=Location(x=1, y=1))
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        order_repository = OrderRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await order_repository.add(order)
        await unit_of_work.save_changes()

        order.assign(courier)
        await order_repository.update(order)

        order_from_db = await order_repository.fetch_order_by_id(order.id)

        assert_that(order_from_db.status).is_equal_to(OrderStatus.ASSIGNED)
        assert_that(order_from_db.courier_id).is_equal_to(courier.id)

    async def test_fetch_order_by_id(self, test_db_session: AsyncSession):
        order = Order(order_id=uuid.uuid4(), location=Location(x=1, y=1))
        order_repository = OrderRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await order_repository.add(order)
        await unit_of_work.save_changes()

        order_from_db = await order_repository.fetch_order_by_id(order.id)

        assert_that(order_from_db).is_equal_to(order)

    async def test_fetch_first_order_in_created_status(self, test_db_session: AsyncSession):
        order_1 = Order(order_id=uuid.uuid4(), location=Location(x=1, y=1))
        order_2 = Order(order_id=uuid.uuid4(), location=Location(x=2, y=2))
        order_3 = Order(order_id=uuid.uuid4(), location=Location(x=3, y=3))

        order_repository = OrderRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await order_repository.add(order_1)
        await order_repository.add(order_2)
        await order_repository.add(order_3)
        await unit_of_work.save_changes()

        order_from_db = await order_repository.fetch_first_order_in_created_status()

        assert_that(order_from_db.status).is_equal_to(OrderStatus.CREATED)

    async def test_fetch_all_in_assigned_status(self, test_db_session: AsyncSession):
        order_1 = Order(order_id=uuid.uuid4(), location=Location(x=1, y=1))
        order_2 = Order(order_id=uuid.uuid4(), location=Location(x=2, y=2))
        order_3 = Order(order_id=uuid.uuid4(), location=Location(x=3, y=3))

        courier_1 = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_2 = Courier(name="Sasha", transport_name="Car", transport_speed=3, location=Location(x=2, y=2))

        order_repository = OrderRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        order_1.assign(courier_1)
        order_2.assign(courier_2)

        await order_repository.add(order_1)
        await order_repository.add(order_2)
        await order_repository.add(order_3)
        await unit_of_work.save_changes()

        orders: list[Order] = await order_repository.fetch_all_in_assigned_status()

        assert_that(len(orders)).is_equal_to(2)
        for order in orders:
            assert_that(order.status).is_equal_to(OrderStatus.ASSIGNED)

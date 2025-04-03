from assertpy import assert_that
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.model.courier_aggregate.courier import Courier, CourierStatus
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


class TestCourierRepository:

    async def test_add_courier(self, test_db_session: AsyncSession):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_repository = CourierRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await courier_repository.add(courier)
        await unit_of_work.save_changes()

        courier_from_db = await courier_repository.fetch_courier_by_id(courier.id)

        assert_that(courier_from_db).is_equal_to(courier)

    async def test_update_courier(self, test_db_session: AsyncSession):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_repository = CourierRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await courier_repository.add(courier)
        await unit_of_work.save_changes()

        courier.set_busy()
        await courier_repository.update(courier)
        await unit_of_work.save_changes()

        courier_from_db = await courier_repository.fetch_courier_by_id(courier.id)

        assert_that(courier_from_db.status).is_equal_to(CourierStatus.BUSY)

    async def test_fetch_courier_by_id(self, test_db_session: AsyncSession):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_repository = CourierRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await courier_repository.add(courier)
        await unit_of_work.save_changes()

        courier_from_db = await courier_repository.fetch_courier_by_id(courier.id)

        assert_that(courier_from_db).is_equal_to(courier)

    async def test_fetch_all_in_free_status(self, test_db_session: AsyncSession):
        courier_1 = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_2 = Courier(name="Sasha", transport_name="Car", transport_speed=3, location=Location(x=2, y=2))
        courier_3 = Courier(name="Vanya", transport_name="Foor", transport_speed=1, location=Location(x=3, y=3))

        courier_2.set_busy()

        courier_repository = CourierRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await courier_repository.add(courier_1)
        await courier_repository.add(courier_2)
        await courier_repository.add(courier_3)
        await unit_of_work.save_changes()

        free_couriers: list[Courier] = await courier_repository.fetch_all_in_free_status()

        assert_that(len(free_couriers)).is_equal_to(2)
        for courier in free_couriers:
            assert_that(courier.status).is_equal_to(CourierStatus.FREE)

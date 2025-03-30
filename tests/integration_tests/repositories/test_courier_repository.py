from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.adapters.postgres.repositories.courier_repository import CourierRepository
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.shared_kernel.location import Location

from assertpy import assert_that


class TestCourierRepository:

    async def test_add(self, test_db_session: AsyncSession):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier_repository = CourierRepository(test_db_session)
        unit_of_work = UnitOfWork(database_session=test_db_session)

        await courier_repository.add(courier)
        await unit_of_work.save_changes()

        courier_from_db = await courier_repository.fetch_by_courier_id(courier.id)

        assert_that(courier).is_equal_to(courier_from_db)

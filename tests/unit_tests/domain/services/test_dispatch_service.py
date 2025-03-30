from uuid import uuid4

import pytest
from assertpy import assert_that

from core.domain.model.courier_aggregate.courier import Courier, CourierStatus
from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location
from core.domain.services.dispatch_service import DispatchService


class TestDispatchService:

    @pytest.mark.parametrize(
        "order, couriers, expected_courier",
        [
            (
                Order(order_id=uuid4(), location=Location(x=1, y=1)),
                [
                    Courier(name="Вася", transport_name="Foot", transport_speed=1, location=Location(x=5, y=5)),
                    Courier(name="Петя", transport_name="Bicycle", transport_speed=2, location=Location(x=5, y=5)),
                    Courier(name="Саша", transport_name="Car", transport_speed=3, location=Location(x=5, y=5)),
                ],
                Courier(name="Саша", transport_name="Car", transport_speed=3, location=Location(x=5, y=5)),
            ),
            (
                Order(order_id=uuid4(), location=Location(x=1, y=1)),
                [
                    Courier(name="Вася", transport_name="Foot", transport_speed=1, location=Location(x=1, y=2)),
                    Courier(name="Петя", transport_name="Bicycle", transport_speed=2, location=Location(x=5, y=5)),
                    Courier(name="Саша", transport_name="Car", transport_speed=3, location=Location(x=5, y=5)),
                ],
                Courier(name="Вася", transport_name="Foot", transport_speed=1, location=Location(x=1, y=2)),
            ),
            (
                Order(order_id=uuid4(), location=Location(x=1, y=1)),
                [
                    Courier(name="Вася", transport_name="Foot", transport_speed=1, location=Location(x=5, y=5)),
                    Courier(name="Петя", transport_name="Bicycle", transport_speed=2, location=Location(x=5, y=5)),
                    Courier(name="Саша", transport_name="Car", transport_speed=3, location=Location(x=10, y=10)),
                ],
                Courier(name="Петя", transport_name="Bicycle", transport_speed=2, location=Location(x=5, y=5)),
            ),
        ],
    )
    def test_dispatch_when_params_is_correct(
        self,
        order: Order,
        couriers: list[Courier],
        expected_courier: Courier,
    ):

        courier: Courier = DispatchService.dispatch(order, couriers)

        assert_that(courier.name).is_equal_to(expected_courier.name)
        assert_that(courier.status).is_equal_to(CourierStatus.BUSY)
        assert_that(order.courier_id).is_equal_to(courier.id)

    def test_dispatch_when_order_is_none(self):
        order: Order = None
        couriers: list[Courier] = [
            Courier(name="Вася", transport_name="Foot", transport_speed=1, location=Location(x=5, y=5))
        ]
        with pytest.raises(TypeError):
            DispatchService.dispatch(order, couriers)

    def test_dispatch_when_couriers_is_none(self):
        order = (Order(order_id=uuid4(), location=Location(x=1, y=1)),)
        couriers: list[Courier] = None
        with pytest.raises(TypeError):
            DispatchService.dispatch(order, couriers)

    def test_dispatch_when_couriers_is_empty(self):
        order = (Order(order_id=uuid4(), location=Location(x=1, y=1)),)
        couriers: list[Courier] = []
        with pytest.raises(ValueError):
            DispatchService.dispatch(order, couriers)

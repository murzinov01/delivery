from uuid import UUID, uuid4

import pytest
from assertpy import assert_that

from core.domain.model.courier_aggregate import Courier
from core.domain.model.order_aggregate import Order, OrderStatus
from core.domain.model.shared_kernel import Location


class TestOrder:

    def test_be_correct_when_all_params_is_correct_on_created(self):
        order_id: UUID = uuid4()
        location = Location(x=1, y=1)
        order = Order(order_id=order_id, location=location)

        assert_that(order.id).is_equal_to(order_id)
        assert_that(order.status).is_equal_to(OrderStatus.CREATED)
        assert_that(order.location).is_equal_to(location)
        assert_that(order.courier_id).is_none()

    @pytest.mark.parametrize("order_id, location", [(123, Location(x=1, y=1)), (uuid4(), None)])
    def test_raise_error_on_incorrect_params(self, order_id, location):
        with pytest.raises(ValueError):
            Order(order_id=order_id, location=location)

    def test_be_assigned_when_params_is_correct(self):
        order = Order(order_id=uuid4(), location=Location(x=1, y=1))
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))

        order.assign(courier)

        assert_that(order.status).is_equal_to(OrderStatus.ASSIGNED)
        assert_that(order.courier_id).is_equal_to(courier.id)

    def test_raise_assigned_error_when_params_is_incorrect(self):
        order = Order(order_id=uuid4(), location=Location(x=1, y=1))
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))

        with pytest.raises(ValueError):
            order.assign(None)

        with pytest.raises(Order.AssignStatusError):
            order.status = OrderStatus.ASSIGNED
            order.assign(courier)

        with pytest.raises(Order.AssignStatusError):
            order.status = OrderStatus.COMPLETED
            order.assign(courier)

    def test_be_completed_when_order_in_correct_status(self):
        order = Order(order_id=uuid4(), location=Location(x=1, y=1))

        order.status = OrderStatus.ASSIGNED
        order.complete()

        assert_that(order.status).is_equal_to(OrderStatus.COMPLETED)

    def test_raise_completed_error_when_order_is_in_incorrect_status(self):
        order = Order(order_id=uuid4(), location=Location(x=1, y=1))

        with pytest.raises(Order.CompleteStatusError):
            order.complete()

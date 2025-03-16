from uuid import UUID

import pytest
from assertpy import assert_that

from core.domain.model.courier_aggregate import Courier, CourierStatus, Transport
from core.domain.model.shared_kernel import Location


class TestCourier:

    def test_be_corrected_when_all_params_is_correct_on_created(self):
        name: str = "Ivan"
        transport_name: str = "Bicycle"
        transport_speed: int = 2
        location = Location(x=1, y=1)
        courier = Courier(name, transport_name, transport_speed, location)

        assert_that(courier.status).is_equal_to(CourierStatus.FREE)
        assert_that(courier.id).is_instance_of(UUID)
        assert_that(courier.transport).is_instance_of(Transport)
        assert_that(courier.name).is_equal_to(name)
        assert_that(courier.location).is_equal_to(location)

    def test_raise_error_when_params_is_incorrect_on_created(self):
        with pytest.raises(ValueError):
            courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=None)

    def test_set_busy_when_courier_is_free(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))

        courier.set_busy()

        assert_that(courier.status).is_equal_to(CourierStatus.BUSY)

    def test_raise_already_busy_when_courier_is_busy(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))

        courier.set_busy()

        with pytest.raises(Courier.AlreadyBusyStatusError):
            courier.set_busy()

    def test_set_free_when_courier_is_busy(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        courier.status = CourierStatus.BUSY

        courier.set_free()

        assert_that(courier.status).is_equal_to(CourierStatus.FREE)

    def test_raise_already_free_when_courier_is_free(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))

        with pytest.raises(Courier.AlreadyFreeStatusError):
            courier.set_free()

    def test_move_courier(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        target_location = Location(x=5, y=5)
        expected_location = Location(x=3, y=1)

        courier.move(target_location)

        assert_that(courier.location).is_equal_to(expected_location)

    def test_move_courier_several_times(self):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=2, location=Location(x=1, y=1))
        target_location = Location(x=5, y=5)
        expected_location = Location(x=5, y=3)

        courier.move(target_location)
        courier.move(target_location)
        courier.move(target_location)

        assert_that(courier.location).is_equal_to(expected_location)

    @pytest.mark.parametrize(
        "location, target_location, transport_speed, expected_steps_count",
        [
            (Location(x=1, y=1), Location(x=1, y=1), 1, 0),
            (Location(x=1, y=1), Location(x=1, y=1), 2, 0),
            (Location(x=1, y=1), Location(x=5, y=5), 1, 8),
            (Location(x=1, y=1), Location(x=5, y=5), 2, 4),
            (Location(x=1, y=1), Location(x=5, y=4), 1, 7),
            (Location(x=1, y=1), Location(x=5, y=4), 2, 4),
        ],
    )
    def test_calc_steps_to_location(
        self,
        location: Location,
        target_location: Location,
        transport_speed: int,
        expected_steps_count: int,
    ):
        courier = Courier(name="Ivan", transport_name="Bicycle", transport_speed=transport_speed, location=location)

        steps_count: int = courier.calc_steps_to_location(target_location)

        assert_that(steps_count).is_equal_to(expected_steps_count)

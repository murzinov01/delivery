from uuid import UUID

import pytest
from assertpy import assert_that

from core.domain.model.courier_aggregate.transport import Transport
from core.domain.model.shared_kernel.location import Location


class TestTransport:

    @pytest.mark.parametrize("name, speed", [("on foot", 1), ("bicycle", 2), ("car", 3)])
    def test_be_correct_when_params_is_correct_on_created(self, name: str, speed: int):
        transport = Transport(name, speed)

        assert_that(transport.id).is_instance_of(UUID)
        assert_that(transport.name).is_equal_to(name)
        assert_that(transport.speed).is_equal_to(speed)

    @pytest.mark.parametrize(
        "name, speed, expected_exception",
        [
            ("", 1, Transport.EmptyNameError),
            (None, 2, Transport.EmptyNameError),
            ("car", 0, Transport.SpeedLimitError),
            ("car", 4, Transport.SpeedLimitError),
        ],
    )
    def test_raise_error_when_params_is_incorrect(self, name: str, speed: int, expected_exception: Exception):
        with pytest.raises(expected_exception):
            Transport(name, speed)

    def test_equal_when_transport_uuids_are_equal(self):
        transport_1 = Transport(name="car", speed=3)
        transport_2 = Transport(name="car", speed=3)

        transport_2.id = transport_1.id

        assert_that(transport_2).is_equal_to(transport_1)

    def test_not_equal_when_transport_contains_same_params(self):
        transport_1 = Transport(name="car", speed=3)
        transport_2 = Transport(name="car", speed=3)

        assert_that(transport_2).is_not_equal_to(transport_1)

    @pytest.mark.parametrize(
        "location_from, location_to, expected_location",
        [
            (Location(x=1, y=1), Location(x=5, y=5), Location(x=3, y=1)),
            (Location(x=5, y=5), Location(x=1, y=1), Location(x=3, y=5)),
            (Location(x=1, y=1), Location(x=5, y=1), Location(x=3, y=1)),
            (Location(x=1, y=1), Location(x=1, y=5), Location(x=1, y=3)),
            (Location(x=1, y=1), Location(x=2, y=5), Location(x=2, y=2)),
            (Location(x=2, y=1), Location(x=1, y=1), Location(x=1, y=1)),
        ],
    )
    def test_move_from_one_location_to_another(
        self,
        location_from: Location,
        location_to: Location,
        expected_location: Location,
    ):
        transport = Transport(name="bicycle", speed=2)

        new_location: Location = transport.move(location_from, location_to)
        assert_that(new_location).is_equal_to(expected_location)

"""Test location value object."""

import pytest
from assertpy import assert_that
from pydantic import ValidationError

from core.domain.model.shared_kernel.location import Location


class TestLocation:

    def test_be_correct_when_params_is_correct_on_created(self):
        location = Location(x=5, y=5)

        assert_that(location.x).is_equal_to(5)
        assert_that(location.y).is_equal_to(5)

    @pytest.mark.parametrize("x, y", [(0, 10), (-5, 5), (0, 100), (15, -1)])
    def test_raise_error_on_incorrect_params(self, x: int, y: int):
        with pytest.raises(ValidationError):
            Location(x=x, y=y)

    def test_consider_that_location_attributes_is_immutable(self):
        location = Location(x=5, y=5)
        with pytest.raises(ValidationError):
            location.x = 6
        with pytest.raises(ValidationError):
            location.y = 6

    def test_be_equal_when_all_properties_is_equal(self):
        first_location = Location(x=5, y=5)
        second_location = Location(x=5, y=5)

        assert_that(first_location).is_equal_to(second_location)

    @pytest.mark.parametrize("x1, y1, x2, y2", [(1, 2, 1, 3), (5, 4, 1, 3), (5, 2, 1, 2)])
    def test_be_not_equal_when_all_properties_is_not_equal(self, x1: int, y1: int, x2: int, y2: int):
        first_location = Location(x=x1, y=y1)
        second_location = Location(x=x2, y=y2)

        assert_that(first_location).is_not_equal_to(second_location)

    @pytest.mark.parametrize(
        "first_location, second_location, expected_direction",
        [
            (Location(x=1, y=1), Location(x=10, y=10), 18),
            (Location(x=5, y=5), Location(x=1, y=1), 8),
        ],
    )
    def test_calc_distance_to(self, first_location: Location, second_location: Location, expected_direction: int):
        assert_that(first_location.calc_distance_to(second_location)).is_equal_to(expected_direction)

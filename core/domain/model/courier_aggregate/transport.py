"""Transport entity."""

from typing import Self
from uuid import UUID, uuid4

import numpy as np

from core.domain.model.shared_kernel import Location


class Transport:

    MIN_SPEED: int = 1
    MAX_SPEED: int = 3

    class EmptyNameError(Exception):
        def __init__(self) -> None:
            super().__init__("Transport name must be not None or empty string")

    class SpeedLimitError(Exception):
        def __init__(self) -> None:
            super().__init__("Transport speed must be in interval: 1 <= value <= 3")

    def __init__(self, name: str, speed: int) -> None:

        if not name:
            raise self.EmptyNameError
        if speed < self.MIN_SPEED or speed > self.MAX_SPEED:
            raise self.SpeedLimitError

        self.id: UUID = uuid4()
        self.name: str = name
        self.speed: int = speed

    def __eq__(self, value: Self) -> bool:
        return self.id == value.id

    def __str__(self) -> str:
        return f"Transport({self.id}): {self.name=}, {self.speed=}"

    def move(self, location_from: Location, location_to: Location) -> Location:
        max_move_distance: int = self.speed

        diff_x: int = location_to.x - location_from.x
        diff_y: int = location_to.y - location_from.y

        move_x: int = np.clip(diff_x, -max_move_distance, max_move_distance)
        max_move_distance -= abs(move_x)
        move_y: int = np.clip(diff_y, -max_move_distance, max_move_distance)

        return Location(x=location_from.x + move_x, y=location_from.y + move_y)

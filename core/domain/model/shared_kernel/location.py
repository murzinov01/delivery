"""Location value object implementation."""

import random
from typing import Self

from pydantic import BaseModel, ConfigDict, Field


min_value: int = 1
max_value: int = 10


class Location(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int = Field(ge=min_value, le=max_value)
    y: int = Field(ge=min_value, le=max_value)

    def __init__(self, x: int, y: int, **kwargs: dict) -> None:
        super().__init__(x=x, y=y, **kwargs)

    @classmethod
    def random(cls) -> "Location":
        return Location(
            x=random.randint(min_value, max_value),
            y=random.randint(min_value, max_value),
        )

    def distance_to(self, target_location: "Location") -> int:
        return abs(target_location.x - self.x) + abs(target_location.y - self.y)

    def __composite_values__(self) -> tuple:
        return self.x, self.y

    def __repr__(self) -> str:
        return f"Location(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: Self) -> bool:
        return isinstance(other, Location) and other.x == self.x and other.y == self.y

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

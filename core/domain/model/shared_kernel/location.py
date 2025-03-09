"""Location value object implementation."""

import random

from pydantic import BaseModel, ConfigDict, Field


min_value: int = 1
max_value: int = 10


class Location(BaseModel):
    model_config = ConfigDict(frozen=True)

    x: int = Field(ge=min_value, le=max_value)
    y: int = Field(ge=min_value, le=max_value)

    @classmethod
    def random(cls) -> "Location":
        return Location(
            x=random.randint(min_value, max_value),
            y=random.randint(min_value, max_value),
        )

    def calc_distance_to(self, target_location: "Location") -> int:
        return abs(target_location.x - self.x) + abs(target_location.y - self.y)

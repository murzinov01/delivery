"""Get busy couriers response DTO."""

from uuid import UUID

import pydantic


class Location(pydantic.BaseModel):
    x: int
    y: int


class CourierDTO(pydantic.BaseModel):
    id: UUID
    name: str
    location: Location
    transport_id: UUID

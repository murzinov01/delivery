"""Get incomplete orders DTO."""

from uuid import UUID

import pydantic


class Location(pydantic.BaseModel):
    x: int
    y: int


class OrderDTO(pydantic.BaseModel):
    id: UUID
    location: Location

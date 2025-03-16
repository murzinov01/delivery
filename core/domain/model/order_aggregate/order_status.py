"""Order status."""

from enum import StrEnum


class OrderStatus(StrEnum):
    CREATED = "created"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

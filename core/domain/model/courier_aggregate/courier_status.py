"""Courier status."""

from enum import StrEnum


class CourierStatus(StrEnum):
    FREE = "free"
    BUSY = "busy"

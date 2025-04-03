"""Courier aggregate."""

from uuid import UUID, uuid4

from core.domain.model.courier_aggregate.courier_status import CourierStatus
from core.domain.model.courier_aggregate.transport import Transport
from core.domain.model.shared_kernel.location import Location


class Courier:

    class AlreadyBusyStatusError(Exception):
        def __init__(self) -> None:
            super().__init__("Courier is already busy")

    class AlreadyFreeStatusError(Exception):
        def __init__(self) -> None:
            super().__init__("Courier is already free")

    def __init__(self, name: str, transport_name: str, transport_speed: int, location: Location) -> None:
        if location is None:
            raise ValueError("location value is required")

        self.id: UUID = uuid4()
        self.name: str = name
        self.transport: Transport = Transport(transport_name, transport_speed)
        self.location: Location = location
        self.status: CourierStatus = CourierStatus.FREE

    def set_busy(self) -> None:
        if self.status == CourierStatus.BUSY:
            raise self.AlreadyBusyStatusError

        self.status = CourierStatus.BUSY

    def set_free(self) -> None:
        if self.status == CourierStatus.FREE:
            raise self.AlreadyFreeStatusError

        self.status = CourierStatus.FREE

    def move(self, target_location: Location) -> None:
        self.location = self.transport.move(location_from=self.location, location_to=target_location)

    def calc_steps_to_location(self, target_location: Location) -> int:
        distance: int = self.location.distance_to(target_location)

        return round(distance / self.transport.speed)

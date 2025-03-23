"""Order aggregate."""

from uuid import UUID

from core.domain.model.courier_aggregate import Courier
from core.domain.model.order_aggregate import OrderStatus
from core.domain.model.shared_kernel import Location


class Order:

    class AssignStatusError(Exception):
        def __init__(self, status_from: OrderStatus) -> None:
            super().__init__(f"Can't assign from status {status_from}")

    class CompleteStatusError(Exception):
        def __init__(self, status_from: OrderStatus) -> None:
            super().__init__(f"Can't complete the order from status {status_from}")

    def __init__(self, order_id: UUID, location: Location) -> None:
        if not isinstance(order_id, UUID):
            raise ValueError("Order id must be valid UUID")  # noqa:TRY004
        if location is None:
            raise ValueError("location value is required")

        self.id: UUID = order_id
        self.location: Location = location
        self.status: OrderStatus = OrderStatus.CREATED
        self.courier_id: UUID | None = None

    def __str__(self) -> str:
        return f"Order({self.id}): location={self.location}, status={self.status}, courier_id={self.courier_id}"

    def assign(self, courier: Courier) -> None:

        if courier is None:
            raise ValueError("courier value is required")
        if self.status != OrderStatus.CREATED:
            raise self.AssignStatusError(self.status)

        self.status = OrderStatus.ASSIGNED
        self.courier_id = courier.id

    def complete(self) -> None:

        if self.status != OrderStatus.ASSIGNED:
            raise self.CompleteStatusError(self.status)

        self.status = OrderStatus.COMPLETED

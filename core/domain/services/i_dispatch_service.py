"""Dispatch service interface."""

from typing import Protocol

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.order_aggregate.order import Order


class IDispatchService(Protocol):

    def dispatch(self, order: Order, couriers: list[Courier]) -> Courier:
        pass

"""Dispatch service."""

import math

from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.order_aggregate.order import Order


class DispatchService:

    class CourierNotFoundError(Exception):
        def __init__(self, order: Order) -> None:
            super().__init__(f"Suitable courier was not found for {order=}")

    @classmethod
    def dispatch(cls, order: Order, couriers: list[Courier]) -> Courier:
        if order is None or couriers is None:
            raise TypeError
        if len(couriers) == 0:
            raise ValueError("Couriers count must be > 0")

        min_steps_cnt_to_location: int = math.inf
        best_courier: Courier | None = None

        for courier in couriers:
            if (steps_cnt := courier.calc_steps_to_location(order.location)) < min_steps_cnt_to_location:
                min_steps_cnt_to_location = steps_cnt
                best_courier = courier

        if best_courier is None:
            raise cls.CourierNotFoundError(order)

        best_courier.set_busy()
        order.assign(best_courier)

        return best_courier

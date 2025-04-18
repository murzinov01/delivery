"""Delivery Controller."""

# generated by fastapi-codegen:
#   filename:  openapi.yml
#   timestamp: 2025-04-06T12:21:27+00:00

import uuid
from typing import TYPE_CHECKING, Annotated

from api.adapters.http.contract.models import (
    ApiV1CouriersGetResponse,
    ApiV1OrdersActiveGetResponse,
    Courier,
    Error,
    Location,
    Order,
)
from api.ioc import IOCContainer
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from that_depends import Provide

from core.application.use_cases.commands.create_order.command import CreateOrderCommand
from core.application.use_cases.commands.create_order.handler import CreateOrderHandler
from core.application.use_cases.queries.get_busy_couriers.handler import GetBusyCouriersHandler
from core.application.use_cases.queries.get_busy_couriers.query import GetBusyCouriersQuery
from core.application.use_cases.queries.get_incomplete_orders.handler import GetIncompleteOrdersHandler
from core.application.use_cases.queries.get_incomplete_orders.query import GetIncompleteOrdersQuery


if TYPE_CHECKING:
    from core.application.use_cases.queries.get_busy_couriers.response import CourierDTO
    from core.application.use_cases.queries.get_incomplete_orders.response import OrderDTO


ROUTER = APIRouter()


@ROUTER.get("/api/v1/couriers", response_model=ApiV1CouriersGetResponse, responses={"default": {"model": Error}})
async def get_couriers(
    couriers_handler: Annotated[GetBusyCouriersHandler, Depends(Provide[IOCContainer.get_busy_couriers_handler])],
) -> ApiV1CouriersGetResponse | Error:
    """Получить всех курьеров."""
    get_couriers_query = GetBusyCouriersQuery()
    try:
        couriers: list[CourierDTO] = await couriers_handler.handle(get_couriers_query)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Error(code=0, message=str(exc)).model_dump(),
        ) from exc

    return ApiV1CouriersGetResponse(
        root=[
            Courier(id=courier.id, name=courier.name, location=Location(x=courier.location.x, y=courier.location.y))
            for courier in couriers
        ],
    )


@ROUTER.post("/api/v1/orders", response_model=None, responses={"default": {"model": Error}})
async def create_order(
    orders_handler: Annotated[CreateOrderHandler, Depends(Provide[IOCContainer.create_order_handler])],
) -> Error | None:
    """Создать заказ."""
    basket_id: uuid.UUID = uuid.uuid4()
    street = "Несуществующая"

    create_order_command = CreateOrderCommand(basket_id=basket_id, street=street)
    try:
        await orders_handler.handle(create_order_command)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Error(code=1, message=str(exc)).model_dump(),
        ) from exc


@ROUTER.get(
    "/api/v1/orders/active",
    response_model=ApiV1OrdersActiveGetResponse,
    responses={"default": {"model": Error}},
)
async def get_orders(
    orders_handler: Annotated[GetIncompleteOrdersHandler, Depends(Provide[IOCContainer.get_incomplete_orders_handler])],
) -> ApiV1OrdersActiveGetResponse | None:
    """Получить все незавершенные заказы."""
    get_orders_query = GetIncompleteOrdersQuery()

    try:
        orders: list[OrderDTO] = await orders_handler.handle(get_orders_query)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Error(code=0, message=str(exc)).model_dump(),
        ) from exc

    return ApiV1OrdersActiveGetResponse(
        root=[Order(id=order.id, location=Location(x=order.location.x, y=order.location.y)) for order in orders],
    )

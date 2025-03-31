"""Create order command."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateOrderCommand(BaseModel):

    model_config = ConfigDict(frozen=True)

    basket_id: UUID
    street: str

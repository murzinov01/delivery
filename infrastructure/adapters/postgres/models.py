"""ORM models."""

import typing
import sqlalchemy as sa
import sqlalchemy.orm as so

from core.domain.model.shared_kernel.location import Location
from core.domain.model.order_aggregate.order import Order
from core.domain.model.courier_aggregate.transport import Transport
from core.domain.model.courier_aggregate.courier import Courier


METADATA: typing.Final[sa.MetaData] = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)

mapper_registry = so.registry(metadata=METADATA)


order_table = sa.Table(
    "orders",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID, primary_key=True, comment="ID заказа"),
    sa.Column("courier_id", sa.UUID, nullable=True, comment="ID курьера"),
    sa.Column("location_x", sa.SmallInteger, nullable=False, comment="X координата"),
    sa.Column("location_y", sa.SmallInteger, nullable=False, comment="X координата"),
    sa.Column("status", sa.VARCHAR(50), nullable=False, comment="Статус заказа"),
)

transport_table = sa.Table(
    "transports",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID, primary_key=True, comment="ID транспорта"),
    sa.Column("name", sa.VARCHAR(100), nullable=False, comment="Название транспорта"),
    sa.Column("speed", sa.SmallInteger, nullable=False, comment="Скорость транспорта"),
)

courier_table = sa.Table(
    "couriers",
    mapper_registry.metadata,
    sa.Column("id", sa.UUID, primary_key=True, comment="ID курьера"),
    sa.Column("name", sa.VARCHAR(100), nullable=False, comment="Имя курьера"),
    sa.Column(
        "transport_id", sa.ForeignKey("transports.id", ondelete="CASCADE"), nullable=False, comment="ID транспорта"
    ),
    sa.Column("location_x", sa.SmallInteger, nullable=False, comment="X координата"),
    sa.Column("location_y", sa.SmallInteger, nullable=False, comment="X координата"),
    sa.Column("status", sa.VARCHAR(50), nullable=False, comment="Статус курьера"),
)


mapper_registry.map_imperatively(
    Order,
    order_table,
    properties={
        "location": so.composite(Location, order_table.c.location_x, order_table.c.location_y),
    },
)
mapper_registry.map_imperatively(
    Courier,
    courier_table,
    properties={
        "location": so.composite(Location, courier_table.c.location_x, courier_table.c.location_y),
        "transport": so.relationship(transport_table),
    },
)
mapper_registry.map_imperatively(Transport, transport_table)

"""Test's configuration and common fixtures."""

import asyncio
from typing import AsyncIterable

import pytest
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from infrastructure.adapters.postgres.models import mapper_registry


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncIterable[AsyncSession]:
    logger.info("[fixture] starting db container")

    postgres = PostgresContainer("postgres:16", driver="psycopg")
    postgres.start()

    connection_url: str = postgres.get_connection_url()
    logger.info("[fixture] connecting to: {connection_url}")

    # create session with db container information
    engine: AsyncEngine = create_async_engine(connection_url)
    session: AsyncSession = AsyncSession(bind=engine, autoflush=False, expire_on_commit=False)

    # create schema in database
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield session

    logger.info("[fixture] stopping db container")
    postgres.stop()


@pytest.fixture(scope="function", autouse=True)
async def cleanup(test_db_session: AsyncSession):
    logger.info("[fixture] truncating all tables")

    # truncating all tables
    for table in reversed(mapper_registry.metadata.sorted_tables):
        await test_db_session.execute(table.delete())

    logger.info("[fixture] closing db session")
    await test_db_session.commit()
    await test_db_session.close()

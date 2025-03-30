"""Create connection to db (Engine, Session) factories."""

import typing

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


async def create_async_database_engine(
    database_dsn: str,
    pool_min_size: int,
    pool_max_overflow_size: int,
    pool_pre_ping: bool,
    **kwargs: dict,
) -> typing.AsyncIterator[AsyncEngine]:
    logger.info("Connection to Database...")
    async_engine: AsyncEngine = create_async_engine(
        url=database_dsn,
        pool_size=pool_min_size,
        max_overflow=pool_max_overflow_size,
        pool_pre_ping=pool_pre_ping,
        **kwargs,
    )
    try:
        yield async_engine
    finally:
        logger.info("Disconnection from Database...")
        await async_engine.dispose()


async def create_async_session(engine: AsyncEngine, **kwargs: dict) -> typing.AsyncIterator[AsyncSession]:
    session: AsyncSession = AsyncSession(bind=engine, **kwargs)
    try:
        yield session
    except Exception:
        logger.exception("Session rollback because of exception")
        await session.rollback()
        raise
    finally:
        await session.close()

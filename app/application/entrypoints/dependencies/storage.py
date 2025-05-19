from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.infrastructure.database.base import SessionFactory


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session, session.begin():
        yield session

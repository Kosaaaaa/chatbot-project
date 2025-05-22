from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.infrastructure.database.base import SessionFactory
from app.infrastructure.database.repository.chat_message import ChatMessageRepository


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session, session.begin():
        yield session


def get_chat_message_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> ChatMessageRepository:
    return ChatMessageRepository(session)

from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
)
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.domain.models.chat_message import ChatMessage


class ChatMessageRepository:
    entity_cls: type[ChatMessage] = ChatMessage

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def query(self) -> list[ChatMessage]:
        result = await self.session.execute(select(self.entity_cls))
        return list(result.scalars().all())

    async def get_model_messages(self) -> list[ModelMessage]:
        chat_messages = await self.query()
        messages: list[ModelMessage] = []
        for msg in chat_messages:
            messages.extend(ModelMessagesTypeAdapter.validate_json(msg.message_list))
        return messages

    async def add_messages(self, messages: bytes) -> None:
        self.session.add(
            ChatMessage(
                message_list=messages.decode(),
            )
        )
        await self.session.flush()
        await self.session.commit()

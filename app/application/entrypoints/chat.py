from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.application.entrypoints.dependencies.storage import get_session
from app.domain.models.chat_message import ChatMessage

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.get("/")
async def get_chat(session: Annotated[AsyncSession, Depends(get_session)]):
    result = await session.execute(select(ChatMessage))
    return Response(
        b"\n".join([m.model_dump_json().encode() for m in result.scalars().all()]),
        media_type="text/plain",
    )

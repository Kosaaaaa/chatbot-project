import json
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.responses import Response, StreamingResponse
from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

from app.application.entrypoints.dependencies.agent import get_agent
from app.application.entrypoints.dependencies.storage import get_chat_message_repository
from app.application.entrypoints.schema.chat_message import ChatMessage
from app.infrastructure.database.repository.chat_message import ChatMessageRepository

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def to_chat_message(m: ModelMessage) -> ChatMessage:
    first_part = m.parts[0]
    if isinstance(m, ModelRequest) and isinstance(first_part, UserPromptPart):
        assert isinstance(first_part.content, str)
        return ChatMessage(
            role="user",
            timestamp=first_part.timestamp.isoformat(),
            content=first_part.content,
        )
    elif isinstance(m, ModelResponse) and isinstance(first_part, TextPart):
        return ChatMessage(
            role="model",
            timestamp=m.timestamp.isoformat(),
            content=first_part.content,
        )
    raise UnexpectedModelBehavior(f"Unexpected message type for chat app: {m}")


@chat_router.get("/")
async def get_chat(
    chat_message_repository: Annotated[ChatMessageRepository, Depends(get_chat_message_repository)],
) -> Response:
    msgs = await chat_message_repository.get_model_messages()
    return Response(
        b"\n".join(to_chat_message(m).model_dump_json().encode("utf-8") for m in msgs),
        media_type="text/plain",
    )


@chat_router.post("/")
async def post_chat(
    prompt: Annotated[str, Form()],
    agent: Annotated[Agent, Depends(get_agent)],
    chat_message_repository: Annotated[ChatMessageRepository, Depends(get_chat_message_repository)],
) -> StreamingResponse:
    async def stream_messages():
        """Streams new line delimited JSON `Message`s to the client."""
        # stream the user prompt so that can be displayed straight away
        yield (
            json.dumps(
                {
                    "role": "user",
                    "timestamp": datetime.now(tz=UTC).isoformat(),
                    "content": prompt,
                }
            ).encode("utf-8")
            + b"\n"
        )
        # get the chat history so far to pass as context to the agent
        messages = await chat_message_repository.get_model_messages()
        # run the agent with the user prompt and the chat history
        async with agent.run_stream(prompt, message_history=messages) as result:
            async for text in result.stream(debounce_by=0.01):
                # text here is a `str` and the frontend wants
                # JSON encoded ModelResponse, so we create one
                m = ModelResponse(parts=[TextPart(text)], timestamp=result.timestamp())
                yield to_chat_message(m).model_dump_json().encode("utf-8") + b"\n"

        # add new messages (e.g. the user prompt and the agent response in this case) to the database
        await chat_message_repository.add_messages(result.new_messages_json())

    return StreamingResponse(stream_messages(), media_type="text/plain")

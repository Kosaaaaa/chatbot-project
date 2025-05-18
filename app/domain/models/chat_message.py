import uuid
from enum import StrEnum

from sqlmodel import Field, SQLModel


class ChatMessageRole(StrEnum):
    USER = "USER"
    MODEL = "MODEL"


class ChatMessageBase(SQLModel):
    role: ChatMessageRole
    timestamp: str
    content: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)

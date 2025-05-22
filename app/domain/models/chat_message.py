import uuid

from sqlalchemy.types import Text
from sqlmodel import Field, SQLModel


class ChatMessage(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    message_list: str = Field(sa_type=Text)

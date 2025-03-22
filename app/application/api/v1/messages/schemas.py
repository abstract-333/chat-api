from collections.abc import Iterable
from datetime import datetime

from pydantic import BaseModel

from domain.entities.messages import (
    Chat,
    Message,
)


class CreateChatInSchema(BaseModel):
    title: str


class CreateChatOutSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> "CreateChatOutSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageSchema(BaseModel):
    text: str
    chat_oid: str


class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str

    @classmethod
    def from_entity(cls, message: Message) -> "CreateMessageResponseSchema":
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageDetailSchema":
        return cls(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime
    messages: Iterable[MessageDetailSchema]

    @classmethod
    def from_entity(cls, chat: Chat) -> "ChatDetailSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
            messages=[
                MessageDetailSchema.from_entity(message) for message in chat.messages
            ],
        )

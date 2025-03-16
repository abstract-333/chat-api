import datetime
from typing import TypedDict

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.values.messages import (
    Text,
    Title,
)


class MessageDocument(TypedDict):
    oid: str
    text: str
    created_at: datetime.datetime


class ChatDocument(TypedDict):
    oid: str
    title: str
    created_at: datetime.datetime
    messages: list[MessageDocument]


def convert_message_entity_to_document(
    message: Message,
) -> MessageDocument:
    return {
        "oid": message.oid,
        "created_at": message.created_at,
        "text": message.text.as_generic_type(),
    }


def convert_message_document_to_entity(
    document: MessageDocument,
) -> Message:
    return Message(
        oid=document["oid"],
        text=Text(document["text"]),
        created_at=document["created_at"],
    )


def convert_chat_entity_to_document(chat: Chat) -> ChatDocument:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [
            convert_message_entity_to_document(message) for message in chat.messages
        ],
    }


def convert_chat_document_to_entity(document: ChatDocument) -> Chat:
    return Chat(
        oid=document["oid"],
        title=Title(document["title"]),
        created_at=document["created_at"],
        messages={
            convert_message_document_to_entity(message)
            for message in document["messages"]
        },
    )

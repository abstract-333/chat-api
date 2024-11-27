import datetime

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages.convertors import (
    convert_document_to_message,
    convert_message_to_document,
)


def convert_chat_to_document(chat: Chat) -> dict[
    str,
    str | datetime.datetime | list[dict[str, str | datetime.datetime]],
]:

    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [convert_message_to_document(message) for message in chat.messages],
    }


def convert_document_to_chat(
    document: dict[
        str,
        str | datetime.datetime | list[dict[str, str | datetime.datetime]],
    ],
) -> Chat:
    return Chat(
        oid=document["oid"],
        title=Title(document["title"]),
        created_at=document["created_at"],
        messages={
            convert_document_to_message(message) for message in document["chats"]
        },
    )

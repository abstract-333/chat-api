import datetime

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.values.messages import (
    Text,
    Title,
)


def convert_message_to_document(message: Message) -> dict[str, str | datetime.datetime]:
    return {
        "oid": message.oid,
        "created_at": message.created_at,
        "text": message.text.as_generic_type(),
    }


def convert_document_to_message(
    document: dict[str, str | datetime.datetime],
) -> Message:
    return Message(
        oid=document["oid"],
        text=Text(document["text"]),
        created_at=document["created_at"],
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

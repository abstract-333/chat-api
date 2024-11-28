from typing import (
    Any,
    Mapping,
)

from domain.entities.messages import (
    Chat,
    Message,
)


# TODO: add typing
def convert_message_entity_to_document(
    message: Message,
) -> dict[str, Any]:
    return {
        "oid": message.oid,
        "created_at": message.created_at,
        "text": message.text.as_generic_type(),
    }


def convert_message_document_to_entity(
    document: Mapping[str, Any],
) -> Message:
    return Message(
        oid=document["oid"],
        text=document["text"],
        created_at=document["created_at"],
    )


def convert_chat_entity_to_document(chat: Chat) -> dict[str, Any]:

    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [
            convert_message_entity_to_document(message) for message in chat.messages
        ],
    }


def convert_chat_document_to_entity(document: Mapping[str, Any]) -> Chat:
    return Chat(
        oid=document["oid"],
        title=document["title"],
        created_at=document["created_at"],
        messages={
            convert_message_document_to_entity(message)
            for message in document["messages"]
        },
    )

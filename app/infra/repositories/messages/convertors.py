import datetime

from domain.entities.messages import Message
from domain.values.messages import Text


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

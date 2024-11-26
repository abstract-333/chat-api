import datetime

from domain.entities.messages import (
    Chat,
    Message,
)


def convert_message_to_document(message: Message) -> dict[str, str | datetime.datetime]:
    return {
        'oid': message.oid,
        'created_at': message.created_at,
        'text': message.text.as_generic_type(),
    }


def convert_chat_to_document(chat: Chat) -> dict[
    str, str | datetime.datetime | list[dict[str, str | datetime.datetime]],
]:
    return {
        'oid': chat.oid,
        'title': chat.title.as_generic_type(),
        'created_at': chat.created_at,
        'messages': [convert_message_to_document(message) for message in chat.messages],

    }

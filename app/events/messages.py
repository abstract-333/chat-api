from dataclasses import dataclass

from events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str

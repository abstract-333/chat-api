from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from domain.entities.base import BaseEntity
from domain.values.messages import (
    Text,
    Title,
)
from events.messages import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )

    @classmethod
    def create_chat(cls, title: Title) -> Self:
        new_chat: Self = cls(title=title)
        new_chat.register_event(
            event=NewChatCreatedEvent(
                chat_oid=new_chat.oid,
                chat_title=title.as_generic_type(),
            ),
        )
        return new_chat

    def add_message(self, message: Message) -> None:
        self.messages.add(message)
        self.register_event(
            event=NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                message_oid=message.oid,
                chat_oid=self.oid,
            ),
        )

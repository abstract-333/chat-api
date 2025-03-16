from abc import ABC
from dataclasses import (
    dataclass,
    field,
)

from domain.entities.messages import (
    Chat,
    Message,
)
from infra.repositories.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)


@dataclass
class BaseMemoryRepository(ABC):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)


@dataclass
class MemoryChatRepository(BaseChatsRepository, BaseMemoryRepository):
    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        for chat in self._saved_chats:
            if chat.oid == oid:
                return chat
        return None

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)


@dataclass
class MemoryMessageRepository(BaseMessagesRepository, BaseMemoryRepository):
    # TODO
    async def add_message(self, chat_oid: str, message: Message) -> None:
        for iteration_chats in range(len(self._saved_chats)):
            if self._saved_chats[iteration_chats].oid == chat_oid:
                self._saved_chats[iteration_chats].add_message(message)
                break

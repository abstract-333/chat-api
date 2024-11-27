from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.messages import Message


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, chat_oid: str, message: Message) -> None: ...

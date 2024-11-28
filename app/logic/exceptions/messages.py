from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self) -> str:
        return f'Chat with this title "{self.title}" already exists'


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    oid: str

    @property
    def message(self) -> str:
        return f'Chat with this oid "{self.oid}" not found'

from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.chats.base import BaseChatsRepository
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithThatTitleAlreadyExistsException(title=command.title)
        title = Title(value=command.title)

        new_chat: Chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(chat=new_chat)

        return new_chat

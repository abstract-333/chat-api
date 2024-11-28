from dataclasses import dataclass

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.values.messages import (
    Text,
    Title,
)
from infra.repositories.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from logic.commands.base import (
    BaseCommand,
    CommandHandler,
)
from logic.exceptions.messages import (
    ChatNotFoundException,
    ChatWithThatTitleAlreadyExistsException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithThatTitleAlreadyExistsException(title=command.title)
        title = Title(value=command.title)

        new_chat: Chat = Chat.create_chat(title=title)
        await self.chats_repository.add_chat(chat=new_chat)

        return new_chat


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    chat_oid: str
    text: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Message]):
    messages_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat_oid: str = command.chat_oid
        chat: Chat | None = await self.chats_repository.get_chat_by_oid(oid=chat_oid)
        if not chat:
            raise ChatNotFoundException(oid=chat_oid)

        text: Text = Text(command.text)
        message: Message = Message(text=text)
        chat.add_message(message)
        await self.messages_repository.add_message(message=message, chat_oid=chat_oid)
        return message

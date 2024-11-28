import pytest
from faker import Faker

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.values.messages import Title
from infra.repositories.base import BaseChatsRepository
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from logic.exceptions.messages import (
    ChatNotFoundException,
    ChatWithThatTitleAlreadyExistsException,
)
from logic.mediator import Mediator
from utils.uuid_4 import get_uuid4


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chats_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    chat: Chat
    chat, *_ = await mediator.handle_command(
        command=CreateChatCommand(title=faker.text()),
    )
    assert await chats_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type(),
    )


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chats_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    title_text: str = faker.text()
    chat = Chat(title=Title(value=title_text))
    await chats_repository.add_chat(chat=chat)

    assert chat in chats_repository._saved_chats

    with pytest.raises(expected_exception=ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(command=CreateChatCommand(title=title_text))

    assert len(chats_repository._saved_chats) == 1


@pytest.mark.asyncio
async def test_create_message_command_success(
    chats_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    title_text: str = faker.text()
    chat = Chat(title=Title(value=title_text))
    await chats_repository.add_chat(chat=chat)
    message: Message
    message, *_ = await mediator.handle_command(
        command=CreateMessageCommand(chat_oid=chat.oid, text=faker.text()),
    )
    assert message in chats_repository._saved_chats[0].messages


@pytest.mark.asyncio
async def test_create_message_command_chat_not_exists(
    chats_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    oid: str = get_uuid4()
    assert not await chats_repository.get_chat_by_oid(oid=oid)
    with pytest.raises(expected_exception=ChatNotFoundException):
        await mediator.handle_command(
            command=CreateMessageCommand(chat_oid=get_uuid4(), text=faker.text()),
        )
    assert not await chats_repository.get_chat_by_oid(oid=oid)

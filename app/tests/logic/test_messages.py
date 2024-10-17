import pytest
from faker import Faker

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.base import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    chat: Chat
    chat, *_ = await mediator.handle_command(
        command=CreateChatCommand(title=faker.text())
    )

    assert await chat_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type()
    )


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
) -> None:
    title_text: str = faker.text()
    chat = Chat(title=Title(value=title_text))
    await chat_repository.add_chat(chat=chat)

    assert chat in chat_repository._saved_chats

    with pytest.raises(expected_exception=ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(command=CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chats) == 1

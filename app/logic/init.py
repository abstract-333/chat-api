from infra.repositories.base import BaseChatRepository
from logic.commands.messages import CreateChatCommandHandler, CreateChatCommand
from logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    mediator.register_command(
        command=CreateChatCommand,
        command_handlers=[CreateChatCommandHandler(chat_repository=chat_repository)],
    )

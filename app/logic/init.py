from functools import lru_cache
from punq import Container, Scope


from infra.repositories.base import BaseChatRepository
from infra.repositories.memory import MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(
        service=BaseChatRepository,
        factory=MemoryChatRepository,
        scope=Scope.singleton,
    )
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            command=CreateChatCommand,
            command_handlers=[container.resolve(service_key=CreateChatCommandHandler)],
        )

        return mediator

    container.register(service=Mediator, factory=init_mediator)

    return container

from punq import (
    Container,
    Scope,
)

from infra.repositories.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infra.repositories.memory import (
    MemoryChatRepository,
    MemoryMessageRepository,
)
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatsRepository,
        MemoryChatRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseMessagesRepository,
        MemoryMessageRepository,
        scope=Scope.singleton,
    )

    return container

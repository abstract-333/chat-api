from punq import (
    Container,
    Scope,
)

from infra.repositories.chats.base import BaseChatsRepository
from infra.repositories.chats.memory import MemoryChatRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseChatsRepository,
        MemoryChatRepository,
        scope=Scope.singleton,
    )

    return container

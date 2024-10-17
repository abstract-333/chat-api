from infra.repositories.base import BaseChatRepository
from infra.repositories.memory import MemoryChatRepository
from logic.init import _init_container
from punq import Container, Scope


def init_dummy_container() -> Container:
    container: Container = _init_container()
    container.register(
        service=BaseChatRepository,
        factory=MemoryChatRepository,
        scope=Scope.singleton,
    )

    return container

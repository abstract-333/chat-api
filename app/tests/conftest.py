from punq import Container
from pytest import fixture

from infra.repositories.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(service_key=Mediator)


@fixture()
def chats_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(service_key=BaseChatsRepository)


@fixture()
def messages_repository(container: Container) -> BaseMessagesRepository:
    return container.resolve(service_key=BaseMessagesRepository)

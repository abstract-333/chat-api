from punq import Container
from pytest import fixture

from infra.repositories.chats.base import BaseChatsRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(service_key=Mediator)


@fixture()
def chat_repository(container: Container) -> BaseChatsRepository:
    return container.resolve(service_key=BaseChatsRepository)

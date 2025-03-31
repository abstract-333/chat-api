from contextlib import nullcontext as does_not_raise
from datetime import datetime
from typing import Any

import pytest
from faker import Faker

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.exceptions.messages import (
    EmptyTextError,
    TextTooLongException,
)
from domain.values.messages import (
    Text,
    Title,
)
from events.messages import NewMessageReceivedEvent
from utils.uuid_4 import get_uuid4


@pytest.mark.parametrize(
    argnames='text, chat_oid, expectation',
    argvalues=[
        ('Hello World', get_uuid4(), does_not_raise()),
        ('Hello World' * 100, get_uuid4(), does_not_raise()),
        ('', get_uuid4(), pytest.raises(expected_exception=EmptyTextError)),
    ],
)
def test_create_message(
    text: str,
    chat_oid: str,
    expectation: Any,
) -> None:
    with expectation:
        assert (
            Message(text=Text(value=text), chat_oid=chat_oid).text.as_generic_type()
            == text
        )
        assert Message(text=Text(value=text), chat_oid=chat_oid).text == Text(text)
        assert (
            Message(text=Text(value=text), chat_oid=chat_oid).created_at.date()
            == datetime.today().date()
        )


@pytest.mark.parametrize(
    argnames='chat_title ,expectation',
    argvalues=[
        ('Hello World Chat', does_not_raise()),
        ('', pytest.raises(expected_exception=EmptyTextError)),
        ('t' * 300, pytest.raises(expected_exception=TextTooLongException)),
    ],
)
def test_create_chat(
    chat_title: str,
    expectation: Any,
) -> None:
    with expectation:
        assert Chat(title=Title(value=chat_title)).title.as_generic_type() == chat_title
        assert Chat(title=Title(value=chat_title)).created_at.date()
        assert (
            Chat(title=Title(value=chat_title)).created_at.date()
            == datetime.today().date()
        )


def test_add_message_to_chat(faker: Faker) -> None:
    title: str = faker.text(max_nb_chars=100)
    chat = Chat(title=Title(title))

    message_text: str = faker.text(max_nb_chars=200)
    message: Message = Message(chat_oid=chat.oid, text=Text(message_text))

    chat.add_message(message=message)
    assert message in chat.messages
    chat.add_message(message=message)
    assert message in chat.messages


def test_new_message_events(faker: Faker) -> None:
    title: str = faker.text(max_nb_chars=100)
    chat = Chat(title=Title(title))

    message_text: str = faker.text(max_nb_chars=200)
    message: Message = Message(chat_oid=chat.oid, text=Text(message_text))
    chat.add_message(message=message)
    assert message in chat.messages

    events = chat.pull_events()
    pulled_events = chat.pull_events()
    assert not pulled_events, pulled_events
    assert len(events) == 1, events

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), new_event
    assert new_event.message_oid == message.oid
    assert new_event.chat_oid == chat.oid
    assert new_event.message_text == message.text.as_generic_type()

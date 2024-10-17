from contextlib import nullcontext as does_not_raise
from datetime import datetime
from typing import Any

import pytest
from domain.entities.messages import Chat, Message
from domain.exceptions.messages import EmptyTextError, TextTooLongException
from domain.values.messages import Text, Title
from events.messages import NewMessageReceivedEvent


@pytest.mark.parametrize(
    argnames="text, expectation",
    argvalues=[
        ("Hello World", does_not_raise()),
        ("Hello World" * 100, does_not_raise()),
        ("", pytest.raises(expected_exception=EmptyTextError)),
    ],
)
def test_create_message(
    text: str,
    expectation: Any,
):
    with expectation:
        assert Message(text=Text(value=text)).text.as_generic_type() == text
        assert Message(text=Text(value=text)).text == Text(text)
        assert (
            Message(text=Text(value=text)).created_at.date() == datetime.today().date()
        )


@pytest.mark.parametrize(
    argnames="chat_title ,expectation",
    argvalues=[
        ("Hello World Chat", does_not_raise()),
        ("", pytest.raises(expected_exception=EmptyTextError)),
        ("t" * 300, pytest.raises(expected_exception=TextTooLongException)),
    ],
)
def test_create_chat(
    chat_title: str,
    expectation: Any,
):
    with expectation:
        assert Chat(title=Title(value=chat_title)).title.as_generic_type() == chat_title
        assert Chat(title=Title(value=chat_title)).created_at.date()
        assert (
            Chat(title=Title(value=chat_title)).created_at.date()
            == datetime.today().date()
        )


@pytest.mark.parametrize(
    argnames="message, title ,expectation",
    argvalues=[
        (
            Message(Text("Hello World Chat")),
            Title("Hello World Title"),
            does_not_raise(),
        ),
    ],
)
def test_add_message_to_chat(
    message: Message,
    title: Title,
    expectation: Any,
):
    with expectation:
        chat = Chat(title=title)
        chat.add_message(message=message)
        assert message in chat.messages
        chat.add_message(message=message)
        assert message in chat.messages


@pytest.mark.parametrize(
    argnames="message, title ,expectation",
    argvalues=[
        (
            Message(Text("Hello World Chat")),
            Title("Hello World Title"),
            does_not_raise(),
        ),
    ],
)
def test_new_message_events(
    message: Message,
    title: Title,
    expectation: Any,
):
    with expectation:
        chat = Chat(title=title)
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

from datetime import datetime
from contextlib import nullcontext as does_not_raise
from typing import Any
import pytest
from domain.entities.messages import Chat, Message
from domain.exceptions.messages import EmptyTextError, TextTooLongException
from domain.values.messages import Text, Title


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

from dataclasses import dataclass
from typing import Any, TypeVar

from domain.exceptions.messages import EmptyTextError, TextTooLongException
from domain.values.base import BaseValueObject

VT = TypeVar(name="VT", bound=Any)


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTextError()

    def as_generic_type(self) -> str:
        return str(object=self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTextError()

        if len(self.value) > 255:
            raise TextTooLongException(text=self.value)

    def as_generic_type(self) -> str:
        return str(object=self.value)

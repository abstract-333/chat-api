from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from events.base import BaseEvent
from utils.uuid import get_uuid4


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=get_uuid4,
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    _events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )

    def register_event(self, event: BaseEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events: list[BaseEvent] = copy(self._events)
        self._events.clear()
        return registered_events

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: Self) -> bool:
        return self.oid == __value.oid

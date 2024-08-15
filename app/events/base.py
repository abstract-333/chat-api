from abc import ABC
from dataclasses import dataclass, field

from utils.uuid import get_uuid4


@dataclass
class BaseEvent(ABC):
    event_id: str = field(
        default_factory=get_uuid4,
        kw_only=True,
    )

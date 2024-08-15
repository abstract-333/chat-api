from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

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

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: "BaseEntity") -> bool:
        return self.oid == __value.oid

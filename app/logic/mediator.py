from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from logic.commands.base import (
    CommandHandler,
    CR,
    CT,
)
from logic.events.base import (
    ER,
    ET,
    EventHandler,
)
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    EventHandlersNotRegisteredException,
)


@dataclass(eq=False)
class Mediator:
    events_map: defaultdict[ET, list[EventHandler[ET, ER]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: defaultdict[CT, list[CommandHandler[CT, CR]]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(
            self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
            self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    async def publish(self, events: Iterable[ET]) -> Iterable[ER]:
        event_type = events.__class__
        handlers = self.events_map.get(event_type)
        print(f"publish {event_type}")
        print(f"publish {handlers}")
        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)

        result: list[ER] = []

        for event in events:
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: CT) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type=command_type)

        return [await handler.handle(command) for handler in handlers]

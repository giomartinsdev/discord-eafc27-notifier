import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy.orm import Session

from .models import Event

log = logging.getLogger("app.events")


@dataclass(frozen=True)
class DomainEvent:
    type: str
    payload: dict


_subscribers: dict[str, list[Callable[[DomainEvent], None]]] = defaultdict(list)


def subscribe(event_type: str, handler: Callable[[DomainEvent], None]) -> None:
    _subscribers[event_type].append(handler)


def publish(session: Session, event: DomainEvent) -> DomainEvent:
    """Persist to outbox in same transaction as the write (transactional outbox)."""
    session.add(Event(type=event.type, payload=event.payload))
    return event


def dispatch(event: DomainEvent) -> None:
    for handler in _subscribers[event.type]:
        handler(event)
    for handler in _subscribers["*"]:
        handler(event)


subscribe("*", lambda e: log.info("event %s %s", e.type, e.payload))

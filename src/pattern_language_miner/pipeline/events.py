"""Observer pattern implementation for pipeline events.

Defines the event types broadcast by the pipeline and the :class:`EventBus`
that decouples event producers from consumers.

Design Pattern
--------------
**Observer** — :class:`EventBus` is the *Subject*.  Callables registered
via :meth:`EventBus.subscribe` are the *Observers*.  This avoids tight
coupling between pipeline steps and progress-reporting or logging logic.

Example:
    >>> bus = EventBus()
    >>> bus.subscribe(PipelineEventType.STEP_COMPLETE,
    ...               lambda e: print(f"Done: {e.step_name}"))
    >>> bus.publish(PipelineEvent(PipelineEventType.STEP_COMPLETE, "analyze"))
    Done: analyze
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class PipelineEventType(Enum):
    """Enumeration of event types emitted during pipeline execution."""

    PIPELINE_START = auto()
    STEP_START = auto()
    STEP_COMPLETE = auto()
    STEP_ERROR = auto()
    PIPELINE_COMPLETE = auto()


@dataclass
class PipelineEvent:
    """Carries information about a single pipeline event.

    Attributes:
        event_type: The type of event that occurred.
        step_name: Human-readable name of the pipeline step.
        payload: Optional extra data associated with the event.
    """

    event_type: PipelineEventType
    step_name: str
    payload: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    """Lightweight publish-subscribe event bus.

    Subscribers register a callable for a given :class:`PipelineEventType`.
    When an event is published, all registered handlers for that type are
    invoked in registration order.

    Example:
        >>> bus = EventBus()
        >>> events = []
        >>> bus.subscribe(PipelineEventType.STEP_COMPLETE, events.append)
        >>> bus.publish(PipelineEvent(PipelineEventType.STEP_COMPLETE, "enrich"))
        >>> len(events)
        1
    """

    def __init__(self) -> None:
        self._handlers: Dict[
            PipelineEventType, List[Callable[[PipelineEvent], None]]
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: PipelineEventType,
        handler: Callable[[PipelineEvent], None],
    ) -> None:
        """Register *handler* to be called when *event_type* is published.

        Args:
            event_type: The event type to listen for.
            handler: A callable that accepts a :class:`PipelineEvent`.
        """
        self._handlers[event_type].append(handler)
        logger.debug("Subscribed %s to %s.", handler, event_type)

    def publish(self, event: PipelineEvent) -> None:
        """Dispatch *event* to all registered handlers.

        Handler exceptions are caught and logged so that one failing
        observer cannot prevent others from running.

        Args:
            event: The event to broadcast.
        """
        for handler in self._handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Handler %s raised an exception for %s: %s",
                    handler,
                    event.event_type,
                    exc,
                )

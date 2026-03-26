"""Pipeline orchestrator using the Chain-of-Responsibility pattern.

Design Patterns
---------------
- **Chain of Responsibility** — :class:`Pipeline` executes a sequence of
  :class:`PipelineStep` objects, each responsible for one transformation.
- **Observer** — progress events are broadcast via an :class:`EventBus` so
  that callers can react without polluting step logic.
- **Template Method** — :class:`PipelineStep` defines the contract; concrete
  sub-classes override :meth:`PipelineStep.run`.

Example:
    >>> from pattern_language_miner.extractor.pattern_extractor import PatternExtractor
    >>> from pathlib import Path
    >>>
    >>> class ExtractStep(PipelineStep):
    ...     name = "extract"
    ...     def run(self, context):
    ...         extractor = context["extractor"]
    ...         extractor.run()
    ...         return context
    >>>
    >>> bus = EventBus()
    >>> bus.subscribe(PipelineEventType.STEP_COMPLETE,
    ...               lambda e: print(f"Finished: {e.step_name}"))
    >>> pipeline = Pipeline([ExtractStep()], event_bus=bus)
    >>> pipeline.execute({"extractor": extractor})
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .events import EventBus, PipelineEvent, PipelineEventType

logger = logging.getLogger(__name__)


class PipelineStep(ABC):
    """Abstract base for a single step in the analysis pipeline.

    Sub-classes must:

    1. Set a non-empty :attr:`name` class attribute.
    2. Implement :meth:`run`, which receives and returns a *context* dict.

    The *context* dict is a shared mutable namespace that propagates state
    between consecutive steps.
    """

    #: Human-readable name shown in logs and events.
    name: str = "unnamed_step"

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the step and return the (possibly mutated) context.

        Args:
            context: Shared pipeline context dict.  Steps may read from
                and write to this dict.

        Returns:
            The updated context dict.
        """


class Pipeline:
    """Execute an ordered sequence of :class:`PipelineStep` objects.

    Steps share a mutable *context* dictionary.  If a step raises an
    exception the pipeline stops and re-raises, after publishing a
    :data:`PipelineEventType.STEP_ERROR` event.

    Args:
        steps: Ordered list of steps to execute.
        event_bus: Optional :class:`EventBus` for progress notifications.

    Example:
        >>> pipeline = Pipeline([step_a, step_b])
        >>> result = pipeline.execute({"input_dir": Path("./docs")})
    """

    def __init__(
        self,
        steps: List[PipelineStep],
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.steps = steps
        self.event_bus = event_bus or EventBus()

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run all steps in order, threading *context* through each one.

        Args:
            context: Initial context dict passed to the first step.

        Returns:
            The final context dict returned by the last step.

        Raises:
            Exception: Re-raises any exception thrown by a step, after
                publishing a :data:`PipelineEventType.STEP_ERROR` event.
        """
        self.event_bus.publish(
            PipelineEvent(PipelineEventType.PIPELINE_START, "pipeline")
        )
        logger.info("Pipeline starting with %d step(s).", len(self.steps))

        for step in self.steps:
            self.event_bus.publish(
                PipelineEvent(PipelineEventType.STEP_START, step.name)
            )
            logger.info("Step [%s] starting.", step.name)
            try:
                context = step.run(context)
            except Exception as exc:
                self.event_bus.publish(
                    PipelineEvent(
                        PipelineEventType.STEP_ERROR,
                        step.name,
                        {"error": str(exc)},
                    )
                )
                logger.error("Step [%s] failed: %s", step.name, exc)
                raise
            self.event_bus.publish(
                PipelineEvent(PipelineEventType.STEP_COMPLETE, step.name)
            )
            logger.info("Step [%s] complete.", step.name)

        self.event_bus.publish(
            PipelineEvent(PipelineEventType.PIPELINE_COMPLETE, "pipeline")
        )
        logger.info("Pipeline complete.")
        return context

"""Pipeline sub-package.

Provides the :class:`~pattern_language_miner.pipeline.pipeline.Pipeline`
orchestrator and the :class:`~pattern_language_miner.pipeline.events.PipelineEvent`
Observer infrastructure.
"""

from .events import EventBus, PipelineEvent, PipelineEventType
from .pipeline import Pipeline, PipelineStep

__all__ = [
    "EventBus",
    "Pipeline",
    "PipelineEvent",
    "PipelineEventType",
    "PipelineStep",
]

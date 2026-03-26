"""Unit tests for the Pipeline orchestrator and EventBus."""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from pattern_language_miner.pipeline.events import (
    EventBus,
    PipelineEvent,
    PipelineEventType,
)
from pattern_language_miner.pipeline.pipeline import Pipeline, PipelineStep


# ---------------------------------------------------------------------------
# Concrete step implementations for testing
# ---------------------------------------------------------------------------


class IncrementStep(PipelineStep):
    """Increment a counter in the context."""

    name = "increment"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["count"] = context.get("count", 0) + 1
        return context


class FailingStep(PipelineStep):
    """Always raise a RuntimeError."""

    name = "failing"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise RuntimeError("Deliberate failure")


class AppendStep(PipelineStep):
    """Append a value to a list in the context."""

    def __init__(self, value: str) -> None:
        self.name = f"append_{value}"
        self.value = value

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context.setdefault("items", []).append(self.value)
        return context


# ---------------------------------------------------------------------------
# EventBus tests
# ---------------------------------------------------------------------------


class TestEventBus:
    def test_subscribe_and_publish(self):
        bus = EventBus()
        received: List[PipelineEvent] = []
        bus.subscribe(PipelineEventType.STEP_COMPLETE, received.append)
        event = PipelineEvent(PipelineEventType.STEP_COMPLETE, "test")
        bus.publish(event)
        assert len(received) == 1
        assert received[0] is event

    def test_multiple_subscribers(self):
        bus = EventBus()
        calls: List[str] = []
        bus.subscribe(PipelineEventType.STEP_START, lambda e: calls.append("a"))
        bus.subscribe(PipelineEventType.STEP_START, lambda e: calls.append("b"))
        bus.publish(PipelineEvent(PipelineEventType.STEP_START, "x"))
        assert calls == ["a", "b"]

    def test_no_handler_for_event_type(self):
        bus = EventBus()
        # Should not raise when no handlers are registered.
        bus.publish(PipelineEvent(PipelineEventType.PIPELINE_COMPLETE, "pipeline"))

    def test_handler_exception_does_not_propagate(self):
        bus = EventBus()

        def bad_handler(e):
            raise ValueError("bad")

        bus.subscribe(PipelineEventType.STEP_COMPLETE, bad_handler)
        # Should not raise.
        bus.publish(PipelineEvent(PipelineEventType.STEP_COMPLETE, "x"))

    def test_event_type_isolation(self):
        bus = EventBus()
        received: List[PipelineEvent] = []
        bus.subscribe(PipelineEventType.STEP_COMPLETE, received.append)
        bus.publish(PipelineEvent(PipelineEventType.STEP_START, "x"))
        assert received == []


# ---------------------------------------------------------------------------
# Pipeline tests
# ---------------------------------------------------------------------------


class TestPipeline:
    def test_single_step_runs(self):
        pipeline = Pipeline([IncrementStep()])
        result = pipeline.execute({})
        assert result["count"] == 1

    def test_multiple_steps_run_in_order(self):
        steps = [AppendStep("a"), AppendStep("b"), AppendStep("c")]
        result = Pipeline(steps).execute({})
        assert result["items"] == ["a", "b", "c"]

    def test_step_failure_raises(self):
        pipeline = Pipeline([IncrementStep(), FailingStep()])
        with pytest.raises(RuntimeError, match="Deliberate failure"):
            pipeline.execute({})

    def test_step_failure_publishes_error_event(self):
        errors: List[PipelineEvent] = []
        bus = EventBus()
        bus.subscribe(PipelineEventType.STEP_ERROR, errors.append)

        pipeline = Pipeline([FailingStep()], event_bus=bus)
        with pytest.raises(RuntimeError):
            pipeline.execute({})

        assert len(errors) == 1
        assert errors[0].step_name == "failing"

    def test_context_is_threaded_through_steps(self):
        steps = [IncrementStep(), IncrementStep(), IncrementStep()]
        result = Pipeline(steps).execute({"count": 10})
        assert result["count"] == 13

    def test_events_emitted_in_order(self):
        bus = EventBus()
        events: List[PipelineEventType] = []
        for et in PipelineEventType:
            bus.subscribe(et, lambda e, _et=et: events.append(e.event_type))

        Pipeline([IncrementStep()], event_bus=bus).execute({})

        assert events[0] == PipelineEventType.PIPELINE_START
        assert events[-1] == PipelineEventType.PIPELINE_COMPLETE

    def test_empty_pipeline_returns_context(self):
        ctx = {"key": "value"}
        result = Pipeline([]).execute(ctx)
        assert result == ctx


from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)


def test_tracing_creates_spans():

    exporter = InMemorySpanExporter()

    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))

    tracer = provider.get_tracer("test_agent")

    with tracer.start_as_current_span("research_workflow"):

        with tracer.start_as_current_span("researcher"):
            pass

        with tracer.start_as_current_span("analyst"):
            pass

    spans = exporter.get_finished_spans()

    assert len(spans) == 3

    names = [span.name for span in spans]

    assert "research_workflow" in names
    assert "researcher" in names
    assert "analyst" in names

    root_span = next(
        span for span in spans
        if span.name == "research_workflow"
    )

    child_spans = [
        span for span in spans
        if span.name in ("researcher", "analyst")
    ]

    for span in child_spans:
        assert span.context.trace_id == root_span.context.trace_id
        assert span.parent.span_id == root_span.context.span_id

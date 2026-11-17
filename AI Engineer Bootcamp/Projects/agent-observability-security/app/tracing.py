
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor
)


# Identify our application
resource = Resource.create({
    "service.name": "ai-agent-observability"
})


# Configure tracer provider
provider = TracerProvider(resource=resource)

# Export spans to terminal
exporter = ConsoleSpanExporter()

provider.add_span_processor(
    SimpleSpanProcessor(exporter)
)

# Register provider
trace.set_tracer_provider(provider)

# Create tracer
tracer = trace.get_tracer("agent_system")

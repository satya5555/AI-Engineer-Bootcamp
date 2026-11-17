
from app.agents import researcher, analyst, writer
from app.tracing import tracer


def main():

    topic = "AI in Healthcare"

    print("\nStarting AI Agent Workflow\n")

    with tracer.start_as_current_span("research_workflow") as span:

        span.set_attribute("workflow.name", "research_workflow")
        span.set_attribute("workflow.topic", topic)

        findings = researcher(topic)
        analysis = analyst(findings)
        report = writer(analysis)

        span.set_attribute("workflow.status", "completed")

    print("\nFinal Report:")
    print(report)


if __name__ == "__main__":
    main()

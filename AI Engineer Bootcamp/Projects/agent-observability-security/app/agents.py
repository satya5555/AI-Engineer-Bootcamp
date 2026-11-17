import logging
import json
import time
from datetime import datetime, timezone
from app.tracing import tracer
from opentelemetry.trace import Status, StatusCode

class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_data = {
            "timestamp": datetime.fromtimestamp(
                record.created, timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        return json.dumps(log_data)


# Configure JSON logging
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("agent_system")
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False



def researcher(topic):

    with tracer.start_as_current_span("researcher") as span:

        span.set_attribute("agent.name", "researcher")
        span.set_attribute("research.topic", topic)
        start_time = time.perf_counter()

        logger.info("Researcher started for topic: %s", topic)

        time.sleep(1)

        findings = [
            f"Finding 1 about {topic}",
            f"Finding 2 about {topic}",
            f"Finding 3 about {topic}"
        ]

        span.set_attribute("research.findings_count", len(findings))

        logger.info("Researcher completed successfully")
        span.set_attribute(
        "agent.duration_seconds",
        time.perf_counter() - start_time
)

        return findings



def analyst(findings):

    with tracer.start_as_current_span("analyst") as span:

        span.set_attribute("agent.name", "analyst")
        span.set_attribute("input.findings_count", len(findings))
        start_time = time.perf_counter()

        logger.info("Analyst started")

        try:
            time.sleep(1)

            if not findings:
                raise ValueError("No research findings provided")

            analysis = {
                "total_findings": len(findings),
                "summary": f"Analysed {len(findings)} research findings"
            }

            logger.info("Analyst completed successfully")
            span.set_attribute(
    "agent.duration_seconds",
    time.perf_counter() - start_time
)

            return analysis

        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))

            logger.error("Analyst failed: %s", e)

            raise


def writer(analysis):

    with tracer.start_as_current_span("writer") as span:

        span.set_attribute("agent.name", "writer")
        start_time = time.perf_counter()

        logger.info("Writer started")

        time.sleep(1)

        report = f"""
RESEARCH REPORT

{analysis['summary']}

Total findings: {analysis['total_findings']}
"""

        logger.info("Writer completed successfully")
        span.set_attribute(
    "agent.duration_seconds",
    time.perf_counter() - start_time
)

        return report

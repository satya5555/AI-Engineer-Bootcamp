
from google.adk.agents import SequentialAgent

from app.agents import researcher, analyst, writer

research_workflow = SequentialAgent(
    name="research_workflow",
    description="Researches a topic, analyzes findings, and creates a final report.",
    sub_agents=[
        researcher,
        analyst,
        writer
    ]
)


from google.adk.agents import LlmAgent, ParallelAgent

MODEL = "gemini-2.5-flash"

technology_agent = LlmAgent(
    name="technology_researcher",
    model=MODEL,
    instruction="""
    Research the important AI technologies used in healthcare.
    Explain their applications and give examples.
    """,
    output_key="technology_output"
)

benefits_agent = LlmAgent(
    name="benefits_researcher",
    model=MODEL,
    instruction="""
    Research the benefits of AI in healthcare.
    Explain improvements in diagnosis, treatment and efficiency.
    """,
    output_key="benefits_output"
)

challenges_agent = LlmAgent(
    name="challenges_researcher",
    model=MODEL,
    instruction="""
    Research the challenges of AI in healthcare.
    Consider privacy, bias, cost and reliability.
    """,
    output_key="challenges_output"
)

parallel_research = ParallelAgent(
    name="parallel_research",
    description="Researches healthcare AI from three perspectives.",
    sub_agents=[
        technology_agent,
        benefits_agent,
        challenges_agent
    ]
)

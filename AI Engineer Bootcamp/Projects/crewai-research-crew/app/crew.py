from crewai import Crew, Process

from app.agents import researcher, analyst, writer
from app.tasks import research_task, analysis_task, writing_task


research_crew = Crew(
    agents=[
        researcher,
        analyst,
        writer
    ],

    tasks=[
        research_task,
        analysis_task,
        writing_task
    ],

    process=Process.sequential,

    verbose=True
)
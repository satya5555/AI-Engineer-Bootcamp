from crewai import Task
from app.agents import researcher, analyst, writer


research_task = Task(
    description=(
        "Research the topic: {topic}. "
        "Search the web for relevant and reliable information. "
        "Collect important facts, applications, benefits, "
        "challenges and source URLs."
    ),

    expected_output=(
        "A detailed collection of research findings with "
        "source titles, URLs and relevant information."
    ),

    agent=researcher
)

analysis_task = Task(
    description=(
        "Analyze the research findings about {topic}. "
        "Identify major applications, benefits, challenges "
        "and emerging trends. Extract meaningful insights "
        "and provide evidence-based conclusions."
    ),

    expected_output=(
        "A structured analysis containing applications, "
        "benefits, challenges, emerging trends and conclusions."
    ),

    agent=analyst,

    context=[research_task]
)

writing_task = Task(
    description=(
        "Prepare a professional research report about {topic} "
        "using the research findings and analytical insights. "
        "Include an executive summary, introduction, major "
        "applications, benefits, challenges, emerging trends "
        "and conclusion. Preserve relevant source URLs. "
        "Do not introduce unsupported claims."
    ),

    expected_output=(
        "A complete, well-structured research report "
        "with an executive summary, detailed sections, "
        "conclusion and references."
    ),

    agent=writer,

    context=[research_task, analysis_task]
)
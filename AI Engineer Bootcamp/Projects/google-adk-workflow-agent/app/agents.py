
from google.adk.agents import LlmAgent

MODEL = "gemini-2.5-flash"

# Agent 1: Researcher
researcher = LlmAgent(
    name="researcher",
    model=MODEL,
    description="Researches a given topic and collects useful information.",
    instruction="""
Research the topic provided by the user.
Collect important facts, concepts, examples, and applications.
Organize your findings clearly.
""",
    output_key="research_output"
)

# Agent 2: Analyst
analyst = LlmAgent(
    name="analyst",
    model=MODEL,
    description="Analyzes research findings and identifies insights.",
    instruction="""
Analyze the following research findings:

{research_output}

Identify key insights, benefits, challenges, and practical applications.
Provide a structured analysis.
""",
    output_key="analysis_output"

)

# Agent 3: Writer
writer = LlmAgent(
    name="writer",
    model=MODEL,
    description="Creates a structured report from research and analysis.",
    instruction="""
Prepare a comprehensive research report using the following information.

Research findings:
{research_output}

Analysis:
{analysis_output}

Include:
1. Introduction
2. Key findings
3. Benefits
4. Challenges
5. Real-world applications
6. Conclusion
""",
    output_key="report_output"
)

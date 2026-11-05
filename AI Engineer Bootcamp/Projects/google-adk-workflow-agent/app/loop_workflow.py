from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools.tool_context import ToolContext

MODEL = "gemini-2.5-flash"


def approve_report(tool_context: ToolContext):
    """Approve the report and stop the loop."""

    tool_context.actions.escalate = True

    return {
        "status": "approved",
        "message": "Report approved successfully."
    }


writer_agent = LlmAgent(
    name="report_writer",
    model=MODEL,
    instruction="""
    You are a professional report writer.

    Create a short, well-structured report about the user's topic.

    If reviewer feedback is available in {review_feedback?},
use it to improve your report.

If no feedback is available, create the initial report
without assuming any previous review.

    Save the latest report in report_draft.
    """,
    output_key="report_draft"
)


reviewer_agent = LlmAgent(
    name="report_reviewer",
    model=MODEL,
    instruction="""
    You are a strict report reviewer.

    Review the report below:

    {report_draft}

    Check:
    1. Clarity
    2. Structure
    3. Completeness
    4. Accuracy of reasoning

    If the report meets these standards,
    call the approve_report tool.

    Otherwise, provide specific feedback for improvement.
    Save your feedback in review_feedback.
    """,
    tools=[approve_report],
    output_key="review_feedback"
)


report_loop = LoopAgent(
    name="report_improvement_loop",
    description="Improves a report through repeated review.",
    sub_agents=[
        writer_agent,
        reviewer_agent
    ],
    max_iterations=3
)
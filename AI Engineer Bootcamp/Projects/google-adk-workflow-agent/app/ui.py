import os
import asyncio
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
# Load environment variables before importing ADK agents
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path, override=True)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.workflow import research_workflow
from app.parallel_workflow import parallel_research
from app.loop_workflow import report_loop


async def run_workflow(agent, topic, app_name, initial_state=None):
    session_service = InMemorySessionService()

    user_id = "streamlit_user"
    session_id = "session_1"

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=initial_state or {}
    )

    runner = Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=topic)]
    )

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        pass

    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    return session.state


# Streamlit UI
st.set_page_config(
    page_title="Google ADK Workflow Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Google ADK Workflow Agent")

st.markdown(
    "Explore three AI agent workflow patterns powered by Google ADK."
)

workflow = st.sidebar.selectbox(
    "Choose an Agent Workflow",
    [
        "Sequential Research",
        "Parallel Research",
        "Iterative Report Generation"
    ]
)

st.subheader(workflow)

topic = st.text_input(
    "Enter your research topic",
    placeholder="Artificial Intelligence in Healthcare"
)

if st.button("Run AI Workflow", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:
        try:
            with st.spinner("AI agents are working..."):

                if workflow == "Sequential Research":
                    state = asyncio.run(
                        run_workflow(
                            research_workflow,
                            topic,
                            "sequential_app"
                        )
                    )

                elif workflow == "Parallel Research":
                    state = asyncio.run(
                        run_workflow(
                            parallel_research,
                            topic,
                            "parallel_app"
                        )
                    )

                else:
                    state = asyncio.run(
                        run_workflow(
                            report_loop,
                            topic,
                            "loop_app",
                            {
                                "review_feedback":
                                "No previous feedback. Create the initial report."
                            }
                        )
                    )

            st.success("Workflow completed successfully!")

            if workflow == "Sequential Research":
                st.subheader("Research Findings")
                st.write(state.get("research_output", "No output"))

                st.subheader("Analysis")
                st.write(state.get("analysis_output", "No output"))

                st.subheader("Final Report")
                st.write(state.get("report_output", "No output"))

            elif workflow == "Parallel Research":
                st.subheader("Technology Research")
                st.write(state.get("technology_output", "No output"))

                st.subheader("Benefits")
                st.write(state.get("benefits_output", "No output"))

                st.subheader("Challenges")
                st.write(state.get("challenges_output", "No output"))

            else:
                st.subheader("Final Improved Report")
                st.write(state.get("report_draft", "No report generated"))

                st.subheader("Review Feedback")
                st.write(state.get("review_feedback", "No feedback available"))

        except Exception as e:
            st.error(f"Workflow failed: {e}")
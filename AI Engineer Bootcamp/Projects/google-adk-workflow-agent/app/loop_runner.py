import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path, override=True)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.loop_workflow import report_loop


async def main():
    session_service = InMemorySessionService()

    app_name = "loop_report_app"
    user_id = "user_1"
    session_id = "session_1"

    await session_service.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id,
    state={
        "review_feedback": "No previous feedback. Create the initial report."
    }
)

    runner = Runner(
        agent=report_loop,
        app_name=app_name,
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="Artificial Intelligence in Healthcare"
            )
        ]
    )

    print("Starting report improvement workflow...\n")

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if event.is_final_response():
            print("Workflow completed.")

    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    print("\n========== FINAL REPORT ==========")
    print(session.state.get("report_draft", "No report generated."))

    print("\n========== REVIEW FEEDBACK ==========")
    print(session.state.get("review_feedback", "No feedback available."))


if __name__ == "__main__":
    asyncio.run(main())
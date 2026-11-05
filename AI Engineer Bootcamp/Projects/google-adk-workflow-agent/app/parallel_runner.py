
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.parallel_workflow import parallel_research

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path, override=True)
print("ENV path:", env_path)
print("API key loaded:", bool(os.getenv("GOOGLE_API_KEY")))
print("Vertex AI:", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY was not loaded.")

async def main():
    session_service = InMemorySessionService()

    app_name = "parallel_research_app"
    user_id = "user_1"
    session_id = "session_1"

    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )

    runner = Runner(
        agent=parallel_research,
        app_name=app_name,
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text="Research Artificial Intelligence in Healthcare"
            )
        ]
    )

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

    print("\n--- PARALLEL RESEARCH RESULTS ---")

    print("\nTechnology:")
    print(session.state.get("technology_output", "No output"))

    print("\nBenefits:")
    print(session.state.get("benefits_output", "No output"))

    print("\nChallenges:")
    print(session.state.get("challenges_output", "No output"))


if __name__ == "__main__":
    asyncio.run(main())

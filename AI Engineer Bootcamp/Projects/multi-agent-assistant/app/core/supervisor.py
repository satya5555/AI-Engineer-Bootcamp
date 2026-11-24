
from app.core.state import (
    create_initial_state,
    update_state,
    record_agent_activity,
    record_error
)

from app.core.memory import save_memory
from app.core.planner import create_dynamic_plan

from app.agents.researcher import research_agent
from app.agents.analyst import analyst_agent
from app.agents.writer import writer_agent


AGENTS = {
    "researcher": research_agent,
    "analyst": analyst_agent,
    "writer": writer_agent
}


def create_plan(state):
    """Create a dynamic execution plan."""

    plan = create_dynamic_plan(state["user_request"])

    update_state(state, {
        "plan": plan,
        "status": "planning_completed"
    })

    record_agent_activity(
        state,
        "supervisor",
        f"Created execution plan: {plan}"
    )

    return state



def execute_plan(state, agent_names):

    for agent_name in agent_names:

        if agent_name not in AGENTS:
            raise ValueError(
                f"Unknown agent: {agent_name}"
            )

        # Prepare input for standalone analysis.
        if agent_name == "analyst":
            if not state["research_findings"]:
                state["research_findings"] = [
                    state["user_request"]
                ]

        # Prepare input for standalone writing.
        if agent_name == "writer":
            if not state["research_findings"] and not state["analysis"]:
                state["research_findings"] = [
                    state["user_request"]
                ]

        state["current_agent"] = agent_name

        AGENTS[agent_name](state)

    return state


def run_workflow(user_request, human_approved=False):
    """Coordinate dynamically selected agents."""

    state = None

    try:
        # Step 1: Initialize state
        state = create_initial_state(user_request)

        # Step 2: Create dynamic plan
        create_plan(state)

        # Step 3: Separate writer from pre-approval agents
        plan = state["plan"]

        pre_approval_agents = [
            name for name in plan
            if name != "writer"
        ]

        # Step 4: Execute selected research and analysis agents
        execute_plan(state, pre_approval_agents)

        # Step 5: Human approval checkpoint
        update_state(state, {
            "status": "awaiting_approval",
            "current_agent": "supervisor"
        })

        record_agent_activity(
            state,
            "supervisor",
            "Workflow waiting for human approval"
        )

        if not human_approved:
            return state

        update_state(state, {
            "human_approved": True,
            "status": "approved"
        })

        # Step 6: Execute writer only if selected
        if "writer" in plan:
            execute_plan(state, ["writer"])

        else:
            update_state(state, {
                "status": "completed"
            })

        # Step 7: Save completed workflow
        save_memory(state)

        record_agent_activity(
            state,
            "supervisor",
            "Workflow completed successfully"
        )

        return state

    except Exception as error:

        if state is None:
            state = {
                "user_request": user_request,
                "status": "failed",
                "errors": [],
                "agent_history": [],
                "final_response": ""
            }

        record_error(
            state,
            state.get("current_agent") or "supervisor",
            error
        )

        return state



def resume_workflow(state, approved):
    """Resume a workflow after human approval."""

    if state["status"] != "awaiting_approval":
        raise ValueError(
            "Workflow is not waiting for approval"
        )

    if not approved:
        update_state(state, {
            "status": "rejected"
        })

        record_agent_activity(
            state,
            "supervisor",
            "Human rejected the workflow"
        )

        return state

    try:
        update_state(state, {
            "human_approved": True,
            "status": "in_progress"
        })

        # Execute the remaining agents selected in the plan.
        remaining_agents = [
            agent for agent in state["plan"]
            if agent not in [
                activity["agent"]
                for activity in state["agent_history"]
                if activity["agent"] != "supervisor"
            ]
        ]

        if remaining_agents:
            execute_plan(state, remaining_agents)

        update_state(state, {
            "status": "completed"
        })

        save_memory(state)

        record_agent_activity(
            state,
            "supervisor",
            "Workflow resumed and completed"
        )

        return state

    except Exception as error:
        record_error(
            state,
            state.get("current_agent") or "supervisor",
            error
        )

        return state

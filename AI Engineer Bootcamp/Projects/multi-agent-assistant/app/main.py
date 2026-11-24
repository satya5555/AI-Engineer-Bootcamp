from app.core.supervisor import run_workflow, resume_workflow


def main():
    print("\n===================================")
    print("       MULTI-AGENT ASSISTANT")
    print("===================================\n")

    request = input("What would you like me to research?\n> ")


    if not request.strip():
        print("\nPlease enter a valid request.")
        return

    # Start workflow
    print("\n[Supervisor] Starting workflow...")

    state = run_workflow(request)

    # Display research findings
    print("\n[Researcher] Research findings:")

    for finding in state["research_findings"]:
        print(f"- {finding}")

    # Display analysis
    print("\n[Analyst] Analysis:")
    print(state["analysis"])

    # Human approval
    print("\n[Supervisor] Workflow is waiting for approval.")

    approval = input(
        "\nDo you approve the findings? (yes/no): "
    ).strip().lower()

    approved = approval in ["yes", "y"]

    # Resume workflow
    state = resume_workflow(state, approved)

    if state["status"] == "completed":
        print("\n[Writer] Final Response:")
        print(state["final_response"])

    elif state["status"] == "rejected":
        print("\n[Supervisor] Workflow rejected by human.")

    else:
        print("\n[Supervisor] Workflow failed.")
        print(state["errors"])

    print("\n===================================")
    print("          WORKFLOW SUMMARY")
    print("===================================")

    print("Status:", state["status"])
    print("Human Approved:", state["human_approved"])
    print("Agents Executed:")

    for activity in state["agent_history"]:
        print(f"- {activity['agent']}: {activity['action']}")


if __name__ == "__main__":
    main()
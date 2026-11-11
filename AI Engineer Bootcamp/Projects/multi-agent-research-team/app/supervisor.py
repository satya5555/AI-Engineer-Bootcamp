
from app.agents import researcher, analyst, writer, reviewer


def run_research_team(topic, data):

    print("\n[Supervisor] Starting research team...")

    # Step 1: Researcher
    print("[Supervisor] Assigning task to Researcher")
    research = researcher(topic, data)

    # Step 2: Analyst
    print("[Supervisor] Sending findings to Analyst")
    analysis = analyst(research)

    # Step 3: Writer
    print("[Supervisor] Sending analysis to Writer")
    report = writer(analysis)

    # Step 4: Reviewer and revision loop
    max_attempts = 2
    review = None

    for attempt in range(max_attempts):

        print(f"\n[Supervisor] Review attempt {attempt + 1}")

        review = reviewer(report)

        print("[Supervisor] Reviewer feedback:", review["feedback"])

        if review["approved"]:
            print("[Supervisor] Report approved!")
            break

        if attempt < max_attempts - 1:
            print("[Supervisor] Requesting report revision...")

            report = writer(
                analysis,
                feedback=review["feedback"]
            )

    return {
        "research": research,
        "analysis": analysis,
        "report": report,
        "review": review
    }

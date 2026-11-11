
from concurrent.futures import ThreadPoolExecutor
import time

from app.agents import analyst, writer, reviewer


# Parallel research agents

def diagnosis_agent():
    print("[Diagnosis Agent] Researching medical diagnosis...")

    return [
        "AI helps detect diseases through medical image analysis.",
        "Machine learning predicts patient health risks."
    ]


def surgery_agent():
    print("[Surgery Agent] Researching robotic surgery...")

    return [
        "Robotic systems assist surgeons with precise procedures."
    ]


def drug_agent():
    print("[Drug Agent] Researching drug discovery...")

    return [
        "AI helps researchers identify potential treatments faster."
    ]


def run_hybrid_workflow():

    print("\n[Supervisor] Starting hybrid workflow...")

    start_time = time.time()

    # Stage 1: Parallel execution
    print("\n[Supervisor] Starting parallel research...")

    with ThreadPoolExecutor(max_workers=3) as executor:

        tasks = [
            executor.submit(diagnosis_agent),
            executor.submit(surgery_agent),
            executor.submit(drug_agent)
        ]

        results = [
            task.result()
            for task in tasks
        ]

    # Stage 2: Fan-in
    print("\n[Supervisor] Combining research findings...")

    combined_findings = []

    for result in results:
        combined_findings.extend(result)

    print("[Supervisor] Total findings:", len(combined_findings))

    # Stage 3: Sequential execution
    research = {
        "agent": "Researcher",
        "topic": "AI Healthcare",
        "findings": combined_findings
    }

    print("\n[Supervisor] Sending findings to Analyst")
    analysis = analyst(research)

    print("[Supervisor] Sending analysis to Writer")
    report = writer(analysis)

    print("[Supervisor] Sending report to Reviewer")
    review = reviewer(report)

    end_time = time.time()

    # Stage 4: Final output
    print("\n========== FINAL RESEARCH REPORT ==========\n")
    print(report["report"])

    print("\n========== REVIEW RESULT ==========")
    print("Approved:", review["approved"])
    print("Feedback:", review["feedback"])

    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    run_hybrid_workflow()

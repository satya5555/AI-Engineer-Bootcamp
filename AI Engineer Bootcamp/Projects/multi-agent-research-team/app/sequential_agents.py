
import time

from app.parallel_agents import (
    diagnosis_agent,
    surgery_agent,
    drug_agent
)


def run_sequential_agents():

    print("\n[Supervisor] Starting sequential agents...")

    start_time = time.time()

    # Execute agents one after another
    results = []

    results.append(diagnosis_agent())
    results.append(surgery_agent())
    results.append(drug_agent())

    end_time = time.time()

    print("\n[Supervisor] All agents completed.")

    print("\n========== COMBINED RESULTS ==========")

    for result in results:
        print(f"\n{result['agent']}:")
        print(result["finding"])

    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    run_sequential_agents()

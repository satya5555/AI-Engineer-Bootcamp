
from concurrent.futures import ThreadPoolExecutor
import time


def diagnosis_agent():
    print("[Diagnosis Agent] Researching AI in medical diagnosis...")
    time.sleep(2)

    return {
        "agent": "Diagnosis Agent",
        "finding": "AI helps detect diseases through medical image analysis."
    }


def surgery_agent():
    print("[Surgery Agent] Researching robotic surgery...")
    time.sleep(2)

    return {
        "agent": "Surgery Agent",
        "finding": "Robotic systems assist surgeons with precise procedures."
    }


def drug_agent():
    print("[Drug Agent] Researching drug discovery...")
    time.sleep(2)

    return {
        "agent": "Drug Agent",
        "finding": "AI helps identify potential treatments faster."
    }


def run_parallel_agents():

    print("\n[Supervisor] Starting parallel agents...")

    start_time = time.time()

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

    end_time = time.time()

    print("\n[Supervisor] All agents completed.")

    print("\n========== COMBINED RESULTS ==========")

    for result in results:
        print(f"\n{result['agent']}:")
        print(result["finding"])

    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    run_parallel_agents()

import time


def research_agent():
    print("[Research Agent] Executing...")

    # Simulate a temporary failure
    if not hasattr(research_agent, "attempts"):
        research_agent.attempts = 0

    research_agent.attempts += 1

    if research_agent.attempts < 3:
        raise Exception("Temporary research failure")

    return "Research completed successfully"


def run_with_retry(agent, max_retries=3):

    for attempt in range(1, max_retries + 1):

        try:
            print(f"\n[Supervisor] Attempt {attempt}")

            result = agent()

            print("[Supervisor] Agent succeeded!")
            return result

        except Exception as error:

            print("[Supervisor] Agent failed:", error)

            if attempt < max_retries:
                print("[Supervisor] Retrying...")
                time.sleep(1)

    print("\n[Supervisor] Maximum retries reached.")
    return None


def main():

    result = run_with_retry(research_agent)

    print("\nFinal result:", result)


if __name__ == "__main__":
    main()
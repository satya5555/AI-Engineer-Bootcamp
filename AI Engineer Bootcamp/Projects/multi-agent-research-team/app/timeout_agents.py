from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time


def research_agent():
    print("[Research Agent] Starting research...")

    time.sleep(5)

    return "Research completed successfully"


def run_agent_with_timeout(agent, timeout=2):

    with ThreadPoolExecutor(max_workers=1) as executor:

        task = executor.submit(agent)

        try:
            result = task.result(timeout=timeout)

            print("[Supervisor] Agent completed:", result)

        except TimeoutError:
            print("[Supervisor] Agent timed out!")
            task.cancel()


def main():

    print("[Supervisor] Starting agent...")

    start = time.time()

    run_agent_with_timeout(research_agent, timeout=2)

    print(
        f"\nTotal execution time: {time.time() - start:.2f} seconds"
    )


if __name__ == "__main__":
    main()
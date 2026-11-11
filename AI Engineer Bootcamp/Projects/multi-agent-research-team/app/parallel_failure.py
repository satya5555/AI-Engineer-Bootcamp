from concurrent.futures import ThreadPoolExecutor, as_completed


def diagnosis_agent():
    return "Diagnosis research completed"


def surgery_agent():
    raise Exception("Surgery research failed")


def drug_agent():
    return "Drug discovery research completed"


def main():

    agents = {
        "Diagnosis": diagnosis_agent,
        "Surgery": surgery_agent,
        "Drug Discovery": drug_agent
    }

    results = {}

    with ThreadPoolExecutor(max_workers=3) as executor:

        tasks = {
            executor.submit(agent): name
            for name, agent in agents.items()
        }

        for task in as_completed(tasks):

            name = tasks[task]

            try:
                results[name] = task.result()
                print(f"[Supervisor] {name}: SUCCESS")

            except Exception as error:
                results[name] = None
                print(f"[Supervisor] {name}: FAILED - {error}")

    print("\n========== FINAL RESULTS ==========")

    for name, result in results.items():
        print(name, ":", result)

    successful = sum(
        result is not None
        for result in results.values()
    )

    print(f"\nSuccessful agents: {successful}/{len(agents)}")


if __name__ == "__main__":
    main()
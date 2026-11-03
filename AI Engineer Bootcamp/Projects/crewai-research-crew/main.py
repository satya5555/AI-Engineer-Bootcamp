from app.crew import research_crew


def main():
    topic = input("Enter your research topic: ")

    if not topic.strip():
        print("Please enter a valid research topic.")
        return

    print("\nStarting AI Research Crew...\n")

    result = research_crew.kickoff(
        inputs={"topic": topic}
    )

    print("\n" + "=" * 70)
    print("FINAL RESEARCH REPORT")
    print("=" * 70)

    print(result)


if __name__ == "__main__":
    main()
def research_agent():
    print("\n[Research Agent] Preparing solution...")

    return {
        "solution": "AI can help hospitals improve patient care."
    }


def critic_agent(solution):
    print("\n[Critic Agent] Reviewing solution...")

    feedback = []

    if len(solution) < 100:
        feedback.append("Add more details.")

    if "examples" not in solution.lower():
        feedback.append("Include practical examples.")

    return feedback


def improvement_agent(solution, feedback):
    print("\n[Improvement Agent] Improving solution...")

    improved = solution

    if "Add more details." in feedback:
        improved += (
            " AI systems can analyse medical images "
            "and help doctors identify diseases."
        )

    if "Include practical examples." in feedback:
        improved += (
            " Examples include medical image analysis "
            "and patient risk prediction."
        )

    return improved


def main():
    proposal = research_agent()

    solution = proposal["solution"]

    feedback = critic_agent(solution)

    print("\nFeedback:", feedback)

    improved_solution = improvement_agent(
        solution,
        feedback
    )

    print("\n========== IMPROVED SOLUTION ==========")
    print(improved_solution)


if __name__ == "__main__":
    main()
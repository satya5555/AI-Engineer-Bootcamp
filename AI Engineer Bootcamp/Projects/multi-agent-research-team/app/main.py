
from pathlib import Path

from app.supervisor import run_research_team


def load_data():
    file_path = Path(__file__).parent.parent / "data" / "research_data.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def main():
    topic = input("Enter your research topic: ")

    data = load_data()

    result = run_research_team(topic, data)

    print("\n========== RESEARCH REPORT ==========\n")
    print(result["report"]["report"])

    print("\n========== REVIEW RESULT ==========\n")
    print("Approved:", result["review"]["approved"])
    print("Feedback:", result["review"]["feedback"])


if __name__ == "__main__":
    main()

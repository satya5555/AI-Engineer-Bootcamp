from app.utility import AIUtility


def main():
    ai = AIUtility()

    text = """
    My laptop has been extremely slow since yesterday.
    Applications take several minutes to open and sometimes
    freeze completely.
    """

    print("=" * 60)
    print("AI UTILITY")
    print("=" * 60)

    print("\n--- SUMMARY ---")
    print(ai.summarize(text))

    print("\n--- REWRITE ---")
    print(ai.rewrite(text))

    print("\n--- CLASSIFICATION ---")
    print(ai.classify(text))

    print("\n--- TICKET ANALYSIS ---")
    analysis = ai.analyze_ticket(text)

    print(f"Category: {analysis.category}")
    print(f"Priority: {analysis.priority}")
    print(f"Summary: {analysis.summary}")
    print(f"Sentiment: {analysis.sentiment}")


if __name__ == "__main__":
    main()
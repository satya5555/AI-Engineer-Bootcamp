knowledge_base = [
    {
        "topic": "healthcare AI",
        "content": "AI can help doctors analyze medical images."
    },
    {
        "topic": "healthcare AI",
        "content": "Predictive models can help identify patients at risk."
    },
    {
        "topic": "healthcare AI",
        "content": "AI-powered systems can automate administrative tasks."
    },
    {
        "topic": "healthcare AI",
        "content": "Data privacy and model accuracy are major challenges."
    }
]


def search_knowledge(query, limit=5):
    """Search the local knowledge base using keyword matching."""

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty")

    words = {
        word.lower().strip(".,?!")
        for word in query.split()
        if len(word) > 2
    }

    results = []

    for item in knowledge_base:
        text = (item["topic"] + " " + item["content"]).lower()

        if any(word in text for word in words):
            results.append(item)

    return results[:limit]
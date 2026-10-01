class Researcher:
    def __init__(self, search):
        self.search = search

    def research(self, question, max_results=5):
        results = self.search.search(
            question,
            max_results=max_results
        )

        evidence = []

        for result in results:
            evidence.append({
                "title": result["title"],
                "url": result["url"],
                "snippet": result["snippet"]
            })

        return evidence
class DocumentRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def search(
        self,
        question: str,
        k: int = 4,
        max_distance: float = 0.70
    ):
        results = self.vector_store.similarity_search_with_score(
            question,
            k=k
        )

        filtered_results = []

        for document, score in results:
            if score <= max_distance:
                filtered_results.append(
                    (document, score)
                )

        return filtered_results
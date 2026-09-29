class HybridSearch:

    def __init__(self, keyword_search, semantic_search):
        self.keyword_search = keyword_search
        self.semantic_search = semantic_search

    def search(self, question, k=4, min_score=0.02):

        keyword_docs = self.keyword_search.search(
            question,
            k=6
        )

        semantic_docs = self.semantic_search.search(
            question
        )

        scores = {}
        documents = {}

        # BM25 contribution
        for rank, document in enumerate(keyword_docs):

            key = document.page_content

            if key not in scores:
                scores[key] = {
                    "rrf_score": 0,
                    "keyword_score": 0,
                    "semantic_score": 0
                }

            score = 1 / (60 + rank + 1)

            scores[key]["keyword_score"] = score
            scores[key]["rrf_score"] += score

            documents[key] = document

        # Semantic contribution
        for rank, document in enumerate(semantic_docs):

            key = document.page_content

            if key not in scores:
                scores[key] = {
                    "rrf_score": 0,
                    "keyword_score": 0,
                    "semantic_score": 0
                }

            score = 1 / (60 + rank + 1)

            scores[key]["semantic_score"] = score
            scores[key]["rrf_score"] += score

            documents[key] = document

        # Rank documents
        ranked = sorted(
            scores.keys(),
            key=lambda key: scores[key]["rrf_score"],
            reverse=True
        )

        results = []

        for key in ranked:

            score = scores[key]["rrf_score"]

            if score < min_score:
                continue

            results.append({
                "document": documents[key],
                "rrf_score": score,
                "keyword_score": scores[key]["keyword_score"],
                "semantic_score": scores[key]["semantic_score"]
            })

            if len(results) >= k:
                break

        return results
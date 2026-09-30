class Evaluator:

    def __init__(self, hybrid_search, chat):
        self.hybrid_search = hybrid_search
        self.chat = chat

    def evaluate_question(self, question):

        results = self.hybrid_search.search(
            question,
            k=4
        )

        answer, sources = self.chat.answer(
            question,
            results
        )

        return {
            "question": question,
            "answer": answer,
            "results": results,
            "sources": sources
        }
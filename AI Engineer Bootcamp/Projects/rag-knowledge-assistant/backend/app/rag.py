from app.retriever import Retriever
from app.generator import Generator


class RAGPipeline:

    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()

    def ask(self, question):

        documents, distances = self.retriever.search(
            question
        )

        if not documents:
            return {
                "answer": "No relevant information was found.",
                "sources": [],
                "distances": []
            }

        answer = self.generator.generate(
            question,
            documents
        )

        return {
            "answer": answer,
            "sources": documents,
            "distances": distances
        }
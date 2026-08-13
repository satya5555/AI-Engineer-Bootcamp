import chromadb

from app.config import CHROMA_PATH, COLLECTION_NAME


class Retriever:

    def __init__(self):
        client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = client.get_collection(
            name=COLLECTION_NAME
        )

    def search(self, question, n_results=2):
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )

        documents = results["documents"][0]
        distances = results["distances"][0]

        print("\nDEBUG - Retrieved Documents:")
        for i, document in enumerate(documents):
            print(f"\nDocument {i + 1}:")
            print(repr(document))
            print(f"Distance: {distances[i]:.4f}")

        return documents, distances
class SemanticSearch:

    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever(
            search_kwargs={"k": 4}
        )

    def search(self, question):
        return self.retriever.invoke(question)
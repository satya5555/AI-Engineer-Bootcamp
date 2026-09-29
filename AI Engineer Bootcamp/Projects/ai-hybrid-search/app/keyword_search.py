from langchain_community.retrievers import BM25Retriever


class KeywordSearch:

    def __init__(self, documents):
        self.retriever = BM25Retriever.from_documents(documents)

    def search(self, question, k=4):
        self.retriever.k = k
        return self.retriever.invoke(question)
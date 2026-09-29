from langchain_core.documents import Document

from app.keyword_search import KeywordSearch
from app.vectorstore import VectorStore
from app.semantic_search import SemanticSearch


documents = [
    Document(
        page_content="Python is widely used for artificial intelligence and machine learning."
    ),
    Document(
        page_content="Java is commonly used for enterprise applications."
    ),
    Document(
        page_content="ERR-502 indicates a payment service failure."
    ),
    Document(
        page_content="Customer ID CUST-84721 reported a payment issue."
    )
]


# Keyword search
keyword_search = KeywordSearch(documents)


# Semantic search
vector_store = VectorStore()
semantic_search = SemanticSearch(vector_store.get_store())


questions = [
    "Python machine learning",
    "ERR-502",
    "CUST-84721",
    "Why was the payment service failing?",
    "What happened with the customer payment?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUERY:", question)
    print("=" * 70)

    print("\n--- BM25 KEYWORD SEARCH ---")

    keyword_results = keyword_search.search(question, k=2)

    for index, document in enumerate(keyword_results):
        print(f"{index + 1}. {document.page_content}")

    print("\n--- SEMANTIC SEARCH ---")

    semantic_results = semantic_search.search(question)

    for index, document in enumerate(semantic_results[:2]):
        print(f"{index + 1}. {document.page_content}")
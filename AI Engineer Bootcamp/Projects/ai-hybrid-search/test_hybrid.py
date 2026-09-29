from langchain_core.documents import Document

from app.keyword_search import KeywordSearch
from app.vectorstore import VectorStore
from app.semantic_search import SemanticSearch
from app.hybrid_search import HybridSearch
from app.chat import RAGChat

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


# BM25
keyword_search = KeywordSearch(documents)


# Semantic
vector_store = VectorStore()
semantic_search = SemanticSearch(
    vector_store.get_store()
)


# Hybrid
hybrid_search = HybridSearch(
    keyword_search,
    semantic_search
)


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

    results = hybrid_search.search(
    question,
    k=3
)

    for index, result in enumerate(results):

        document = result["document"]

        print(
            f"{index + 1}. "
            f"{document.page_content}"
        )

        print(
            f"   RRF:      {result['rrf_score']:.6f}"
        )

        print(
            f"   BM25:     {result['keyword_score']:.6f}"
        )

        print(
            f"   Semantic: {result['semantic_score']:.6f}"
        )
chat = RAGChat()

answer = chat.answer(
            question,
            results
        )

print("\nANSWER:")
print(answer)
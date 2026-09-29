from langchain_core.documents import Document

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


vector_store = VectorStore()
vector_store.add_documents(documents)

search = SemanticSearch(vector_store.get_store())

questions = [
    "Python machine learning",
    "Why was the payment service failing?",
    "What happened with the customer payment?",
    "What technology is used for AI?"
]

for question in questions:

    print("\n" + "=" * 60)
    print("QUERY:", question)
    print("=" * 60)

    results = search.search(question)

    for index, document in enumerate(results):
        print(f"{index + 1}. {document.page_content}")
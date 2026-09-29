from langchain_core.documents import Document
from app.keyword_search import KeywordSearch


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


search = KeywordSearch(documents)

questions = [
    "Python machine learning",
    "ERR-502",
    "CUST-84721",
    "payment service failure"
]

for question in questions:

    print("\n" + "=" * 60)
    print("QUERY:", question)
    print("=" * 60)

    results = search.search(question, k=2)

    for index, document in enumerate(results):
        print(f"{index + 1}. {document.page_content}")
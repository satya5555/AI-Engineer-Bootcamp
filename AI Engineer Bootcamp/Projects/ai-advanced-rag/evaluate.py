from app.vectorstore import VectorStore
from app.retriever import DocumentRetriever


vector_store = VectorStore()

retriever = DocumentRetriever(
    vector_store.get_store()
)


questions = [
    "Doctor details?",
    "What department does the doctor belong to?",
    "What information is provided about the patient?",
    "What is the main purpose of the document?",
    "What is the patient's favorite programming language?",
    "What is the recipe for pasta?"
]


k_values = [2, 4, 6]


for question in questions:

    print("\n" + "=" * 70)
    print(f"QUESTION: {question}")
    print("=" * 70)

    for k in k_values:

        results = retriever.search(
            question,
            k=k,
            max_distance=0.70
        )

        print(
            f"\nk={k} → "
            f"{len(results)} relevant chunks"
        )

        for index, (document, score) in enumerate(results):

            page = document.metadata.get(
                "page",
                0
            ) + 1

            print(
                f"  {index + 1}. "
                f"Page {page}, "
                f"distance={score:.4f}"
            )
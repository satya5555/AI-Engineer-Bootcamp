from app.vectorstore import VectorStore
from app.retriever import DocumentRetriever
from app.chat import RAGChat


# Load existing vector database
vector_store = VectorStore()

retriever = DocumentRetriever(
    vector_store.get_store()
)


# Get user question
question = input("\nAsk a question: ")


# Retrieve relevant documents
results = retriever.search(
    question,
    k=4,
    max_distance=0.70
)


# Handle retrieval failure
if not results:
    print("\nNo sufficiently relevant documents found.")

    chat = RAGChat()

    answer, sources = chat.answer(
        question,
        []
    )

else:
    print(
        f"\nRelevant documents found: {len(results)}"
    )

    # Generate answer
    chat = RAGChat()

    answer, sources = chat.answer(
        question,
        results
    )


# Normalize Gemini response
if isinstance(answer, list):
    text_parts = []

    for item in answer:
        if isinstance(item, dict):
            text = item.get("text")

            if text:
                text_parts.append(text)

    answer = "\n".join(text_parts)


# Display answer
print("\n" + "=" * 60)
print("ANSWER")
print("=" * 60)

print(answer)


# Display sources
print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)

if sources:
    for source in sources:
        print(
            f"Page {source['page']} "
            f"(distance: {source['score']:.4f})"
        )
else:
    print("No sources available.")
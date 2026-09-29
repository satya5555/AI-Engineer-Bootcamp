from pathlib import Path

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore
from app.keyword_search import KeywordSearch
from app.semantic_search import SemanticSearch
from app.hybrid_search import HybridSearch
from app.chat import RAGChat


# --------------------------------------------------
# 1. Load PDF
# --------------------------------------------------

pdf_path = Path(__file__).parent / "documents" / "sample.pdf"

loader = PDFLoader()
documents = loader.load(str(pdf_path))

print(f"Pages loaded: {len(documents)}")


# --------------------------------------------------
# 2. Split document
# --------------------------------------------------

splitter = TextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split(documents)

print(f"Chunks available: {len(chunks)}")


# --------------------------------------------------
# 3. Keyword search
# --------------------------------------------------

keyword_search = KeywordSearch(chunks)


# --------------------------------------------------
# 4. Semantic search
# --------------------------------------------------

vector_store = VectorStore()

semantic_search = SemanticSearch(
    vector_store.get_store()
)


# --------------------------------------------------
# 5. Hybrid search
# --------------------------------------------------

hybrid_search = HybridSearch(
    keyword_search,
    semantic_search
)


# --------------------------------------------------
# 6. Ask question
# --------------------------------------------------

question = input("\nAsk a question: ")


results = hybrid_search.search(
    question,
    k=4,
    min_score=0.03
)


# --------------------------------------------------
# 7. Display retrieval results
# --------------------------------------------------

print("\n" + "=" * 70)
print("HYBRID SEARCH RESULTS")
print("=" * 70)

if not results:

    print("No relevant documents found.")

else:

    for index, result in enumerate(results):

        document = result["document"]

        page = document.metadata.get(
            "page",
            0
        ) + 1

        print(
            f"\n{index + 1}. Page {page}"
        )

        print(
            f"   {document.page_content[:250]}"
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


# --------------------------------------------------
# 8. Generate answer
# --------------------------------------------------

chat = RAGChat()

answer, sources = chat.answer(
    question,
    results
)


# --------------------------------------------------
# 9. Display answer
# --------------------------------------------------

print("\n" + "=" * 70)
print("ANSWER")
print("=" * 70)

print(answer)
print("\n" + "=" * 70)
print("SOURCES")
print("=" * 70)

if sources:

    for source in sources:

        print(
            f"Page {source['page']} | "
            f"RRF: {source['rrf_score']:.6f}"
        )

else:

    print("No sources available.")
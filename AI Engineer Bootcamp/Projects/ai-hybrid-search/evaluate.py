from pathlib import Path

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore
from app.keyword_search import KeywordSearch
from app.semantic_search import SemanticSearch
from app.hybrid_search import HybridSearch


# --------------------------------------------------
# Load document
# --------------------------------------------------

pdf_path = Path(__file__).parent / "documents" / "sample.pdf"

loader = PDFLoader()
documents = loader.load(str(pdf_path))

splitter = TextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split(documents)


# --------------------------------------------------
# Create retrievers
# --------------------------------------------------

keyword_search = KeywordSearch(chunks)

vector_store = VectorStore()

semantic_search = SemanticSearch(
    vector_store.get_store()
)

hybrid_search = HybridSearch(
    keyword_search,
    semantic_search
)


# --------------------------------------------------
# Evaluation questions
# --------------------------------------------------

questions = [
    "What is the main topic of the document?",
    "What information is provided about the document?",
    "Give me an exact name or identifier from the document.",
    "Explain the main idea in simple words.",
    "What is the recipe for pasta?"
]


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

for question in questions:

    print("\n" + "=" * 80)
    print("QUESTION:", question)
    print("=" * 80)

    print("\n--- BM25 ---")

    keyword_results = keyword_search.search(
        question,
        k=3
    )

    for index, document in enumerate(keyword_results):

        page = document.metadata.get(
            "page",
            0
        ) + 1

        print(
            f"{index + 1}. Page {page}: "
            f"{document.page_content[:150]}"
        )

    print("\n--- SEMANTIC ---")

    semantic_results = semantic_search.search(
        question
    )

    for index, document in enumerate(
        semantic_results[:3]
    ):

        page = document.metadata.get(
            "page",
            0
        ) + 1

        print(
            f"{index + 1}. Page {page}: "
            f"{document.page_content[:150]}"
        )

    print("\n--- HYBRID ---")

    hybrid_results = hybrid_search.search(
        question,
        k=3
    )

    for index, result in enumerate(
        hybrid_results
    ):

        document = result["document"]

        page = document.metadata.get(
            "page",
            0
        ) + 1

        print(
            f"{index + 1}. Page {page}: "
            f"{document.page_content[:150]}"
        )

        print(
            f"   RRF={result['rrf_score']:.6f}"
        )
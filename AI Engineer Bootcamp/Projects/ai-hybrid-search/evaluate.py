import json
from pathlib import Path

from app.evaluator import Evaluator

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore
from app.keyword_search import KeywordSearch
from app.semantic_search import SemanticSearch
from app.hybrid_search import HybridSearch
from app.chat import RAGChat
from app.metrics import keyword_match, retrieval_hit
from app.metrics import (
    keyword_match,
    answer_match,
    retrieval_hit,
    refusal_match,
    classify_result
)

# ---------------------------------------------
# 1. Load evaluation questions
# ---------------------------------------------

questions_path = Path("evaluation_questions.json")

with open(
    questions_path,
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


# ---------------------------------------------
# 2. Load PDF
# ---------------------------------------------

pdf_path = Path("documents/sample.pdf")

loader = PDFLoader()

documents = loader.load(
    str(pdf_path)
)

print(f"Pages loaded: {len(documents)}")


# ---------------------------------------------
# 3. Split PDF
# ---------------------------------------------

splitter = TextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split(
    documents
)

print(f"Chunks created: {len(chunks)}")


# ---------------------------------------------
# 4. Create retrieval components
# ---------------------------------------------

keyword_search = KeywordSearch(
    chunks
)

vector_store = VectorStore()

semantic_search = SemanticSearch(
    vector_store.get_store()
)

hybrid_search = HybridSearch(
    keyword_search,
    semantic_search
)


# ---------------------------------------------
# 5. Create chat
# ---------------------------------------------

chat = RAGChat()


# ---------------------------------------------
# 6. Create evaluator
# ---------------------------------------------

evaluator = Evaluator(
    hybrid_search,
    chat
)


# ---------------------------------------------
# 7. Run evaluation
# ---------------------------------------------

from app.metrics import (
    keyword_match,
    answer_match,
    retrieval_hit
)

retrieval_scores = []
keyword_scores = []
answer_scores = []

for item in questions:
    question = item["question"]
    expected_answer = item["expected_answer"]
    expected_keywords = item["expected_keywords"]

    print("\n" + "=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)

    result = evaluator.evaluate_question(question)

    retrieval_score = retrieval_hit(
        result["results"],
        expected_keywords
    )

    keyword_score = keyword_match(
        result["answer"],
        expected_keywords
    )

    if expected_keywords:
        answer_score = answer_match(
            result["answer"],
            expected_answer
    )
    else:
        answer_score = refusal_match(
        result["answer"],
        expected_answer
    )

    print("\nANSWER")
    print("-" * 80)
    print(result["answer"])

    print("\nEVALUATION")
    print("-" * 80)
    print(
        f"Retrieval Hit: "
        f"{retrieval_score if retrieval_score is not None else 'N/A'}"
    )
    print(
        f"Keyword Match: "
        f"{keyword_score if keyword_score is not None else 'N/A'}"
    )
    print(f"Answer Match:  {answer_score:.2f}")

    if retrieval_score is not None:
        retrieval_scores.append(retrieval_score)

    if keyword_score is not None:
        keyword_scores.append(keyword_score)

    answer_scores.append(answer_score)
    is_unsupported = len(expected_keywords) == 0

    result_type = classify_result(
        retrieval_score,
        answer_score,
        is_unsupported
    )

    print(f"Result Type:   {result_type}")

    print("\nRETRIEVED SOURCES")
    print("-" * 80)

    if result["sources"]:
        for source in result["sources"]:
            print(
                f"Page {source['page']} | "
                f"RRF: {source['rrf_score']:.6f}"
            )
    else:
        print("No sources found.")


print("\n" + "=" * 80)
print("EVALUATION SUMMARY")
print("=" * 80)

if retrieval_scores:
    retrieval_avg = sum(retrieval_scores) / len(retrieval_scores)
    print(f"Average Retrieval Hit: {retrieval_avg:.2f}")

if keyword_scores:
    keyword_avg = sum(keyword_scores) / len(keyword_scores)
    print(f"Average Keyword Match:  {keyword_avg:.2f}")

answer_avg = sum(answer_scores) / len(answer_scores)
print(f"Average Answer Match:   {answer_avg:.2f}")
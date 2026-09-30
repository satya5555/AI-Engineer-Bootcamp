import re


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def keyword_match(answer, expected_keywords):
    if not expected_keywords:
        return None

    answer_text = normalize_text(answer)

    matched = 0

    for keyword in expected_keywords:
        if normalize_text(keyword) in answer_text:
            matched += 1

    return matched / len(expected_keywords)


def answer_match(answer, expected_answer):
    answer_text = normalize_text(answer)
    expected_text = normalize_text(expected_answer)

    if expected_text in answer_text:
        return 1.0

    expected_words = set(expected_text.split())

    if not expected_words:
        return 0.0

    answer_words = set(answer_text.split())
    matched_words = expected_words.intersection(answer_words)

    return len(matched_words) / len(expected_words)


def retrieval_hit(results, expected_keywords):
    if not expected_keywords:
        return None

    for result in results:
        text = normalize_text(
            result["document"].page_content
        )

        if any(
            normalize_text(keyword) in text
            for keyword in expected_keywords
        ):
            return 1.0

    return 0.0
def refusal_match(answer, expected_answer):
    answer_text = normalize_text(answer)
    expected_text = normalize_text(expected_answer)

    refusal_phrases = [
        "could not find",
        "couldn't find",
        "not available",
        "information is not available",
        "information not found"
    ]

    answer_refuses = any(
        phrase in answer_text
        for phrase in refusal_phrases
    )

    expected_refuses = any(
        phrase in expected_text
        for phrase in refusal_phrases
    )

    return 1.0 if answer_refuses == expected_refuses else 0.0
def classify_result(
    retrieval_score,
    answer_score,
    is_unsupported=False
):
    if is_unsupported:
        if answer_score == 1.0:
            return "UNSUPPORTED_QUERY_HANDLED"
        return "UNSUPPORTED_QUERY_FAILURE"

    if retrieval_score == 0.0:
        return "RETRIEVAL_FAILURE"

    if answer_score < 1.0:
        return "GENERATION_FAILURE"

    return "PASS"
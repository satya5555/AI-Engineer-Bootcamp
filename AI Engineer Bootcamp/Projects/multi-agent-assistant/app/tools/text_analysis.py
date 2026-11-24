def analyze_text(text):
    """Calculate basic text statistics."""

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    words = text.split()
    sentences = [
        item for item in text.split(".") if item.strip()
    ]

    return {
        "character_count": len(text),
        "word_count": len(words),
        "sentence_count": len(sentences)
    }
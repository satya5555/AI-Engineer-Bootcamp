from langchain_core.documents import Document

from app.chunker import TextChunker


with open(
    "documents/sample.txt",
    "r",
    encoding="utf-8"
) as file:
    text = file.read()


document = Document(
    page_content=text,
    metadata={
        "source": "documents/sample.txt"
    }
)

chunker = TextChunker(
    chunk_size=300,
    chunk_overlap=100
)

chunks = chunker.split(
    [document]
)

print(f"Original characters: {len(text)}")
print(f"Chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks):

    print("\n" + "=" * 60)

    print(f"Chunk {index + 1}")
    print(f"Characters: {len(chunk.page_content)}")

    print("\nContent:")
    print(chunk.page_content)
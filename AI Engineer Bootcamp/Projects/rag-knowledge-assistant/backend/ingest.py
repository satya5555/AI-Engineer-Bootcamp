import chromadb


KNOWLEDGE_BASE_PATH = "data/knowledge_base.txt"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "company_knowledge_v2"


def load_knowledge_base():
    with open(
        KNOWLEDGE_BASE_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        content = file.read()

    chunks = [
        block.strip()
        for block in content.split("\n\n")
        if block.strip()
    ]

    return chunks


def create_collection():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
        print("\nOld collection removed.")
    except Exception:
        pass

    return client.create_collection(
        name=COLLECTION_NAME
    )


def main():
    print("=" * 60)
    print("RAG Knowledge Base Ingestion")
    print("=" * 60)

    chunks = load_knowledge_base()

    print(f"\nCreated {len(chunks)} chunks.")

    collection = create_collection()

    collection.add(
        documents=chunks,
        ids=[
            f"chunk_{i}"
            for i in range(len(chunks))
        ]
    )

    print(
        f"Documents in collection: "
        f"{collection.count()}"
    )

    print("\nChunks:")

    for i, chunk in enumerate(
        chunks,
        start=1
    ):
        print(f"\n--- Chunk {i} ---")
        print(chunk)


if __name__ == "__main__":
    main()
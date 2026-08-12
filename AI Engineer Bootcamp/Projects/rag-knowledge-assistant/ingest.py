import chromadb


def load_knowledge_base():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        content = file.read()

    return [
        chunk.strip()
        for chunk in content.split("\n\n")
        if chunk.strip()
    ]


def create_collection():
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    return client.get_or_create_collection(
        name="company_knowledge_v2"
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
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    print(f"Documents in collection: {collection.count()}")

    print("\nChunks:")
    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)


if __name__ == "__main__":
    main()
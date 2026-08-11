import chromadb


def load_documents():
    with open("documents.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()


def create_collection(client):
    return client.get_or_create_collection(
        name="semantic_documents"
    )


def add_documents(collection, documents):
    existing = collection.count()

    if existing == 0:
        collection.add(
            documents=documents,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        print(f"Added {len(documents)} documents to ChromaDB.")
    else:
        print(f"Collection already contains {existing} documents.")


def search_documents(collection, query):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"][0]


def main():
    print("=" * 60)
    print("ChromaDB Semantic Search Engine")
    print("=" * 60)

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = create_collection(client)

    documents = load_documents()

    add_documents(collection, documents)

    print(f"\nTotal documents: {collection.count()}")
    print("\nType 'exit' to quit.")

    while True:
        query = input("\nSearch: ")

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        results = search_documents(
            collection,
            query
        )

        print("\nTop Results:\n")

        for rank, document in enumerate(results, start=1):
            print(f"{rank}. {document}")


if __name__ == "__main__":
    main()
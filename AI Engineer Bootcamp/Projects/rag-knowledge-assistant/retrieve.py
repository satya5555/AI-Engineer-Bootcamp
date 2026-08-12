import chromadb


def create_collection():
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    return client.get_collection(
    name="company_knowledge_v2"
)


def search(collection, query):
    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    return results["documents"][0]


def main():
    collection = create_collection()

    query = input("Ask a question: ")

    results = search(collection, query)

    print("\nRetrieved Context:")
    print("-" * 60)
    print(results[0])


if __name__ == "__main__":
    main()
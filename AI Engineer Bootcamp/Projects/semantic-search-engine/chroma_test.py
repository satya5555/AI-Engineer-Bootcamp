import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents_with_metadata"
)
documents = [
    "Python is a popular programming language used for AI and web development.",
    "Artificial Intelligence is transforming healthcare by improving diagnosis and treatment.",
    "Dogs are loyal animals and are often called man's best friend.",
    "Electric vehicles are becoming increasingly popular around the world.",
    "Cloud computing allows businesses to scale applications efficiently.",
    "Machine Learning is a subset of Artificial Intelligence.",
    "Cybersecurity protects systems from digital attacks.",
    "Git is a distributed version control system.",
    "Docker helps developers package applications into containers.",
    "Kubernetes manages containerized applications at scale."
]
metadatas = [
    {"category": "programming"},
    {"category": "artificial-intelligence"},
    {"category": "animals"},
    {"category": "vehicles"},
    {"category": "cloud"},
    {"category": "artificial-intelligence"},
    {"category": "cybersecurity"},
    {"category": "programming"},
    {"category": "cloud"},
    {"category": "cloud"}
]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print("Documents added successfully!")

results = collection.query(
    query_texts=["How do I write software?"],
    n_results=3
)

print("\nSearch Results:")
print(results["documents"])

results = collection.query(
    query_texts=["How do I develop software?"],
    n_results=3,
    where={"category": "programming"}
)

print("\nProgramming Results:")

for document in results["documents"][0]:
    print("-", document)
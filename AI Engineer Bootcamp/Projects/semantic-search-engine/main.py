from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("documents.txt", "r", encoding="utf-8") as file:
    documents = file.read().splitlines()

print("Documents Loaded Successfully!")

document_embeddings = model.encode(documents)

print(f"\nNumber of Documents : {len(documents)}")
print(f"Embedding Shape     : {document_embeddings.shape}")

print("=" * 60)
print("Semantic Search Engine")
print("=" * 60)

print(f"\nLoaded {len(documents)} documents successfully!")

print("\nType 'exit' anytime to quit.\n")
while True:
    query = input("\nSearch (or type 'exit'): ")

    if query.lower() == "exit":
        print("\nThank you for using Semantic Search Engine!")
        break

    query_embedding = model.encode(query)

    similarities = cosine_similarity(
        [query_embedding],
        document_embeddings
    )

    top_indices = np.argsort(similarities[0])[::-1][:3]

    print("\nTop Results\n")

    found = False

    for rank, index in enumerate(top_indices, start=1):

        score = similarities[0][index]

        if score < 0.30:
            continue

        found = True

        print(f"{rank}. {documents[index]}")
        print(f"   Similarity: {score:.4f}\n")

    if not found:
        print("No relevant documents found.")
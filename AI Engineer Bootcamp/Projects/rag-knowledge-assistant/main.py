import os

import chromadb
from dotenv import load_dotenv
from google import genai


load_dotenv(".env.local")


def create_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY was not found.")

    return genai.Client(api_key=api_key)


def create_collection():
    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    return client.get_collection(
        name="company_knowledge_v2"
    )


def retrieve_context(collection, question):
    results = collection.query(
        query_texts=[question],
        n_results=2
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    if not documents:
        return [], []

    return documents, distances


def generate_answer(client, question, context):
    context_text = "\n\n".join(context)

    prompt = f"""
You are a company knowledge assistant.

Your task is to answer the user's question using only the
information provided in the context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the context does not contain the answer, clearly say:
   "I don't have enough information in the provided knowledge base."
4. Keep the answer concise and clear.
5. If the context contains multiple relevant pieces of information,
   combine them into one useful answer.

Context:
{context_text}

User Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def main():
    print("=" * 60)
    print("RAG Knowledge Assistant")
    print("=" * 60)

    collection = create_collection()
    gemini_client = create_gemini_client()

    print("\nKnowledge base connected.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        context, distances = retrieve_context(
            collection,
            question
        )

        if not context:
            print("\nNo relevant information found.")
            continue

        print("\nRetrieved Context:")
        print("-" * 60)

        for index, chunk in enumerate(context):
            print(f"\nChunk {index + 1}")
            print(chunk)
            print(f"Distance: {distances[index]:.4f}")

        answer = generate_answer(
            gemini_client,
            question,
            context
        )

        print("\nAnswer:")
        print("-" * 60)
        print(answer)


if __name__ == "__main__":
    main()
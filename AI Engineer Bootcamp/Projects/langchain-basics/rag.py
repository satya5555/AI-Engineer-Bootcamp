import os

import chromadb
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "company_knowledge"


# --------------------------------------------------
# Load documents
# --------------------------------------------------

def load_documents():

    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        content = file.read()

    documents = [
        chunk.strip()
        for chunk in content.split("\n\n")
        if chunk.strip()
    ]

    return documents


# --------------------------------------------------
# Create / Load Vector Store
# --------------------------------------------------

def create_vector_store():

    documents = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Add documents only if collection is empty
    if collection.count() == 0:

        collection.add(
            documents=documents,
            ids=[
                f"doc_{i}"
                for i in range(len(documents))
            ]
        )

        print(f"Added {len(documents)} documents to ChromaDB.")

    else:

        print(
            f"Loaded existing collection with "
            f"{collection.count()} documents."
        )

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    return vector_store


# --------------------------------------------------
# Retrieve documents with similarity scores
# --------------------------------------------------

def retrieve_with_scores(vector_store, question):

    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    return results


# --------------------------------------------------
# Create RAG Chain
# --------------------------------------------------

def create_rag_chain(retriever):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a company knowledge assistant.

Answer the user's question using only the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not available in the context,
  say exactly:

"I don't have enough information in the provided knowledge base."

- Keep the answer concise and clear.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    parser = StrOutputParser()

    rag_chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | parser
    )

    return rag_chain


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("LangChain RAG Knowledge Assistant")
    print("=" * 60)

    # Create/load vector database
    vector_store = create_vector_store()

    # Create retriever
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    # Create RAG chain
    rag_chain = create_rag_chain(retriever)

    print("\nKnowledge base ready.")
    print("Type 'exit' to quit.")

    while True:

        question = input("\nQuestion: ").strip()

        # Check exit BEFORE doing retrieval
        if question.lower() == "exit":

            print("\nGoodbye!")
            break

        if not question:

            print("Please enter a question.")
            continue

        # --------------------------------------------------
        # Retrieve documents with scores
        # --------------------------------------------------

        results = retrieve_with_scores(
            vector_store,
            question
        )

        print("\nRetrieved Documents with Scores:")
        print("-" * 60)

        for index, (document, score) in enumerate(
            results,
            start=1
        ):

            print(f"\nSource {index}")
            print(f"Distance Score: {score:.4f}")
            print(document.page_content)

        # --------------------------------------------------
        # Generate answer using RAG
        # --------------------------------------------------

        answer = rag_chain.invoke(question)

        print("\nAnswer:")
        print("-" * 60)
        print(answer)

        # --------------------------------------------------
        # Display sources
        # --------------------------------------------------

        print("\n📚 Sources:")
        print("-" * 60)

        for index, (document, score) in enumerate(
            results,
            start=1
        ):

            source_text = document.page_content

            # First line as source title
            source_title = source_text.split("\n")[0]

            print(
                f"{index}. {source_title} "
                f"(distance: {score:.4f})"
            )
RELEVANCE_THRESHOLD = 0.8
def retrieve_relevant_documents(vector_store, question):

    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    relevant_documents = []

    for document, score in results:

        if score <= RELEVANCE_THRESHOLD:
            relevant_documents.append(document)

    return relevant_documents

# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    main()
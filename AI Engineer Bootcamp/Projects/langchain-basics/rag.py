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


def load_documents():
    with open("knowledge_base.txt", "r", encoding="utf-8") as file:
        content = file.read()

    return [
        chunk.strip()
        for chunk in content.split("\n\n")
        if chunk.strip()
    ]


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

    if collection.count() == 0:

        collection.add(
            documents=documents,
            ids=[
                f"doc_{i}"
                for i in range(len(documents))
            ]
        )

    return Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )


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
  say: "I don't have enough information in the provided knowledge base."
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


def main():

    print("=" * 60)
    print("LangChain RAG Knowledge Assistant")
    print("=" * 60)

    vector_store = create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )

    rag_chain = create_rag_chain(
        retriever
    )

    print("\nKnowledge base ready.")
    print("Type 'exit' to quit.")

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        answer = rag_chain.invoke(question)

        print("\nAnswer:")
        print("-" * 60)
        print(answer)


if __name__ == "__main__":
    main()
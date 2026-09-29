import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()


class VectorStore:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv(
                "GEMINI_EMBEDDING_MODEL",
                "models/gemini-embedding-001"
            ),
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        self.store = Chroma(
            collection_name="hybrid_search",
            embedding_function=self.embeddings,
            persist_directory="./chroma_db"
        )

    def add_documents(self, documents):
        self.store.add_documents(documents)

    def get_store(self):
        return self.store
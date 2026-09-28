from pathlib import Path

from app.loader import PDFLoader
from app.splitter import TextSplitter
from app.vectorstore import VectorStore


pdf_path = Path(__file__).parent / "documents" / "sample.pdf"


loader = PDFLoader()
documents = loader.load(str(pdf_path))

print(f"Pages loaded: {len(documents)}")


splitter = TextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split(documents)

print(f"Chunks created: {len(chunks)}")


vector_store = VectorStore()

vector_store.add_documents(chunks)

print("Documents added to ChromaDB.")
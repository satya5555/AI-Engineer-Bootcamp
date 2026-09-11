from app.loader import PDFLoader
from app.chat import PDFChat


pdf_loader = PDFLoader()
chat = PDFChat()

documents = pdf_loader.load(
    "documents/sample.pdf"
)

print(f"Loaded {len(documents)} pages.")

question = input("\nAsk a question about the PDF: ")

answer = chat.answer(
    question,
    documents
)

print("\nAnswer:")
print(answer)
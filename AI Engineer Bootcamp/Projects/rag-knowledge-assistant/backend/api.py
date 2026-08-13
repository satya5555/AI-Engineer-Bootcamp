from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import RAGPipeline


app = FastAPI(
    title="AI Knowledge Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag = RAGPipeline()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Assistant API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag.ask(request.question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "distances": result["distances"]
    }
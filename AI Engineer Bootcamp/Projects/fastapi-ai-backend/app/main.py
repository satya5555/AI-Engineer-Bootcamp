from fastapi import FastAPI, HTTPException

from app.models.chat import ChatRequest, ChatResponse
from app.services import ollama_service


app = FastAPI(
    title="AI Backend",
    description="A local AI backend powered by FastAPI and Ollama",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the AI Backend",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = ollama_service.generate_response(request.prompt)

        return ChatResponse(
            prompt=request.prompt,
            response=answer
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Local AI model is unavailable"
        ) from exc
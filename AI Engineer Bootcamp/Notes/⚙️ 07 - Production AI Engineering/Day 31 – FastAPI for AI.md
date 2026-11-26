**Topic:** FastAPI for AI  
**Hands-on Project:** AI Backend  
**Technology:** Python, FastAPI, Uvicorn, Pydantic, Ollama, Qwen 2.5 3B, Pytest

---

## 1. What is an API?

API stands for Application Programming Interface.

An API allows two software applications to communicate with each other through a defined set of rules.

For example, consider an AI chatbot:

1. A user enters a prompt in the frontend.
    
2. The frontend sends the prompt to the backend through an API.
    
3. The backend processes the request.
    
4. The backend communicates with an LLM.
    
5. The LLM generates a response.
    
6. The backend returns the response to the frontend.
    

### Why do we need APIs in AI applications?

- Connect frontend applications with AI models.
    
- Expose LLM functionality to other applications.
    
- Handle user requests and responses.
    
- Validate incoming data.
    
- Manage authentication and authorization.
    
- Integrate databases, tools and external services.
    

## 2. Understanding REST APIs

REST stands for Representational State Transfer.

REST is an architectural style used to build web services that communicate using HTTP.

### Important HTTP methods

|Method|Purpose|Example|
|---|---|---|
|GET|Retrieve data|Get chat history|
|POST|Create or process data|Send a prompt|
|PUT|Replace an existing resource|Replace user settings|
|PATCH|Partially update data|Update username|
|DELETE|Delete a resource|Delete a conversation|

### HTTP status codes

|Code|Meaning|Example|
|---|---|---|
|200|OK|Successful request|
|201|Created|Resource created|
|204|No Content|Successful deletion|
|400|Bad Request|Invalid request|
|401|Unauthorized|Authentication required|
|403|Forbidden|Insufficient permissions|
|404|Not Found|Endpoint unavailable|
|422|Unprocessable Entity|Request validation failed|
|500|Internal Server Error|Unexpected backend error|
|503|Service Unavailable|AI service unavailable|

## 3. What is FastAPI?

FastAPI is a modern Python web framework used to build APIs.

It is particularly useful for AI applications because it provides:

- Automatic request validation.
    
- Automatic API documentation.
    
- Asynchronous programming support.
    
- High performance.
    
- Python type hints.
    
- Easy integration with machine learning and LLM libraries.
    

### Why FastAPI instead of Flask?

|Feature|FastAPI|Flask|
|---|---|---|
|Request validation|Built-in through Pydantic|Usually requires extensions|
|API documentation|Automatic|Additional configuration|
|Async support|Built-in|More limited|
|Type hints|Strong integration|Optional|
|Performance|High|Depends on deployment and configuration|

FastAPI is a convenient choice for building modern AI backends.

## 4. Understanding Uvicorn and ASGI

FastAPI is an application framework. It needs an ASGI server to receive and process HTTP requests.

### What is ASGI?

ASGI stands for Asynchronous Server Gateway Interface.

It defines how asynchronous Python web applications communicate with web servers.

### What is Uvicorn?

Uvicorn is an ASGI server commonly used to run FastAPI applications.

Our command:

```
uvicorn app.main:app --reload
```

Explanation:

- `uvicorn`: Starts the ASGI server.
    
- `app.main`: Refers to the main.py module inside the app package.
    
- `app`: Refers to the FastAPI application object.
    
- `--reload`: Automatically restarts the server when code changes.
    

**Important:** `--reload` is primarily useful during development, not production deployment.

## 5. Understanding FastAPI Application Structure

Our project follows a modular architecture.

```
fastapi-ai-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py
│   │
│   └── services/
│       ├── __init__.py
│       └── ollama_service.py
│
├── tests/
│   └── test_main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Responsibilities

**main.py**

- Creates the FastAPI application.
    
- Defines API endpoints.
    
- Handles incoming requests.
    
- Returns responses.
    

**models/chat.py**

- Defines request and response schemas.
    
- Validates incoming data.
    
- Maintains a consistent response structure.
    

**services/ollama_service.py**

- Communicates with the local Ollama model.
    
- Sends prompts to the LLM.
    
- Extracts the generated response.
    

**tests/**

- Contains automated tests for the API.
    

### Why separate these responsibilities?

This approach is called separation of concerns.

Instead of placing all application logic inside one file, we divide the application into independent modules.

Benefits:

- Easier maintenance.
    
- Better readability.
    
- Easier debugging.
    
- Reusable components.
    
- Easier unit testing.
    

## 6. FastAPI Application and Routes

A route defines how the application responds to a particular URL and HTTP method.

Example:

```
from fastapi import FastAPI

app = FastAPI(
    title="AI Backend",
    description="A local AI backend",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the AI Backend"
    }
```

### Important concepts

**FastAPI()**

Creates the application instance.

**@app.get("/")**

Registers a GET endpoint.

**@app.post("/chat")**

Registers a POST endpoint.

**return**

FastAPI automatically converts Python dictionaries and supported response objects into JSON responses.

## 7. Pydantic and Data Validation

Pydantic is a Python library used for data validation and serialization.

FastAPI uses Pydantic models to validate request bodies and define response schemas.

Our request model:

```
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(
        min_length=1,
        max_length=4000
    )
```

Our response model:

```
class ChatResponse(BaseModel):
    prompt: str
    response: str
```

### What happens when a request arrives?

Suppose the client sends:

```
{
    "prompt": "Explain RAG"
}
```

FastAPI:

1. Receives the JSON request.
    
2. Validates it against ChatRequest.
    
3. Converts the data into a Python model object.
    
4. Passes the validated object to the endpoint.
    
5. Uses ChatResponse to structure the output.
    

### What if invalid data is submitted?

For example:

```
{
    "prompt": ""
}
```

The minimum-length validation fails and FastAPI returns HTTP 422.

This avoids manually checking every field inside the endpoint.

## 8. Integrating Ollama with FastAPI

Ollama allows us to run supported language models locally.

In our project, we use:

**Model:** Qwen 2.5 3B

The Python integration:

```
import ollama

MODEL = "qwen2.5:3b"


def generate_response(prompt: str) -> str:

    result = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.3
        }
    )

    return result["message"]["content"].strip()
```

### Understanding the parameters

**model**

Specifies the LLM to use.

**messages**

Contains the conversation messages.

**role**

Identifies the speaker, such as system, user or assistant.

**content**

Contains the actual message.

**temperature**

Controls randomness in generation. Lower values generally produce more predictable outputs.

### Why use a service layer?

We keep the LLM communication in a separate function.

This allows us to:

- Replace the model later.
    
- Change providers without rewriting API routes.
    
- Test the API independently.
    
- Reuse the AI service in other endpoints.
    

## 9. Building the AI Chat Endpoint

Our endpoint:

```
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        answer = ollama_service.generate_response(
            request.prompt
        )

        return ChatResponse(
            prompt=request.prompt,
            response=answer
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Local AI model is unavailable"
        ) from exc
```

### Complete request lifecycle

```
Frontend
   |
   v
POST /chat
   |
   v
FastAPI receives JSON
   |
   v
Pydantic validates input
   |
   v
Chat endpoint
   |
   v
Ollama service
   |
   v
Qwen 2.5 3B
   |
   v
Generated response
   |
   v
ChatResponse
   |
   v
JSON response to frontend
```

This is the basic architecture of an AI backend.

**Production consideration:** In a production application, use more specific exception handling, structured logging, timeouts and appropriate error reporting rather than catching every exception with one generic handler.

## 10. Swagger UI and OpenAPI

FastAPI automatically generates API documentation.

Our application provides:

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

**ReDoc**

```
http://127.0.0.1:8000/redoc
```

**OpenAPI schema**

```
http://127.0.0.1:8000/openapi.json
```

### Benefits

- Explore available endpoints.
    
- View request and response structures.
    
- Execute API requests directly.
    
- Understand validation requirements.
    
- Share API specifications with frontend developers.
    

## 11. Testing FastAPI Applications

We use Pytest and FastAPI TestClient.

Example:

```
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }
```

### What is TestClient?

TestClient allows us to test FastAPI endpoints without manually starting a server.

### What is mocking?

Mocking replaces a real dependency with a controlled test implementation.

In our project, we mock the Ollama service:

```
def mock_generate(prompt):
    return "Mock AI response"
```

Why?

- Tests don't need an actual LLM call.
    
- Tests execute faster.
    
- Tests don't depend on Ollama availability.
    
- We can control the expected output.
    

### Run tests

```
python -m pytest -v
```

Our Day 31 test cases cover:

- Home endpoint.
    
- Health endpoint.
    
- Chat endpoint.
    
- Empty prompt validation.
    

## 12. Environment and Dependency Management

We use a Python virtual environment to isolate project dependencies.

Create:

```
python -m venv .venv
```

Activate in Windows PowerShell:

```
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```
python -m pip install fastapi "uvicorn[standard]" ollama pytest httpx
```

Save dependencies:

```
pip freeze > requirements.txt
```

Install them later:

```
pip install -r requirements.txt
```

### Why use .gitignore?

We should not commit:

- Virtual environments.
    
- Environment secrets.
    
- Python cache files.
    
- Temporary test files.
    

## 13. Production Considerations

A working local API is not automatically production-ready.

Important areas to consider:

|Area|Purpose|
|---|---|
|Authentication|Verify who can access the API|
|Authorization|Control what users can access|
|Input validation|Prevent malformed requests|
|Rate limiting|Prevent excessive requests|
|Timeouts|Avoid waiting indefinitely for an LLM|
|Logging|Track application activity and errors|
|Monitoring|Observe application health|
|Caching|Avoid unnecessary repeated computation|
|Database|Store users, conversations and metadata|
|Deployment|Run the application reliably|

These topics will be developed further in the upcoming production engineering lessons.

## 14. Important Interview Questions

**1. What is FastAPI?**

FastAPI is a modern Python web framework used to develop APIs with automatic validation, documentation and asynchronous support.

**2. What is Uvicorn?**

Uvicorn is an ASGI server used to run asynchronous Python web applications such as FastAPI.

**3. What is Pydantic?**

Pydantic is a data validation library that uses Python type annotations to validate and serialize data.

**4. What is the difference between GET and POST?**

GET retrieves information, whereas POST sends data to the server for processing or resource creation.

**5. What is ASGI?**

ASGI is an interface specification between asynchronous Python applications and web servers.

**6. What is Swagger UI?**

Swagger UI provides an interactive interface to explore and test API endpoints using the OpenAPI specification.

**7. Why do we use response_model in FastAPI?**

It defines and validates the expected response structure and helps generate accurate API documentation.

**8. Why should we separate routes and services?**

It follows separation of concerns, making applications easier to maintain, test and extend.

**9. What is dependency mocking?**

Mocking replaces an actual dependency with a controlled implementation for testing.

**10. Why is FastAPI useful for AI applications?**

It provides a convenient way to expose LLM inference, RAG pipelines and AI services through REST APIs.

---

## 15. Day 31 Practical Checklist

- Created FastAPI project structure.
    
- Installed dependencies.
    
- Started the application using Uvicorn.
    
- Created GET `/` endpoint.
    
- Created GET `/health` endpoint.
    
- Created Pydantic request and response models.
    
- Integrated Ollama with Qwen 2.5 3B.
    
- Created POST `/chat` endpoint.
    
- Tested API using Swagger UI.
    
- Executed automated tests.
    
- Created README.md.
    
- Committed and pushed project to GitHub.
    

## 16. Day 31 Summary

Today we learned how to build an AI backend using FastAPI.

We connected a locally running LLM to a REST API and exposed its capabilities through a chat endpoint.

**Key takeaway:** FastAPI acts as the communication layer between the frontend and AI services. It receives requests, validates input, invokes the AI model and returns structured responses.

**Next lesson:** Day 32 – Streaming Responses: Streaming Chat.
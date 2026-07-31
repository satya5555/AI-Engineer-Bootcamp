# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 5 – Ollama & Local LLMs

---

# 🎯 Today's Goal

Today's goal was to understand and experiment with **running Large Language Models locally** instead of relying entirely on cloud AI APIs.

We explored Ollama, ran local models, interacted with them through the terminal and HTTP API, and built a small Python-based Local AI Assistant.

---

# 🧠 Concept

Until now, our AI architecture looked like:

```text
Application
     ↓
Internet
     ↓
Cloud AI API
     ↓
Gemini
     ↓
Response
```

Today we explored:

```text
Application
     ↓
localhost
     ↓
Ollama
     ↓
Local LLM
     ↓
Our Computer
     ↓
Response
```

The major difference is that model inference happens locally on our machine.

---

# 🦙 Ollama

Ollama is a tool that makes it easier to download, manage, and run supported language models locally.

It provides:

* Local model execution
* Command-line interaction
* Model management
* Local HTTP APIs
* Support for multiple models
* Streaming generation
* Chat-style APIs

---

# 💻 Hardware Check

Before downloading models, we checked our available hardware.

Our development machine had approximately:

```text
RAM       → 8 GB
GPU       → Intel Iris Xe integrated graphics
C: Free   → ~11 GB
D: Free   → ~57 GB
```

This was important because local LLM performance depends heavily on:

* RAM
* GPU / VRAM
* CPU
* Model size
* Quantization
* Context size
* Number of generated tokens

Because the machine has 8 GB RAM, we focused on lightweight models instead of large 7B+ models.

---

# 📦 Ollama Installation

We verified Ollama using:

```bash
ollama --version
```

Installed version:

```text
0.32.5
```

We checked available models using:

```bash
ollama list
```

An existing local model was already available:

```text
phi:2.7b
```

---

# 🤖 Running Our First Local Model

We started Phi using:

```bash
ollama run phi:2.7b
```

This opened an interactive terminal where prompts could be sent directly to the local model.

Example:

```text
Explain what an API is to a beginner in 3 sentences.
```

No cloud AI API was required.

---

# 🧪 Local Model Testing

We tested different prompt styles:

### Simple Explanation

```text
Explain what an API is to a beginner in 3 sentences.
```

### Coding

```text
Write a Python function that checks whether a number is prime.
Return only the code.
```

### Structured Prompt

```text
You are an AI tutor.

Explain Docker using exactly these sections:

1. Definition
2. Analogy
3. Example
4. Common Mistake
5. Interview Question
```

This allowed us to observe how a smaller local model handles instruction following and structured output.

---

# 🆕 Qwen 3.5

We then experimented with a newer lightweight model:

```text
qwen3.5:2b
```

We selected a smaller model because of our 8 GB RAM constraint.

This demonstrated an important principle:

> Model selection should consider the available hardware and application requirements.

A larger model is not automatically the correct choice.

---

# 💾 Model Storage

Because the C: drive had limited free space, we configured Ollama model storage to use the D: drive.

Example location:

```text
D:\OllamaModels
```

This prevents large model files from unnecessarily consuming the system drive.

---

# 🌐 Ollama Local API

Ollama provides an HTTP API locally.

Default server:

```text
http://localhost:11434
```

We checked installed models through:

```text
GET /api/tags
```

and generated responses through:

```text
POST /api/generate
```

---

# 📡 Testing Ollama with PowerShell

We created a JSON request:

```powershell
$body = @{
    model = "qwen3.5:2b"
    prompt = "Explain what an API is in 3 sentences."
    stream = $false
} | ConvertTo-Json
```

Then sent it to Ollama:

```powershell
$response = Invoke-RestMethod `
    -Uri "http://localhost:11434/api/generate" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

The API successfully returned a response from the local model.

---

# 🔍 Ollama Response

The response contained information such as:

```text
model
response
thinking
done
done_reason
total_duration
eval_count
```

This showed us that an LLM API can return much more than just generated text.

It can also expose useful inference metadata.

---

# 🤔 Reasoning / Thinking

During our Qwen experiment, the model generated a significant amount of reasoning before producing its final answer.

The response contained a separate:

```text
thinking
```

field.

This demonstrated that some models may perform additional reasoning before returning their final response.

---

# ⚡ Local AI Performance

One Qwen request generated more than 2,500 evaluated tokens and took approximately three minutes to complete.

This demonstrated that local AI performance depends on more than just model size.

Important factors include:

```text
Model Size
     +
Hardware
     +
Prompt Complexity
     +
Reasoning
     +
Generated Tokens
     ↓
Inference Time
```

---

# 🆚 Gemini vs Ollama

## Gemini

```text
Application
     ↓
Internet
     ↓
Gemini API
     ↓
Google Infrastructure
     ↓
Gemini Model
```

Advantages:

* Powerful cloud infrastructure
* Larger models
* Fast inference
* Minimal local hardware requirements

Considerations:

* Requires internet
* Requires API credentials
* Usage may have quotas/costs
* Data is sent to an external service

---

## Ollama

```text
Application
     ↓
localhost
     ↓
Ollama
     ↓
Local Model
     ↓
Our Hardware
```

Advantages:

* Local execution
* No cloud AI API key required
* Useful for offline experimentation
* Greater control over local models
* Data can remain on the local machine in this setup

Considerations:

* Requires sufficient hardware
* Models consume disk space
* Local inference can be slower
* Smaller machines may require smaller models

---

# 🐍 Local AI Assistant

We created a new project:

```text
Projects/
└── local-ai-assistant/
    └── assistant.py
```

The goal was to interact with Ollama programmatically using Python.

---

# 🔗 Python → Ollama

We used Python's built-in:

```python
urllib.request
```

instead of installing an additional HTTP library.

Our architecture became:

```text
Python
   ↓
HTTP Request
   ↓
localhost:11434
   ↓
Ollama
   ↓
Qwen
   ↓
Local Inference
   ↓
Python Response
```

---

# 🧩 JSON

We used:

```python
json.dumps()
```

to convert Python dictionaries into JSON before sending them to Ollama.

We used:

```python
json.loads()
```

to convert the API response back into Python data.

---

# 💬 Chat API

We also explored:

```text
POST /api/chat
```

instead of only:

```text
POST /api/generate
```

The chat endpoint accepts conversation messages.

---

# 🎭 Message Roles

Chat applications commonly use roles such as:

```text
system
user
assistant
```

Example:

```text
system
↓
Defines assistant behaviour

user
↓
User's message

assistant
↓
Model's response
```

---

# 🧠 Conversation Memory

LLMs do not automatically remember independent API requests.

Our application can maintain conversation history:

```text
System Message
      ↓
User Message
      ↓
Assistant Response
      ↓
User Message
      ↓
Assistant Response
```

The conversation history can then be sent with the next request.

Therefore:

```text
LLM Memory
≠
Automatic Permanent Memory
```

Instead:

```text
Application stores history
        ↓
History sent with request
        ↓
Model receives context
```

This is a fundamental concept behind AI chat applications.

---

# 📜 System Instructions

We added a system message such as:

```text
You are a helpful local AI assistant.

Give clear and concise answers.

Explain technical concepts in beginner-friendly language.
```

System instructions help define how an AI assistant should behave.

---

# 🌊 Streaming

We also explored streaming.

Without streaming:

```text
Request
   ↓
Wait for entire generation
   ↓
Display response
```

With streaming:

```text
Request
   ↓
Chunk
 ↓
Display
 ↓
Chunk
 ↓
Display
 ↓
...
```

Streaming improves perceived responsiveness because the user can start seeing output before generation completely finishes.

It does not necessarily make model inference itself faster.

---

# ⚠️ Issue Encountered

During the Qwen chat/streaming experiment, the assistant sometimes returned a blank visible response or took significant time.

Earlier inspection showed that the model could generate substantial content in a separate reasoning/thinking field.

This became a useful debugging lesson:

```text
Application shows blank response
          ↓
Don't assume model failed
          ↓
Inspect raw API response
          ↓
Check content / thinking / metadata
          ↓
Identify actual layer causing issue
```

We intentionally stopped further debugging so that this issue would not derail the overall AI Engineer roadmap.

---

# 🛠️ Tools Used

* Ollama
* Phi 2.7B
* Qwen 3.5 2B
* PowerShell
* Python
* VS Code
* Ollama REST API
* JSON
* urllib.request

---

# 📖 New Terms

### Local LLM

A language model running on local hardware instead of remote cloud infrastructure.

### Inference

The process of running a trained model to generate predictions or responses.

### Model Weights

The learned parameters that represent what a neural network has learned.

### localhost

The local computer on which an application is running.

### REST API

An HTTP-based interface through which applications communicate.

### System Prompt

Instructions defining the behaviour or role of an AI model.

### Context

Information supplied to the model for the current generation.

### Conversation History

Previous messages supplied to the model as context.

### Streaming

Returning generated output progressively instead of waiting for the entire response.

### Reasoning / Thinking

Intermediate reasoning generated by some models before or alongside the final answer.

---

# 🌍 Real-World Applications

Local LLMs can be useful for:

* Private AI assistants
* Offline AI applications
* Local coding assistants
* Document analysis
* Enterprise prototypes
* Research experiments
* Edge AI
* Local RAG systems
* AI development without cloud API dependency

---

# 📝 Today's Key Takeaways

* LLMs can run locally as well as in the cloud.
* Ollama simplifies local model management and inference.
* Hardware matters when selecting local models.
* Smaller models are often more practical on limited RAM.
* Ollama exposes local HTTP APIs.
* Python applications can communicate with local LLMs.
* Conversation memory can be implemented by maintaining message history.
* System instructions control assistant behaviour.
* Streaming improves perceived responsiveness.
* Reasoning can significantly increase generation time.
* Local AI provides greater control but shifts computation to our hardware.
* Cloud and local AI architectures each have different advantages.
* Debugging AI applications requires inspecting the model/API response rather than assuming every blank UI response means the model failed.

---

# ❓ Questions I Still Have

* How do quantized models reduce memory requirements?
* How does GPU acceleration affect local inference?
* How do context windows affect RAM usage?
* How can local models access our documents?
* How does RAG work with Ollama?
* When should we choose local models instead of cloud models?
* How can conversation history be managed efficiently for long chats?
* How can reasoning models be configured for faster responses?

These topics can be explored later in the roadmap when they become relevant.

---

# 🏆 What We Built Today

## Local AI Assistant

Completed:

* ✅ Ollama setup
* ✅ Local model execution
* ✅ Phi testing
* ✅ Qwen testing
* ✅ Local model storage configuration
* ✅ Ollama HTTP API
* ✅ PowerShell API testing
* ✅ Python Ollama client
* ✅ Local AI Assistant
* ✅ System instructions
* ✅ Conversation-history implementation
* ✅ Streaming experiment
* ⚠️ Qwen reasoning/blank-response behaviour identified for future investigation

---

# 🚀 Next Step

Day 5 introduced **local AI engineering**.

We now understand both:

```text
Cloud LLMs → Gemini API

and

Local LLMs → Ollama
```

The next session will continue according to the 60-day AI Engineer roadmap with the next planned AI tool/concept rather than continuing to expand or debug today's project unnecessarily.

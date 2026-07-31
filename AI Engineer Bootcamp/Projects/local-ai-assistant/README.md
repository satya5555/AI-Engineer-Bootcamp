# Local AI Assistant

A simple local AI assistant built with Python, Ollama, and a locally running language model as part of the 60-Day AI Engineer Bootcamp.

## Features

- Runs AI locally using Ollama
- Python client for the Ollama REST API
- Local LLM interaction
- System instructions
- Conversation history
- Chat API experimentation
- Streaming experimentation
- No cloud AI API key required

## Models Tested

- Phi 2.7B
- Qwen 3.5 2B

## Architecture

```text
Python Application
        ↓
Ollama REST API
        ↓
Local LLM
        ↓
Local Inference
        ↓
AI Response
```

## Run

Make sure Ollama is running and the required model is installed.

```bash
ollama list
```

Then run:

```bash
python assistant.py
```

Type:

```text
exit
```

to close the assistant.

## Learning Goals

This project explores:

- Local LLMs
- AI inference
- Ollama
- REST APIs
- JSON
- System prompts
- Conversation history
- Streaming
- Local vs cloud AI architecture

## Known Issue

During testing with Qwen 3.5 2B on limited local hardware, some chat/streaming requests produced slow or blank visible responses while the model performed extended reasoning.

This is retained as a learning/debugging point for future exploration.

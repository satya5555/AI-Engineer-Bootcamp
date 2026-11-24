import ollama


response = ollama.chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "user",
            "content": "Explain multi-agent AI systems in five points."
        }
    ]
)

print(response["message"]["content"])
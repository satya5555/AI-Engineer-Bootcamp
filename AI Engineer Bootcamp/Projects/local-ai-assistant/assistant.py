import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5:2b"


def ask_ollama(messages):
    data = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "think": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    full_response = ""

    with urllib.request.urlopen(request) as response:
        for line in response:
            if not line:
                continue

            chunk = json.loads(line.decode("utf-8"))

            content = chunk.get("message", {}).get("content", "")

            if content:
                print(content, end="", flush=True)
                full_response += content

    return full_response

print("=" * 50)
print("Local AI Assistant")
print(f"Model: {MODEL}")
print("Type 'exit' to quit")
print("=" * 50)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful local AI assistant. "
            "Give clear and concise answers. "
            "Explain technical concepts in beginner-friendly language."
        )
    }
]
while True:
    prompt = input("\nYou: ")

    if prompt.lower() == "exit":
        print("\nGoodbye!")
        break

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        print("\nAI: ", end="", flush=True)

        answer = ask_ollama(messages)

        print()

        messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as error:
        print(f"\nError: {error}")
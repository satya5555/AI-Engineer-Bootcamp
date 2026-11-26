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
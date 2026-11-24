import ollama


MODEL = "qwen2.5:3b"


def generate_response(system_prompt, user_prompt):
    """Generate a response using the local Ollama model."""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        options={
            "temperature": 0.3
        }
    )

    return response.message.content.strip()
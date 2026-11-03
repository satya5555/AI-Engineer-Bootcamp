from app.agents import llm

response = llm.call(
    messages=[
        {
            "role": "user",
            "content": "Explain AI agents in two sentences."
        }
    ]
)

print(response)
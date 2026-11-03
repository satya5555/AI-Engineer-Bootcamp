from app.agents import researcher

result = researcher.kickoff(
    "Research the applications of RAG in enterprise AI. "
    "Find five useful findings with source URLs."
)

print("\nRESEARCH OUTPUT")
print("=" * 60)
print(result)
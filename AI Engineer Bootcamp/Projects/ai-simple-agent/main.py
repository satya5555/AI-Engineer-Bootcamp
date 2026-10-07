from app.agent import SimpleAgent


agent = SimpleAgent()

question = input("Ask the agent: ")

result = agent.run(question)

print("\nAGENT DECISION")
print("=" * 80)
print(result)
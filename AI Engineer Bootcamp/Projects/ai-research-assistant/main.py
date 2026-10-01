from app.search import WebSearch
from app.researcher import Researcher
from app.synthesizer import Synthesizer
from app.evaluator import ResearchEvaluator


# Initialize components
search = WebSearch()
researcher = Researcher(search)
synthesizer = Synthesizer()
evaluator = ResearchEvaluator()


# Get research question
question = input("Enter a research question: ")


# Collect evidence
evidence = researcher.research(question)


print("\nRESEARCH EVIDENCE")
print("=" * 80)

for index, item in enumerate(evidence, start=1):
    print(f"\n[{index}] {item['title']}")
    print(f"URL: {item['url']}")
    print(f"Evidence: {item['snippet']}")


# Generate research answer
answer = synthesizer.synthesize(
    question,
    evidence
)


# Evaluate research answer
evaluation = evaluator.evaluate(
    answer,
    evidence
)


print("\nRESEARCH ANSWER")
print("=" * 80)
print(answer)


print("\nEVALUATION")
print("=" * 80)
print(f"Evidence Count:  {evaluation['evidence_count']}")
print(f"Sources Used:    {evaluation['sources_used']}")
print(f"Source Coverage: {evaluation['source_coverage']:.2f}")
print(f"Status:          {evaluation['status']}")
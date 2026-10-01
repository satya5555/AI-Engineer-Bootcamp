class ResearchEvaluator:
    def evaluate(self, answer, evidence):
        if isinstance(answer, list):
            answer_text = " ".join(
                str(item) for item in answer
            )
        else:
            answer_text = str(answer)

        answer_text = answer_text.lower()

        if not evidence:
            return {
                "evidence_count": 0,
                "sources_used": 0,
                "source_coverage": 0.0,
                "status": "NO_EVIDENCE"
            }

        sources_used = []

        for index in range(1, len(evidence) + 1):
            source_tag = f"[source {index}]"

            if source_tag in answer_text:
                sources_used.append(index)

        source_coverage = len(sources_used) / len(evidence)

        if len(sources_used) == 0:
            status = "NO_SOURCE_REFERENCES"
        else:
            status = "EVALUATED"

        return {
            "evidence_count": len(evidence),
            "sources_used": len(sources_used),
            "source_coverage": source_coverage,
            "status": status
        }
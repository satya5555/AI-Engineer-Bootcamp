
def researcher(topic, data):
    """Find information relevant to the research topic."""

    results = []

    for item in data:
        if any(word.lower() in item.lower() for word in topic.split()):
            results.append(item)

    return {
        "agent": "Researcher",
        "topic": topic,
        "findings": results
    }


def analyst(research):
    """Analyze the research findings."""

    findings = research["findings"]

    return {
        "agent": "Analyst",
        "total_findings": len(findings),
        "insights": [
            f"Finding {i + 1}: {item}"
            for i, item in enumerate(findings)
        ]
    }


def writer(analysis, feedback=None):
    """Generate or revise a research report."""

    report = "RESEARCH REPORT\n"
    report += "===============\n\n"
    report += f"Total findings: {analysis['total_findings']}\n\n"

    for insight in analysis["insights"]:
        report += f"- {insight}\n"

    if feedback:
        report += "\nREVISION NOTES\n"
        report += "==============\n"
        report += f"Reviewer feedback: {feedback}\n"
        report += "All available findings have been included.\n"

    return {
        "agent": "Writer",
        "report": report
    }


def reviewer(report):
    """Check the report for basic quality requirements."""

    content = report["report"]
    finding_count = content.count("- Finding")

    issues = []

    if len(content.strip()) < 50:
        issues.append("Report is too short.")

    if finding_count < 3:
        issues.append("Report needs at least 3 findings.")

    if "RESEARCH REPORT" not in content:
        issues.append("Report title is missing.")

    approved = len(issues) == 0

    return {
        "agent": "Reviewer",
        "approved": approved,
        "feedback": (
            "Report meets the quality requirements."
            if approved
            else " ".join(issues)
        )
    }

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class Synthesizer:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )

    def synthesize(self, question, evidence):
        if not evidence:
            return "I could not find enough information to answer the question."

        context = ""

        for index, item in enumerate(evidence, start=1):
            context += (
                f"\nSource {index}\n"
                f"Title: {item['title']}\n"
                f"URL: {item['url']}\n"
                f"Evidence: {item['snippet']}\n"
            )

        prompt = f"""
You are an AI research assistant.

Research question:
{question}

Evidence collected from web search:
{context}

Produce a concise research report using ONLY the evidence provided.

Use this structure:

## Summary
Give a short answer to the research question.

## Key Findings
List the most important findings from the evidence.

## Evidence
Explain the important supporting evidence and associate it with
[Source 1], [Source 2], etc.

## Limitations
Mention any important limitations, gaps, conflicting information,
or lack of sufficient evidence.

## Sources
List the sources that were actually used.

Rules:
- Use only the provided evidence.
- Do not invent facts.
- Do not use your own outside knowledge.
- If evidence is insufficient, clearly say so.
- Keep the report concise.
- Use [Source N] references where appropriate.
"""

        response = self.llm.invoke(prompt)

        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):
                    text = item.get("text")

                    if text:
                        parts.append(text)

            return "\n".join(parts)

        return str(content)
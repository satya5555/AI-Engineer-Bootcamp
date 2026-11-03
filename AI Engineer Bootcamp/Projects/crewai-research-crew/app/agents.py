import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

from crewai import Agent
from app.tools import web_search_tool


researcher = Agent(
    role="Senior AI Researcher",

    goal=(
        "Research the given topic and collect "
        "accurate, relevant and useful information."
    ),

    backstory=(
        "You are an experienced AI researcher "
        "specializing in artificial intelligence, "
        "machine learning and emerging technologies. "
        "You are skilled at finding reliable information "
        "and extracting important facts."
    ),

    llm=llm,

    tools=[web_search_tool],

    verbose=True,

    allow_delegation=False
)

analyst = Agent(
    role="Senior Research Analyst",

    goal=(
        "Analyze the research findings, identify important "
        "patterns, compare information and extract meaningful insights."
    ),

    backstory=(
        "You are an experienced research analyst specializing "
        "in artificial intelligence and technology. You are skilled "
        "at interpreting research evidence, identifying trends, "
        "evaluating benefits and challenges, and producing "
        "well-supported conclusions."
    ),

    llm=llm,

    verbose=True,

    allow_delegation=False
)

writer = Agent(
    role="Professional Research Report Writer",

    goal=(
        "Convert research findings and analytical insights "
        "into a clear, structured and professional research report."
    ),

    backstory=(
        "You are an experienced technical writer specializing "
        "in AI and technology research. You excel at presenting "
        "complex information in a simple, organized and readable "
        "format. You ensure that conclusions are supported by "
        "the provided research and analysis."
    ),

    llm=llm,

    verbose=True,

    allow_delegation=False
)
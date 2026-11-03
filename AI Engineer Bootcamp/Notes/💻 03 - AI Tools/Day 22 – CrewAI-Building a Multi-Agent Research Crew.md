## 1. Objective

Understand multi-agent systems and learn how to coordinate multiple specialized AI agents using CrewAI.

Build an AI Research Crew where three agents collaborate to research a topic, analyze the findings, and generate a structured research report.

### What we built

**AI Research Crew**

- Researcher Agent – Collects information from the web.
    
- Analyst Agent – Analyzes research findings and extracts insights.
    
- Writer Agent – Generates a structured research report.
    

**Technology Stack**

- Python
    
- CrewAI
    
- Gemini API
    
- DDGS (DuckDuckGo Search)
    
- Streamlit
    
- python-dotenv
    

---

## 2. What is CrewAI?

CrewAI is a framework for building and orchestrating multi-agent AI applications.

It allows multiple specialized agents to collaborate on a common objective.

Each agent can have:

- A specific role
    
- A defined goal
    
- A backstory
    
- Tools to perform operations
    
- Tasks assigned to it
    

### Why do we need CrewAI?

A single agent can perform multiple operations, but complex workflows can benefit from dividing responsibilities among specialized agents.

For example, a research application can use:

- One agent for information gathering.
    
- Another agent for analyzing information.
    
- Another agent for preparing the final report.
    

This separation makes the workflow easier to organize and extend.

---

## 3. Important CrewAI Concepts

|Concept|Description|
|---|---|
|Agent|An individual AI worker with a specialized responsibility|
|Task|A specific assignment given to an agent|
|Crew|A team of agents working towards a common objective|
|Process|Defines how tasks are executed|
|Tool|An external capability that an agent can use|
|Context|Passes the output of previous tasks to another task|
|LLM|The language model used by agents for reasoning and generation|

### Agent

An Agent represents an AI worker.

Important properties:

- `role`: Defines the agent's identity.
    
- `goal`: Defines what the agent should achieve.
    
- `backstory`: Provides expertise and behavioral context.
    
- `llm`: Specifies the language model.
    
- `tools`: Provides external capabilities.
    
- `verbose`: Displays execution information.
    
- `allow_delegation`: Controls whether the agent can delegate work.
    

### Task

A Task defines the work an agent must perform.

Important properties:

- `description`: Instructions for the task.
    
- `expected_output`: Expected result.
    
- `agent`: Agent responsible for execution.
    
- `context`: Previous task outputs used as context.
    

### Crew

A Crew combines agents and tasks into one coordinated workflow.

### Process

CrewAI supports different execution processes, including:

- Sequential: Executes tasks in a defined order.
    
- Hierarchical: Uses a manager agent to coordinate task execution.
    

---

## 4. Project – AI Research Crew

### Project Objective

Build a multi-agent research application that accepts a research topic and generates a structured report using web evidence.

Example input:

"Applications of Retrieval Augmented Generation in Enterprise AI"

Expected output:

1. Executive Summary
    
2. Introduction
    
3. Major Applications
    
4. Benefits
    
5. Challenges
    
6. Emerging Trends
    
7. Conclusion
    
8. References
    

### Project Structure

```
crewai-research-crew/
│
├── app/
│   ├── __init__.py
│   ├── agents.py
│   ├── tasks.py
│   ├── tools.py
│   └── crew.py
│
├── main.py
├── ui.py
├── requirements.txt
├── .gitignore
└── .env
```

---

## 5. Environment Setup

### Create Virtual Environment

```
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### Dependencies

```
crewai
python-dotenv
streamlit
ddgs
google-genai
```

Install dependencies:

```
pip install -r requirements.txt
```

### Environment Variables

Create `.env`:

```
GEMINI_API_KEY=your_gemini_api_key
```

The API key should never be committed to GitHub.

---

## 6. Configure Gemini LLM

CrewAI uses an LLM to power agent reasoning and response generation.

We configured Gemini using CrewAI's `LLM` class.

```
import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)
```

### Understanding the configuration

- `load_dotenv()` loads environment variables.
    
- `LLM()` initializes the language model.
    
- `model` selects the Gemini model.
    
- `api_key` authenticates the API request.
    
- `temperature` controls response variability.
    

We tested the LLM connection before creating the agents.

---

## 7. Custom Tool – Web Search

Agents can use tools to interact with external systems.

For this project, we created a custom web search tool using DDGS.

### Why do we need a search tool?

The Researcher needs access to external information instead of relying only on its existing model knowledge.

### Implementation

File: `app/tools.py`

The implementation uses:

- `BaseTool` from CrewAI.
    
- `BaseModel` and `Field` from Pydantic.
    
- `DDGS` for web searching.
    

The custom tool contains:

1. `WebSearchInput` – Defines the search query.
    
2. `WebSearchTool` – Implements the search functionality.
    
3. `_run()` – Executes the search and collects titles, URLs and content snippets.
    
4. `web_search_tool` – Instance assigned to the Researcher Agent.
    

The tool returns up to five search results.

### Important learning

A custom tool gives an AI agent the ability to perform an operation outside the language model itself.

---

## 8. Creating Specialized Agents

### 8.1 Researcher Agent

**Role:** Senior AI Researcher

**Goal:** Research the given topic and collect accurate, relevant information.

**Responsibilities:**

- Search the web.
    
- Collect relevant information.
    
- Identify important facts.
    
- Gather source titles and URLs.
    
- Prepare research findings.
    

The Researcher has access to the custom Web Search Tool.

### 8.2 Analyst Agent

**Role:** Senior Research Analyst

**Goal:** Analyze research findings and extract meaningful insights.

**Responsibilities:**

- Identify major application areas.
    
- Evaluate benefits and challenges.
    
- Identify emerging trends.
    
- Compare findings.
    
- Produce evidence-based conclusions.
    

The Analyst receives the Researcher's output through task context.

### 8.3 Writer Agent

**Role:** Professional Research Report Writer

**Goal:** Convert research findings and analytical insights into a structured report.

**Responsibilities:**

- Prepare an executive summary.
    
- Organize research findings.
    
- Present benefits and challenges.
    
- Explain emerging trends.
    
- Write a conclusion.
    
- Preserve relevant source URLs.
    

The Writer receives both research and analysis outputs.

---

## 9. Creating Tasks

We created three tasks in `app/tasks.py`.

### Research Task

Assigned to the Researcher.

It collects relevant information, facts, applications, benefits, challenges and source URLs.

### Analysis Task

Assigned to the Analyst.

It analyzes the Researcher's findings and extracts insights.

Important implementation:

```
context=[research_task]
```

This provides the Researcher's task output as context for the Analyst.

### Writing Task

Assigned to the Writer.

It prepares the final research report using both previous outputs.

Implementation:

```
context=[research_task, analysis_task]
```

This makes both research findings and analytical insights available to the Writer.

### Understanding Task Dependencies

```
Research Task
      |
      v
Analysis Task
      |
      v
Writing Task
```

Task context helps agents use outputs produced earlier in the workflow.

---

## 10. Crew Orchestration

File: `app/crew.py`

We combined all three agents and tasks using the Crew class.

Important implementation:

```
from crewai import Crew, Process

research_crew = Crew(
    agents=[
        researcher,
        analyst,
        writer
    ],

    tasks=[
        research_task,
        analysis_task,
        writing_task
    ],

    process=Process.sequential,

    verbose=True
)
```

### Understanding Process.sequential

A sequential process executes tasks in a defined order.

In our project:

1. Researcher executes the research task.
    
2. Analyst executes the analysis task.
    
3. Writer executes the writing task.
    

The output of earlier tasks is made available to subsequent tasks through the configured context.

---

## 11. Executing the Research Crew

File: `main.py`

We used the `kickoff()` method to start the crew.

```
from app.crew import research_crew

topic = input("Enter your research topic: ")

result = research_crew.kickoff(
    inputs={"topic": topic}
)

print(result)
```

### Understanding kickoff()

`kickoff()` starts the execution of the Crew.

The `inputs` dictionary supplies values for placeholders such as `{topic}` in the task descriptions.

The method returns the final crew output.

---

## 12. Streamlit User Interface

File: `ui.py`

We created a browser-based interface using Streamlit.

Features:

- Research topic input.
    
- Start Research button.
    
- Loading indicator.
    
- Final research report display.
    
- Download research report as a text file.
    

Run the application:

```
python -m streamlit run ui.py
```

Default local URL:

```
http://localhost:8501
```

The Streamlit interface makes the research workflow easier to use without entering queries through the terminal.

---

## 13. Complete Architecture

```
                 USER
                  |
                  v
          Research Topic Input
                  |
                  v
           CREW ORCHESTRATOR
                  |
                  v
           RESEARCHER AGENT
                  |
                  v
            WEB SEARCH TOOL
                  |
                  v
           RESEARCH FINDINGS
                  |
                  v
             ANALYST AGENT
                  |
                  v
          ANALYTICAL INSIGHTS
                  |
                  v
              WRITER AGENT
                  |
                  v
          FINAL RESEARCH REPORT
                  |
                  v
             STREAMLIT UI
```

### Technology Responsibilities

|Component|Responsibility|
|---|---|
|CrewAI|Agent orchestration|
|Gemini|Language understanding and generation|
|DDGS|Web search|
|Custom Tool|Connects search capability to the Researcher|
|Streamlit|User interface|
|Python|Application implementation|

---

## 14. Testing

We tested the workflow using different research topics.

Examples:

1. Applications of RAG in Enterprise AI.
    
2. Impact of Generative AI on Software Development.
    
3. Multi-Agent AI Systems in Healthcare.
    
4. AI Agents in Automated Software Testing.
    

### Expected validation

- Researcher should collect relevant information.
    
- Analyst should identify useful insights.
    
- Writer should generate a structured report.
    
- Report should preserve relevant source URLs.
    

The workflow was successfully executed through the terminal and Streamlit interface.

---

## 15. Important Learnings

1. Understood the concept of multi-agent systems.
    
2. Learned how CrewAI organizes agents and tasks.
    
3. Created specialized agents with separate responsibilities.
    
4. Integrated Gemini as the LLM.
    
5. Built a custom web search tool.
    
6. Learned task context and task dependencies.
    
7. Implemented sequential orchestration.
    
8. Executed the crew using `kickoff()`.
    
9. Built a Streamlit interface for the application.
    

### Limitations and considerations

- Search results depend on the external search provider.
    
- Search snippets are not equivalent to reading and verifying complete source documents.
    
- Agents can produce incorrect or unsupported conclusions.
    
- Source URLs should be independently checked.
    
- Multiple LLM calls can increase latency and API costs.
    
- Sequential execution means later tasks wait for earlier tasks to complete.
    

---

## 16. Day 21 vs Day 22

|Day 21 – Simple Agent|Day 22 – CrewAI|
|---|---|
|One agent|Multiple specialized agents|
|Agent selects tools|Agents collaborate on tasks|
|Simple tool execution|Task orchestration|
|Observation and final response|Sequential multi-agent workflow|
|Single-agent architecture|Multi-agent architecture|

---

## 17. Interview Questions

**Q1. What is CrewAI?**

CrewAI is a framework for building and orchestrating multi-agent AI systems where specialized agents collaborate to complete tasks.

**Q2. What is an Agent in CrewAI?**

An Agent is an AI worker with a defined role, goal, backstory, LLM and optional tools.

**Q3. What is a Task?**

A Task defines the specific assignment an agent must complete and the expected output.

**Q4. What is a Crew?**

A Crew is a group of agents and tasks coordinated to achieve a common objective.

**Q5. What is Process.sequential?**

It is an execution process in which tasks run one after another in a defined order.

**Q6. What is task context?**

Context allows a task to use outputs from previously executed tasks.

**Q7. What is the difference between sequential and hierarchical processes?**

Sequential execution follows a predefined task order. Hierarchical execution uses a manager agent to coordinate task execution.

**Q8. Why use multiple agents instead of one agent?**

Multiple agents allow responsibilities to be separated by specialization, making complex workflows easier to organize and maintain.

**Q9. How does a custom tool work in CrewAI?**

A custom tool exposes an external capability through a defined interface that an agent can invoke.

**Q10. What is kickoff()?**

`kickoff()` starts the execution of a Crew with the supplied inputs.

---

## 18. What Comes Next?

**Day 23 – LangGraph: Building Stateful AI Agents**

Topics:

- What is LangGraph?
    
- Graph-based agent architecture.
    
- Nodes and edges.
    
- State management.
    
- Conditional routing.
    
- Cycles and loops.
    
- Human-in-the-loop workflows.
    
- Building a stateful AI agent.
    

The next step is to understand how LangGraph gives us more explicit control over agent execution and state.

---

## Day 22 Outcome

**Project:** AI Research Crew

**Status:** Completed

**Key Achievement:** Built a working multi-agent research application using CrewAI, Gemini, custom web search and Streamlit.

**Architecture:** Researcher → Analyst → Writer

**Core Learning:** Multiple specialized AI agents can collaborate through task orchestration and shared context to complete a complex workflow.
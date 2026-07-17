# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 2 – Prompt Engineering Fundamentals

---

# 🎯 Today's Goal

By the end of today's session, you should be able to:

- Understand what Prompt Engineering is.
    
- Learn how AI interprets prompts.
    
- Write prompts like an AI Engineer instead of an AI user.
    
- Apply professional prompting techniques.
    
- Create reusable prompts for real-world applications.
    

---

# 🤖 What is Prompt Engineering?

Prompt Engineering is the process of designing clear, structured, and effective instructions that guide an AI model toward producing the desired output.

Think of a prompt as a **job description** for the AI.

The better the instructions, the better the results.

---

# 🏗️ Think Like an AI Engineer

Most beginners ask:

> "Write Java code."

An AI Engineer thinks differently.

Instead of directly asking for code, they define:

```
Problem
      ↓
Required Context
      ↓
Task
      ↓
Constraints
      ↓
Output Format
      ↓
Evaluate
      ↓
Improve
```

Prompt Engineering is an iterative process, not a one-time question.

---

# 🍕 Real-World Analogy

Imagine ordering a pizza.

❌ Bad Prompt

> Give me a pizza.

You may receive anything.

---

✅ Good Prompt

> I want a medium thin-crust vegetarian pizza with extra cheese, mushrooms, olives, and less spicy seasoning. Cut it into 8 slices.

The second request is specific, so the result is closer to what you want.

AI works in exactly the same way.

---

# 🧠 Anatomy of a Great Prompt

Every professional prompt contains five building blocks.

|Component|Purpose|
|---|---|
|**Role**|Who should the AI behave as?|
|**Context**|Background information|
|**Task**|What should the AI do?|
|**Constraints**|Rules and limitations|
|**Output Format**|How should the answer be presented?|

---

# 👤 1. Role

Assigning a role helps the model respond with the right expertise.

Example:

```
You are a Senior Java Backend Engineer.
```

Other examples:

- Product Manager
    
- Data Scientist
    
- Technical Writer
    
- DevOps Engineer
    
- UI/UX Designer
    

---

# 🌍 2. Context

Context tells the AI what it needs to know before solving the problem.

Example:

```
The application is a Tenant Management System
built using Spring Boot and React.
```

More useful context usually leads to more relevant answers.

---

# ✅ 3. Task

Tell the AI exactly what needs to be done.

❌ Weak

```
Explain Git.
```

✅ Better

```
Explain Git to a beginner using simple language,
real-world analogies, ASCII diagrams,
Java developer examples,
and one interview question.
```

---

# 🚧 4. Constraints

Constraints define boundaries.

Examples:

- Maximum 300 words
    
- Use Java only
    
- Avoid third-party libraries
    
- Beginner-friendly explanation
    
- Use bullet points
    

Constraints make responses more consistent.

---

# 📄 5. Output Format

Always specify the format whenever possible.

Examples:

- Markdown
    
- Table
    
- JSON
    
- CSV
    
- Bullet List
    
- Step-by-step Guide
    

Instead of saying:

> Explain REST APIs.

Try:

> Explain REST APIs in a Markdown table with examples.

---

# 🧩 Professional Prompt Formula

A reusable prompt template:

```
Role
+
Context
+
Task
+
Constraints
+
Output Format
```

Example:

```
You are a Senior Backend Engineer.

Context:
We are building a Tenant Management System.

Task:
Design REST APIs for Tenant Registration.

Constraints:
Use Spring Boot REST best practices.

Output:
Markdown table.
```

---

# 🎯 Professional Prompting Techniques

## 1. Zero-shot Prompting

No examples are provided.

Example:

```
Explain REST APIs.
```

---

## 2. One-shot Prompting

Provide one example before asking the model to solve a similar task.

---

## 3. Few-shot Prompting

Provide multiple examples so the AI learns the expected pattern.

Useful for:

- Classification
    
- Data extraction
    
- Formatting
    
- Code generation
    

---

## 4. Role Prompting

Tell the AI who it should become.

Example:

```
You are an AI Instructor.
```

---

## 5. Structured Output Prompting

Specify exactly how the output should look.

Example:

```
Return the answer as JSON.
```

or

```
Generate a Markdown table.
```

---

## 6. Prompt Chaining

Break one large task into smaller tasks.

Example:

```
Research
    ↓
Plan
    ↓
Design
    ↓
Code
    ↓
Review
    ↓
Improve
```

This produces better results than asking everything at once.

---

## 7. Constraint Prompting

Explicitly mention what the AI should or should not do.

Example:

```
Do not use external libraries.

Use only Java 21.

Keep the explanation under 300 words.
```

---

## 8. Delimiter Prompting

Separate instructions from user input.

Example:

```
###
User Input
###
```

or

```
"""
User Content
"""
```

This reduces ambiguity when working with large inputs.

---

## 9. Iterative Prompting

Professional engineers rarely accept the first answer.

Workflow:

```
Write Prompt
      ↓
Generate Response
      ↓
Review
      ↓
Improve Prompt
      ↓
Generate Again
```

Iteration is one of the biggest differences between beginners and experienced AI engineers.

---

# ❌ Common Beginner Mistakes

- Asking vague questions
    
- Providing little or no context
    
- Forgetting to define a role
    
- Ignoring output formatting
    
- Expecting perfect answers on the first attempt
    
- Solving a huge problem with a single prompt
    

---

# 💻 Hands-on Exercise

Rewrite this prompt:

```
Explain Git.
```

Improved version:

```
You are a Senior Software Engineer.

Explain Git to a beginner.

Use simple language,
real-world analogies,
ASCII diagrams,
Java examples,
and end with one interview question.

Return the answer in Markdown.
```

Notice how much more specific and useful the second prompt is.

---

# 📌 Prompt Engineering Principles

✔ Be specific.

✔ Give enough context.

✔ Define a role.

✔ Mention constraints.

✔ Specify the output format.

✔ Break complex tasks into smaller prompts.

✔ Iterate until the response meets your expectations.

---

# 🌍 Real-World Applications

Prompt Engineering is used in:

- AI Coding Assistants
    
- Chatbots
    
- AI Agents
    
- Documentation Generation
    
- Resume Optimization
    
- Research Assistants
    
- Customer Support
    
- Data Analysis
    
- RAG Systems
    
- Multi-Agent Workflows
    

---

# 📝 Today's Key Takeaways

- Prompt Engineering is the skill of designing effective instructions for AI.
    
- Every great prompt contains:
    
    - Role
        
    - Context
        
    - Task
        
    - Constraints
        
    - Output Format
        
- Better prompts produce better results.
    
- Prompt Engineering is an iterative process.
    
- Breaking complex tasks into smaller prompts improves quality.
    

---

# 🚀 Mini Challenge

Improve this prompt:

```
Build a website.
```

Try converting it into a professional AI Engineer prompt by adding:

- Role
    
- Context
    
- Task
    
- Constraints
    
- Output Format
    

---

# ✅ Before We Move On

Today you learned:

- What Prompt Engineering is
    
- How AI interprets prompts
    
- The five building blocks of a professional prompt
    
- Professional prompting techniques
    
- The importance of iteration
    
- How AI Engineers think while writing prompts
    

**Next Session Preview**

We will continue building our first project, **Prompt Playground**, by implementing forms, state management, local storage, and a reusable prompt management interface using Next.js and TypeScript.
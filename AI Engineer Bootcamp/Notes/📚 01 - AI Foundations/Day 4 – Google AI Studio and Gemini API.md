# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 4 – Google AI Studio & Gemini API Integration

---

# 🎯 Today's Goal

Today's focus was hands-on AI integration.

The goal was to move from simply using AI tools to actually **building an application powered by an LLM**.

By the end of the session, we successfully connected our Prompt Playground application to Google's Gemini API.

---

# 🛠️ What We Built

Previously our Prompt Playground worked like this:

```text
Write Prompt
     ↓
React State
     ↓
Save Prompt
     ↓
Local Storage
```

Today we upgraded it into:

```text
Write Prompt
     ↓
Run with Gemini
     ↓
Next.js API Route
     ↓
Gemini API
     ↓
Gemini Model
     ↓
AI Response
     ↓
Display in UI
```

This transformed our normal web application into an **AI-powered application**.

---

# 🤖 Google AI Studio

Google AI Studio is a browser-based environment for experimenting with Google's Gemini models.

It allows developers to:

- Test prompts
    
- Experiment with Gemini models
    
- Adjust model settings
    
- Test structured instructions
    
- Generate API keys
    
- Prototype AI applications
    

We used AI Studio before integrating Gemini into our own application.

---

# 🧪 AI Studio Experiments

We tested several types of prompts.

## Simple Prompt

```text
Explain Docker.
```

---

## Structured Prompt

```text
You are an AI tutor.

Explain Docker.

Return the response using:

1. Simple Definition
2. Real-World Analogy
3. Example
4. Common Mistake
5. Interview Question
```

This demonstrated how structured instructions can produce more predictable output.

---

# 💻 Coding Prompt

We also tested Gemini as a developer assistant.

Example:

```text
You are a senior TypeScript developer.

Create a TypeScript function that accepts
an array of numbers and returns:

- minimum
- maximum
- average

Return only TypeScript code.
```

---

# 🧠 AI User vs AI Engineer

A normal AI user typically works like:

```text
Question
   ↓
AI
   ↓
Answer
```

An AI Engineer thinks about:

```text
Prompt
   ↓
Model
   ↓
Configuration
   ↓
API
   ↓
Application Logic
   ↓
Generated Response
```

The goal is not only to use AI.

The goal is to **build systems using AI models**.

---

# 🔑 Gemini API Key

To allow our application to communicate with Gemini, we created a Gemini API key.

The key was stored inside:

```text
.env.local
```

Example:

```text
GEMINI_API_KEY=********
```

The real API key should never be:

- Hardcoded into source code
    
- Shared publicly
    
- Uploaded to GitHub
    
- Included in screenshots
    
- Sent in frontend requests
    

---

# 🔐 Protecting Secrets

We added:

```text
.env.local
```

to:

```text
.gitignore
```

We verified it using:

```bash
git check-ignore -v .env.local
```

Git confirmed that the file was ignored.

This protects our Gemini API key from accidentally being committed.

---

# 📦 Google Gen AI SDK

We installed Google's JavaScript/TypeScript SDK:

```bash
npm install @google/genai
```

This allows our Next.js backend to communicate with Gemini.

---

# 🏗️ AI Application Architecture

Our application now follows this architecture:

```text
                USER
                  │
                  ↓
          Prompt Playground
                  │
                  ↓
            PromptForm
                  │
                  ↓
            /api/generate
                  │
                  ↓
         Google Gen AI SDK
                  │
                  ↓
             Gemini API
                  │
                  ↓
            Gemini Model
                  │
                  ↓
             AI Response
                  │
                  ↓
             Browser UI
```

---

# 🌐 Next.js API Route

We created:

```text
app/
└── api/
    └── generate/
        └── route.ts
```

This created the endpoint:

```text
POST /api/generate
```

The API route acts as the bridge between our frontend and Gemini.

---

# 🔒 Why Not Call Gemini Directly?

We should NOT do:

```text
Browser
   ↓
Gemini API
```

because the API key could be exposed to users.

Instead:

```text
Browser
   ↓
Our Backend
   ↓
Gemini API
```

The API key remains on the server.

---

# 📡 POST Request

Our frontend sends the user's prompt using:

```text
POST /api/generate
```

Example request data:

```json
{
  "prompt": "Explain artificial intelligence"
}
```

The backend receives the prompt and sends it to Gemini.

---

# 🧪 Testing the API Independently

Before connecting the frontend, we tested our backend directly using PowerShell.

Example:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:3000/api/generate" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"prompt":"Explain artificial intelligence in one sentence"}'
```

Gemini successfully returned an AI-generated response.

---

# 💡 Important Engineering Practice

We tested:

```text
Backend
   ↓
Gemini
```

before testing:

```text
Frontend
   ↓
Backend
   ↓
Gemini
```

Testing individual layers makes debugging easier.

---

# ✨ Run with Gemini

We added a new button:

```text
✨ Run with Gemini
```

When clicked:

```text
Prompt
   ↓
handleGenerate()
   ↓
fetch()
   ↓
POST /api/generate
   ↓
Gemini
   ↓
AI Response
   ↓
setAiResponse()
   ↓
UI Updates
```

---

# ⏳ Loading State

AI requests take time.

We introduced:

```tsx
isGenerating
```

The button changes from:

```text
✨ Run with Gemini
```

to:

```text
Generating...
```

while the model is responding.

This provides better user feedback.

---

# ⚠️ Error Handling

We added error handling for cases such as:

- Empty prompts
    
- API failures
    
- Network problems
    
- Gemini errors
    

Example:

```text
Please enter a prompt first.
```

AI applications must handle failures instead of assuming every model request will succeed.

---

# 🌡️ Temperature

We added a temperature control.

Example:

```text
Temperature: 0.7

Focused ─────────●──── Creative
```

Temperature influences the variability of model responses.

General intuition:

```text
Lower Temperature
       ↓
More focused
More predictable

Higher Temperature
       ↓
More varied
More creative
```

---

# 🧪 Temperature Experiment

We tested the same prompt with different temperatures.

Example:

```text
Write a creative tagline for an AI-powered coding assistant.
```

We compared:

```text
Temperature = 0.1
```

with:

```text
Temperature = 1.0
```

This demonstrated that model configuration can influence output behavior.

---

# 🎯 Choosing Temperature

General intuition:

|Task|Typical Preference|
|---|---|
|Classification|Lower|
|Data Extraction|Lower|
|Technical Answers|Lower / Moderate|
|General Chat|Moderate|
|Brainstorming|Higher|
|Creative Writing|Higher|

These are guidelines rather than strict rules.

---

# 📋 Copy Response

We added a Copy button to Gemini responses.

It uses the browser Clipboard API:

```tsx
navigator.clipboard.writeText(aiResponse)
```

This allows users to quickly reuse generated content.

---

# 🧩 Prompt Playground Architecture

Our application now contains two major systems:

```text
               Prompt Playground
                       │
            ┌──────────┴──────────┐
            ↓                     ↓
      Prompt Management       AI Generation
            │                     │
       React State           API Route
            │                     │
      Local Storage          Gemini API
            │                     │
      Saved Prompts          AI Response
```

---

# 🛠️ Debugging Lesson

Initially:

```text
POST /api/generate
```

returned:

```text
404 Not Found
```

This indicated that Next.js could not locate the API route.

We verified the route structure:

```text
app/api/generate/route.ts
```

After correcting/reloading the route, the API worked successfully.

Important debugging principle:

```text
Error
 ↓
Identify Layer
 ↓
Verify Assumptions
 ↓
Fix
 ↓
Test Again
```

Do not randomly change multiple parts of the application at once.

---

# 🏗️ Production Build

After completing the integration, we ran:

```bash
npm run build
```

The production build succeeded.

Next.js detected:

```text
○ /
ƒ /api/generate
```

Where:

```text
○ = Static page

ƒ = Dynamic server route
```

Our frontend can be statically rendered while the Gemini API endpoint runs dynamically when requested.

---

# ❌ Common Mistakes

### Exposing API Keys

Never put secrets inside frontend code.

❌ Wrong:

```tsx
const apiKey = "AIza...";
```

Use environment variables instead.

---

### Committing `.env.local`

Always verify:

```bash
git check-ignore -v .env.local
```

before pushing sensitive projects.

---

### Calling AI APIs Directly from the Browser

Prefer:

```text
Frontend
   ↓
Backend
   ↓
AI Provider
```

when a secret API key is required.

---

### Ignoring Loading States

AI requests are not instantaneous.

Always provide feedback such as:

```text
Generating...
```

---

### Ignoring API Errors

AI providers can fail because of:

- Rate limits
    
- Invalid keys
    
- Quotas
    
- Network errors
    
- Model availability
    

Production applications must handle these cases.

---

# 🌍 Real-World Applications

The architecture learned today is used in:

- AI Chatbots
    
- AI Writing Assistants
    
- Coding Assistants
    
- Document Summarizers
    
- Resume Analyzers
    
- Research Assistants
    
- AI Search Systems
    
- Customer Support AI
    
- AI Agents
    
- Enterprise AI Applications
    

---

# 📝 Today's Key Takeaways

- Google AI Studio helps prototype Gemini applications.
    
- AI models can be accessed programmatically through APIs.
    
- API keys must remain secret.
    
- `.env.local` stores local environment variables.
    
- `.gitignore` protects secrets from Git.
    
- Next.js API routes can act as a secure backend.
    
- Frontends should not expose secret AI credentials.
    
- AI requests should include loading and error handling.
    
- Temperature influences model output variability.
    
- AI features should be tested independently before full UI integration.
    
- Production builds help catch errors before deployment.
    

---

# 🏆 What We Built Today

## Prompt Playground v2 — Gemini Powered

Completed features:

- ✅ Google AI Studio exploration
    
- ✅ Gemini API key setup
    
- ✅ Secure environment variables
    
- ✅ Google Gen AI SDK
    
- ✅ Next.js AI API route
    
- ✅ Gemini 2.5 Flash integration
    
- ✅ API testing with PowerShell
    
- ✅ Run with Gemini
    
- ✅ AI response display
    
- ✅ Loading state
    
- ✅ Error handling
    
- ✅ Temperature control
    
- ✅ Copy AI response
    
- ✅ Production build verification
    
- ✅ API key security verification
    

---

# 🚀 Next Step

Day 4 successfully transformed Prompt Playground from a normal web application into an **LLM-powered product**.

The next session will continue according to our **60-day AI Engineer roadmap**, exploring the next AI tool/concept and building with it rather than unnecessarily expanding Prompt Playground.
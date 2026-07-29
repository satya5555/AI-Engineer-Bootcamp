# 🚀 AI Engineer Bootcamp

# Sprint 1 – Foundations of AI Engineering

# 📅 Day 3 – Building Prompt Playground

---

# 🎯 Today's Goal

Today's focus was completely hands-on.

The goal was to transform our basic Prompt Playground from a static interface into a functional application where users can:

- Create prompts
    
- Categorize prompts
    
- Display saved prompts
    
- Persist prompts after refreshing
    
- Delete prompts
    
- Organize the application using reusable React components
    

---

# 🛠️ What We Built

We started with:

```text
Prompt Playground 🚀

Prompt Form

Prompt List
```

By the end of the session, we created a functional prompt management application.

Our application now supports:

```text
Create Prompt
      ↓
Store in React State
      ↓
Display Prompt
      ↓
Save to Local Storage
      ↓
Refresh Browser
      ↓
Prompt Still Exists
      ↓
Delete Prompt
```

---

# 🧩 Project Architecture

Our application is divided into reusable components:

```text
prompt-playground/
│
├── app/
│   └── page.tsx
│
├── components/
│   └── prompts/
│       ├── PromptForm.tsx
│       ├── PromptList.tsx
│       └── PromptCard.tsx
│
└── types/
    └── prompt.ts
```

Each component has a specific responsibility.

---

# 📝 PromptForm

`PromptForm` is responsible for collecting user input.

It contains:

- Prompt Title
    
- Category
    
- Prompt Content
    
- Save Prompt button
    

Example:

```text
Title:
Explain Docker

Category:
Learning

Prompt:
Explain Docker to a beginner using a real-world analogy.
```

---

# 🧠 React State – useState

We used React's `useState` hook to remember values.

Example:

```tsx
const [title, setTitle] = useState("");
```

This gives us:

```text
title
  ↓
Current value

setTitle()
  ↓
Function used to update the value
```

When the user types:

```text
Docker
```

the flow becomes:

```text
User types
    ↓
onChange
    ↓
setTitle()
    ↓
React State updates
    ↓
UI updates
```

---

# 🎛️ Controlled Inputs

Our form fields are controlled by React.

Example:

```tsx
<input
  value={title}
  onChange={(e) => setTitle(e.target.value)}
/>
```

React controls both:

```text
Value displayed
      +
Value stored
```

This is known as a **Controlled Component**.

---

# 📦 Creating Prompt Objects

When the form is submitted, we create a Prompt object.

Example structure:

```tsx
{
  id: "...",
  title: "Explain Docker",
  category: "Learning",
  content: "Explain Docker...",
  createdAt: "..."
}
```

Every prompt receives a unique ID using:

```tsx
crypto.randomUUID()
```

The ID allows us to uniquely identify each prompt.

---

# 🧱 TypeScript Interface

We defined the structure of a Prompt using TypeScript.

```tsx
export interface Prompt {
  id: string;
  title: string;
  category: string;
  content: string;
  createdAt: string;
}
```

This ensures every Prompt follows the same structure.

---

# 🔄 Component Communication

Our components communicate through **props**.

Architecture:

```text
              page.tsx
                 │
        ┌────────┴────────┐
        ↓                 ↓
   PromptForm         PromptList
                           │
                           ↓
                      PromptCard
```

`page.tsx` owns the main prompt state.

---

# ⬆️ Sending Data to the Parent

`PromptForm` creates a prompt and sends it to `page.tsx`.

We used:

```tsx
onAddPrompt(newPrompt)
```

The parent then updates the prompt list.

---

# ⬇️ Sending Data to Children

`page.tsx` passes prompts to `PromptList`.

```tsx
<PromptList prompts={prompts} />
```

`PromptList` then sends individual prompts to `PromptCard`.

---

# 🔁 Rendering Multiple Prompts

We used JavaScript's `.map()` function.

```tsx
prompts.map((prompt) => (
  <PromptCard
    key={prompt.id}
    prompt={prompt}
  />
))
```

If there are:

```text
5 prompts
```

React creates:

```text
5 PromptCards
```

automatically.

---

# 💾 Local Storage

Initially, our prompts disappeared whenever the browser refreshed.

React state exists only while the application is running.

We solved this using:

```text
localStorage
```

Application flow:

```text
React State
     ↕
localStorage
```

---

# 📥 Reading from Local Storage

We used:

```tsx
localStorage.getItem("prompts")
```

to retrieve previously saved prompts.

---

# 📤 Saving to Local Storage

We used:

```tsx
localStorage.setItem(
  "prompts",
  JSON.stringify(prompts)
)
```

Local Storage stores strings.

Therefore:

```text
JavaScript Array
      ↓
JSON.stringify()
      ↓
String
      ↓
localStorage
```

---

# 🔄 JSON.parse()

When retrieving the data:

```tsx
JSON.parse(savedPrompts)
```

converts the stored JSON string back into JavaScript data.

```text
localStorage String
        ↓
JSON.parse()
        ↓
JavaScript Array
```

---

# ⚡ useEffect

We used `useEffect` to perform actions when application state changes.

It helped us:

- Load prompts when the application starts
    
- Save prompts whenever the prompt list changes
    

---

# 🗑️ Delete Prompt

We added the ability to delete individual prompts.

Each prompt has a unique:

```text
id
```

When Delete is clicked:

```text
PromptCard
    ↓
onDelete(id)
    ↓
page.tsx
    ↓
setPrompts()
```

---

# 🔍 JavaScript filter()

We used `.filter()` to remove prompts.

Example:

```text
1 → Docker
2 → Git
3 → Kubernetes
```

Delete:

```text
ID = 2
```

Result:

```text
1 → Docker
3 → Kubernetes
```

The original array is not directly modified.

Instead, a new array is created.

---

# 🌐 Next.js Client Components

Next.js App Router uses Server Components by default.

Our interactive components require:

```tsx
"use client";
```

because they use:

- `useState`
    
- `useEffect`
    
- Browser events
    
- `localStorage`
    

---

# 🏗️ Production Build

At the end of development we tested the application using:

```bash
npm run build
```

The build completed successfully:

```text
✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages
✓ Finalizing page optimization
```

This confirmed that:

- TypeScript compilation succeeded
    
- Next.js production compilation succeeded
    
- No blocking build errors were present
    

---

# ❌ Common Mistakes

### Storing everything in one component

Avoid creating a huge `page.tsx`.

Instead:

```text
PromptForm
PromptList
PromptCard
```

separate responsibilities.

---

### Forgetting `"use client"`

Hooks such as:

```tsx
useState()
useEffect()
```

require a Client Component.

---

### Trying to store objects directly in localStorage

Wrong:

```tsx
localStorage.setItem("prompts", prompts)
```

Correct:

```tsx
localStorage.setItem(
  "prompts",
  JSON.stringify(prompts)
)
```

---

### Forgetting unique keys

When rendering lists:

```tsx
key={prompt.id}
```

helps React identify each item correctly.

---

# 🌍 Real-World Applications

The concepts learned today are used in:

- AI chat interfaces
    
- Prompt libraries
    
- AI dashboards
    
- Agent configuration interfaces
    
- AI workflow builders
    
- Chat history systems
    
- User preference management
    
- AI productivity tools
    

---

# 📝 Today's Key Takeaways

- `useState` stores changing UI data.
    
- Controlled inputs connect form fields with React state.
    
- Props allow components to communicate.
    
- `.map()` dynamically renders lists.
    
- `.filter()` helps remove items.
    
- `localStorage` provides browser-side persistence.
    
- `JSON.stringify()` converts objects into strings.
    
- `JSON.parse()` converts stored JSON back into JavaScript objects.
    
- `useEffect` handles side effects such as storage synchronization.
    
- TypeScript interfaces help maintain predictable data structures.
    
- Breaking an application into components improves maintainability.
    

---

# 🏆 What We Built Today

## Prompt Playground v1

Features completed:

- ✅ Create Prompt
    
- ✅ Prompt Categories
    
- ✅ Form Validation
    
- ✅ Dynamic Prompt Cards
    
- ✅ Persistent Local Storage
    
- ✅ Delete Prompt
    
- ✅ Component Architecture
    
- ✅ TypeScript Types
    
- ✅ Successful Production Build
    

---

# 🚀 Next Step

Prompt Playground v1 is now functional.

Our next sessions will continue according to the **60-day AI Engineer roadmap**, focusing primarily on hands-on AI tools and building real products rather than turning the bootcamp into a frontend course.
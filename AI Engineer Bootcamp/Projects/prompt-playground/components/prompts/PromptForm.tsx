"use client";

import { useState } from "react";
import { Prompt } from "@/types/prompt";

interface PromptFormProps {
  onAddPrompt: (prompt: Prompt) => void;
}

export default function PromptForm({ onAddPrompt }: PromptFormProps) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("Coding");
  const [content, setContent] = useState("");

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!title.trim() || !content.trim()) {
      return;
    }

    const newPrompt: Prompt = {
      id: crypto.randomUUID(),
      title: title.trim(),
      category,
      content: content.trim(),
      createdAt: new Date().toISOString(),
    };

    onAddPrompt(newPrompt);

    setTitle("");
    setCategory("Coding");
    setContent("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-2xl rounded-xl bg-white p-6 shadow"
    >
      <h2 className="mb-6 text-2xl font-semibold text-slate-900">
        Create Prompt
      </h2>

      <div className="mb-4">
        <label className="mb-2 block font-medium text-slate-700">
          Prompt Title
        </label>

        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Example: Explain Docker"
          className="w-full rounded-lg border border-slate-300 p-3 text-slate-900"
        />
      </div>

      <div className="mb-4">
        <label className="mb-2 block font-medium text-slate-700">
          Category
        </label>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full rounded-lg border border-slate-300 p-3 text-slate-900"
        >
          <option value="Coding">Coding</option>
          <option value="Writing">Writing</option>
          <option value="Research">Research</option>
          <option value="Learning">Learning</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div className="mb-6">
        <label className="mb-2 block font-medium text-slate-700">Prompt</label>

        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your prompt here..."
          rows={6}
          className="w-full rounded-lg border border-slate-300 p-3 text-slate-900"
        />
      </div>

      <button
        type="submit"
        className="rounded-lg bg-slate-900 px-5 py-3 font-medium text-white hover:bg-slate-700"
      >
        Save Prompt
      </button>
    </form>
  );
}

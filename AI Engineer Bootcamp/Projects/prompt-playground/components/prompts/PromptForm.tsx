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
  const [aiResponse, setAiResponse] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");
  const [temperature, setTemperature] = useState(0.7);

  const handleGenerate = async () => {
    if (!content.trim()) {
      setError("Please enter a prompt first.");
      return;
    }
    try {
      setIsGenerating(true);
      setError("");
      setAiResponse("");

      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: content,
          temperature,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate response");
      }

      setAiResponse(data.result);
    } catch (error) {
      console.error(error);
      setError("Something went wrong while generating the response.");
    } finally {
      setIsGenerating(false);
    }
  };
  const handleCopy = async () => {
    if (!aiResponse) return;

    await navigator.clipboard.writeText(aiResponse);
  };
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
      <div className="mb-6">
        <label className="mb-2 block font-medium text-slate-700">
          Temperature: {temperature}
        </label>

        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={temperature}
          onChange={(e) => setTemperature(Number(e.target.value))}
          className="w-full"
        />

        <div className="mt-1 flex justify-between text-xs text-slate-500">
          <span>Focused</span>
          <span>Creative</span>
        </div>
      </div>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={handleGenerate}
          disabled={isGenerating}
          className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isGenerating ? "Generating..." : "✨ Run with Gemini"}
        </button>

        <button
          type="submit"
          className="rounded-lg bg-slate-900 px-5 py-3 font-medium text-white hover:bg-slate-700"
        >
          Save Prompt
        </button>
        {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
        {aiResponse && (
          <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-semibold text-slate-900">
                ✨ Gemini Response
              </h3>

              <button
                type="button"
                onClick={handleCopy}
                className="rounded-md border border-slate-300 px-3 py-1 text-sm text-slate-700 hover:bg-slate-100"
              >
                Copy
              </button>
            </div>

            <p className="whitespace-pre-wrap text-slate-700">{aiResponse}</p>
          </div>
        )}
      </div>
    </form>
  );
}

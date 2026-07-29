"use client";

import { useEffect, useState } from "react";

import PromptForm from "@/components/prompts/PromptForm";
import PromptList from "@/components/prompts/PromptList";
import { Prompt } from "@/types/prompt";

export default function Home() {
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load saved prompts when the page opens
  useEffect(() => {
    const savedPrompts = localStorage.getItem("prompts");

    if (savedPrompts) {
      setPrompts(JSON.parse(savedPrompts));
    }

    setIsLoaded(true);
  }, []);

  // Save prompts whenever they change
  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem("prompts", JSON.stringify(prompts));
    }
  }, [prompts, isLoaded]);

  const addPrompt = (prompt: Prompt) => {
    setPrompts((currentPrompts) => [prompt, ...currentPrompts]);
  };
  const deletePrompt = (id: string) => {
    setPrompts((currentPrompts) =>
      currentPrompts.filter((prompt) => prompt.id !== id),
    );
  };

  return (
    <main className="min-h-screen bg-slate-100 p-10 text-slate-900">
      <div className="mx-auto max-w-4xl">
        <h1 className="mb-8 text-4xl font-bold">Prompt Playground 🚀</h1>

        <PromptForm onAddPrompt={addPrompt} />

        <div className="mt-10">
          <PromptList prompts={prompts} onDelete={deletePrompt} />
        </div>
      </div>
    </main>
  );
}

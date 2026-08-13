"use client";

import { useState } from "react";

interface Source {
  text: string;
  distance: number;
}

interface ApiResponse {
  answer: string;
  sources: string[];
  distances: number[];
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnswer("");
      setSources([]);

      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      const data: ApiResponse = await response.json();

      if (!response.ok) {
        throw new Error("Failed to get an answer.");
      }

      setAnswer(data.answer);

      const formattedSources = data.sources.map((source, index) => ({
        text: source,
        distance: data.distances[index],
      }));

      setSources(formattedSources);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to the AI Knowledge Assistant. Make sure the FastAPI server is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-white">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="mb-10 text-center">
          <div className="mb-4 text-5xl">🧠</div>

          <h1 className="text-4xl font-bold tracking-tight">
            AI Knowledge Assistant
          </h1>

          <p className="mt-3 text-slate-400">
            Ask questions and get answers from your company knowledge base.
          </p>
        </div>

        {/* Question Card */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
          <label className="mb-3 block text-sm font-medium text-slate-300">
            Ask a question
          </label>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                askQuestion();
              }
            }}
            placeholder="Example: What is the work from home policy?"
            rows={4}
            className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 p-4 text-white outline-none placeholder:text-slate-500 focus:border-blue-500"
          />

          <div className="mt-4 flex items-center justify-between">
            <p className="text-xs text-slate-500">
              Press Enter to ask • Shift + Enter for a new line
            </p>

            <button
              onClick={askQuestion}
              disabled={loading}
              className="rounded-xl bg-blue-600 px-6 py-3 font-medium transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask AI"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
              {error}
            </div>
          )}
        </section>

        {/* Answer */}
        {answer && (
          <section className="mt-8">
            <h2 className="mb-3 text-xl font-semibold">🤖 AI Answer</h2>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 leading-7 text-slate-200">
              {answer}
            </div>
          </section>
        )}

        {/* Sources */}
        {sources.length > 0 && (
          <section className="mt-8">
            <h2 className="mb-3 text-xl font-semibold">📚 Retrieved Sources</h2>

            <div className="space-y-4">
              {sources.map((source, index) => (
                <div
                  key={index}
                  className="rounded-2xl border border-slate-800 bg-slate-900 p-5"
                >
                  <div className="mb-2 flex items-center justify-between">
                    <span className="font-medium text-blue-400">
                      Source {index + 1}
                    </span>

                    <span className="text-xs text-slate-500">
                      Distance: {source.distance.toFixed(4)}
                    </span>
                  </div>

                  <p className="whitespace-pre-line text-sm leading-6 text-slate-300">
                    {source.text}
                  </p>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-slate-600">
          Built with Next.js • FastAPI • ChromaDB • Gemini
        </footer>
      </div>
    </main>
  );
}

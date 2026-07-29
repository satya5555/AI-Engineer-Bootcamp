import { Prompt } from "@/types/prompt";

interface PromptCardProps {
  prompt: Prompt;
  onDelete: (id: string) => void;
}

export default function PromptCard({ prompt, onDelete }: PromptCardProps) {
  return (
    <div className="rounded-xl bg-white p-5 shadow">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-xl font-semibold text-slate-900">{prompt.title}</h3>

        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-600">
          {prompt.category}
        </span>
      </div>

      <p className="whitespace-pre-wrap text-slate-700">{prompt.content}</p>

      <div className="mt-4 flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {new Date(prompt.createdAt).toLocaleString()}
        </p>

        <button
          onClick={() => onDelete(prompt.id)}
          className="rounded-lg bg-red-500 px-3 py-2 text-sm font-medium text-white hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
}

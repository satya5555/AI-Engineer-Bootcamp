import { Prompt } from "@/types/prompt";
import PromptCard from "./PromptCard";

interface PromptListProps {
  prompts: Prompt[];
  onDelete: (id: string) => void;
}

export default function PromptList({ prompts, onDelete }: PromptListProps) {
  if (prompts.length === 0) {
    return (
      <div>
        <h2 className="mb-4 text-2xl font-semibold text-slate-900">
          Saved Prompts
        </h2>

        <p className="text-slate-500">No prompts saved yet.</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4 text-2xl font-semibold text-slate-900">
        Saved Prompts
      </h2>

      <div className="space-y-4">
        {prompts.map((prompt) => (
          <PromptCard key={prompt.id} prompt={prompt} onDelete={onDelete} />
        ))}
      </div>
    </div>
  );
}

import PromptForm from "@/components/prompts/PromptForm";
import PromptList from "@/components/prompts/PromptList";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-100 p-10 text-slate-900">
      <h1 className="text-4xl font-bold mb-8">Prompt Playground 🚀</h1>

      <PromptForm />

      <div className="mt-10">
        <PromptList />
      </div>
    </main>
  );
}

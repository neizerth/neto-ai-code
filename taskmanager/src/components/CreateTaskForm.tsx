import { useCreateTask } from "@/hooks/useTasks";
import { useState } from "react";

export function CreateTaskForm() {
  const [title, setTitle] = useState("");
  const createTask = useCreateTask();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const t = title.trim();
    if (!t) return;
    createTask.mutate(t, {
      onSuccess: () => setTitle(""),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Новая задача"
        className="flex-1 rounded border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={createTask.isPending || !title.trim()}
        className="rounded bg-blue-600 px-4 py-2 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {createTask.isPending ? "…" : "Добавить"}
      </button>
    </form>
  );
}

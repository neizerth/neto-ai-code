import type { Task } from "@/api/tasks";
import { useTaskPriority } from "@/hooks/useTaskPriority";
import { useDeleteTask, useTasks, useUpdateTask } from "@/hooks/useTasks";
import { useEffect, useRef, useState } from "react";

function TaskItem({ task }: { task: Task }) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const inputRef = useRef<HTMLInputElement>(null);
  const priority = useTaskPriority(task.dueDate);
  const updateTask = useUpdateTask();
  const deleteTask = useDeleteTask();

  useEffect(() => {
    if (editing) inputRef.current?.focus();
  }, [editing]);

  const handleSave = () => {
    const t = title.trim();
    if (t && t !== task.title) {
      updateTask.mutate({ id: task.id, patch: { title: t } });
    }
    setEditing(false);
  };

  const handleToggle = () => {
    updateTask.mutate({ id: task.id, patch: { completed: !task.completed } });
  };

  const handleDelete = () => {
    if (window.confirm("Удалить задачу?")) {
      deleteTask.mutate(task.id);
    }
  };

  if (editing) {
    return (
      <li className="flex items-center gap-2 py-2 border-b border-gray-200 last:border-0">
        <input
          ref={inputRef}
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onBlur={handleSave}
          onKeyDown={(e) => e.key === "Enter" && handleSave()}
          className="flex-1 rounded border border-gray-300 px-2 py-1"
        />
        <button
          type="button"
          onClick={handleSave}
          className="rounded bg-blue-600 px-2 py-1 text-sm text-white hover:bg-blue-700"
        >
          Сохранить
        </button>
        <button
          type="button"
          onClick={() => setEditing(false)}
          className="rounded border border-gray-300 px-2 py-1 text-sm hover:bg-gray-100"
        >
          Отмена
        </button>
      </li>
    );
  }

  return (
    <li className="flex items-center gap-3 py-2.5 px-3 border-b border-gray-200 last:border-0 group min-h-[2.75rem]">
      <input
        type="checkbox"
        checked={task.completed}
        onChange={handleToggle}
        disabled={updateTask.isPending}
        className="h-4 w-4 shrink-0 rounded border-gray-300 accent-blue-600"
      />
      <button
        type="button"
        className={`flex-1 min-w-0 leading-6 text-left bg-transparent border-0 cursor-default p-0 font-inherit ${task.completed ? "text-gray-500 line-through" : ""}`}
        onDoubleClick={() => setEditing(true)}
      >
        {task.title}
      </button>
      <span className="shrink-0 text-xs text-gray-400 tabular-nums" title="Приоритет по сроку">
        {priority}
      </span>
      <div className="opacity-0 group-hover:opacity-100 flex items-center gap-1 shrink-0">
        <button
          type="button"
          onClick={() => setEditing(true)}
          className="text-sm text-blue-600 hover:underline"
        >
          Изменить
        </button>
        <button
          type="button"
          onClick={handleDelete}
          disabled={deleteTask.isPending}
          className="text-sm text-red-600 hover:underline disabled:opacity-50"
        >
          Удалить
        </button>
      </div>
    </li>
  );
}

export function TaskList() {
  const { data: tasks, isLoading, error } = useTasks();

  if (isLoading) return <p className="text-gray-500">Загрузка…</p>;
  if (error) return <p className="text-red-600">Ошибка: {(error as Error).message}</p>;
  if (!tasks?.length) return <p className="text-gray-500">Нет задач. Добавьте первую.</p>;

  return (
    <ul className="divide-y divide-gray-200 bg-white rounded-lg border border-gray-200 overflow-hidden">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  );
}

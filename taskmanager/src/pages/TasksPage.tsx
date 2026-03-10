import { CreateTaskForm } from "@/components/CreateTaskForm";
import { TaskList } from "@/components/TaskList";
import { useAuth } from "@/contexts/AuthContext";

export function TasksPage() {
  const { user } = useAuth();

  return (
    <div className="w-full max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Мои задачи</h1>
        {user && (
          <p className="text-sm text-gray-500">
            {user.name} ({user.email})
          </p>
        )}
      </div>
      <CreateTaskForm />
      <TaskList />
    </div>
  );
}

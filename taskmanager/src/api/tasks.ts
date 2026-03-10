import { apiRequest } from "./client";

export interface Task {
  id: number;
  userId: number;
  title: string;
  completed: boolean;
  createdAt: string;
  dueDate?: string | null;
}

export function getTasks(): Promise<Task[]> {
  return apiRequest<Task[]>("/tasks");
}

export function createTask(title: string): Promise<Task> {
  return apiRequest<Task>("/tasks", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}

export function updateTask(
  id: number,
  patch: { title?: string; completed?: boolean },
): Promise<Task> {
  return apiRequest<Task>(`/tasks/${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
}

export function deleteTask(id: number): Promise<void> {
  return apiRequest<void>(`/tasks/${id}`, { method: "DELETE" }) as Promise<void>;
}

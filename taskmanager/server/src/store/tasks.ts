export interface Task {
  id: number;
  userId: number;
  title: string;
  completed: boolean;
  createdAt: string;
  dueDate?: string | null;
}

const tasks = new Map<number, Task>();
const byUser = new Map<number, number[]>();
let nextId = 1;

export function getTasksByUserId(userId: number): Task[] {
  const ids = byUser.get(userId) ?? [];
  return ids
    .map((id) => tasks.get(id))
    .filter((t): t is Task => t != null)
    .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());
}

export function getTaskById(id: number, userId: number): Task | undefined {
  const task = tasks.get(id);
  if (!task || task.userId !== userId) return undefined;
  return task;
}

export function createTask(userId: number, title: string, dueDate?: string | null): Task {
  const task: Task = {
    id: nextId++,
    userId,
    title: title.trim(),
    completed: false,
    createdAt: new Date().toISOString(),
    dueDate: dueDate ?? undefined,
  };
  tasks.set(task.id, task);
  const list = byUser.get(userId) ?? [];
  list.push(task.id);
  byUser.set(userId, list);
  return task;
}

export function updateTask(
  id: number,
  userId: number,
  patch: { title?: string; completed?: boolean; dueDate?: string | null },
): Task | undefined {
  const task = getTaskById(id, userId);
  if (!task) return undefined;
  if (patch.title !== undefined) task.title = patch.title.trim();
  if (patch.completed !== undefined) task.completed = patch.completed;
  if (patch.dueDate !== undefined) task.dueDate = patch.dueDate ?? undefined;
  return task;
}

export function deleteTask(id: number, userId: number): boolean {
  const task = getTaskById(id, userId);
  if (!task) return false;
  tasks.delete(id);
  const list = byUser.get(userId) ?? [];
  byUser.set(
    userId,
    list.filter((x) => x !== id),
  );
  return true;
}

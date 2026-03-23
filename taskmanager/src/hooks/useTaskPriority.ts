/**
 * Возвращает приоритет задачи по дате срока (dueDate).
 * Чем ближе срок — тем выше приоритет (возвращаемое значение от 0.1 до 1).
 */
export function useTaskPriority(dueDate: string | null | undefined): number {
  const MIN_PRIORITY = 0.1;
  if (!dueDate) {
    return MIN_PRIORITY;
  }
  const date = new Date(dueDate);
  const now = Date.now();
  const diff = date.getTime() - now;
  const days = diff / (1000 * 60 * 60 * 24);
  const raw = 1 / (1 + Math.max(0, days));
  return Math.max(MIN_PRIORITY, raw);
}

/**
 * Вычисляет приоритет задачи на основе даты выполнения и важности.
 * 
 * @param dueDate - Дата выполнения задачи.
 * @param importance - Важность задачи (от 1 до 10).
 * @returns Приоритет задачи (число).
 * @throws {TypeError} Если dueDate не является валидной датой.
 * @throws {RangeError} Если importance не находится в диапазоне от 1 до 10.
 */
import { differenceInDays, startOfToday } from 'date-fns';

const MAX_PRIORITY = 1000;
const BASE_FACTOR = 100;
const MIN_IMPORTANCE = 1;
const MAX_IMPORTANCE = 10;

export function calculatePriority(dueDate: Date, importance: number): number {
  // Проверка на валидность даты
  if (!dueDate || isNaN(dueDate.getTime())) {
    throw new TypeError('Invalid date: dueDate must be a valid Date object');
  }

  // Проверка диапазона важности
  if (importance < MIN_IMPORTANCE || importance > MAX_IMPORTANCE) {
    throw new RangeError(`Importance must be between ${MIN_IMPORTANCE} and ${MAX_IMPORTANCE}`);
  }

  const today = startOfToday();
  const daysLeft = differenceInDays(dueDate, today);

  // Базовый приоритет: 100, если дедлайн сегодня или просрочен
  let basePriority = daysLeft <= 0 ? BASE_FACTOR : BASE_FACTOR * daysLeft;

  // Финальный приоритет с учетом важности
  return basePriority + (importance * (MAX_PRIORITY / MAX_IMPORTANCE));
}

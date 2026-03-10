# Задание для скринкаста: модуль регистрации

## Контекст

Frontend приложения **TaskManager**: React 19, TypeScript, Vite.

**Стек:** React Query (серверное состояние), React Hook Form (формы), Zod (валидация), Tailwind CSS.

**Стиль:** Функциональные компоненты с хуками. API-вызовы в `src/api/`, кастомные хуки в `src/hooks/`, компоненты в `src/components/`.

**API:** Backend по адресу `/api`. Регистрация: **POST /api/auth/register**  
- Тело: `{ email: string, password: string }`  
- Успех 201: `{ id: number, email: string, createdAt: string }`  
- **409** — email уже занят (ошибку показать в форме).

В проекте есть глобальный обработчик ошибок мутаций через React Query `defaultOptions.mutations.onError`; при 409 нужно дополнительно показывать ошибку в форме регистрации.

Есть готовый модуль входа (логин) — можно ориентироваться на него.

## Что нужно реализовать

1. **API** — функция `registerUser` в `src/api/auth.ts`: POST `/api/auth/register`, тело `{ email, password }`, ответ `{ id, email, createdAt }`.
2. **Хук** — `useRegister` в `src/hooks/useRegister.ts` на базе React Query `useMutation`.
3. **Схема** — `registrationSchema` в `src/schemas/auth.ts` (Zod): email, password (минимум 6 символов).
4. **Компонент** — `RegistrationForm`: React Hook Form + zodResolver(registrationSchema), вызов useRegister, отображение ошибок валидации и **ошибки 409** в форме.

Код в стиле проекта: TypeScript, функциональные компоненты, принятые библиотеки.

---

## Задание: переработка хука useTaskPriority

**Задача:** Измени хук `useTaskPriority` так, чтобы он корректно обрабатывал отсутствующий `dueDate` в соответствии с бизнес-требованиями.

**Границы изменений:**
- не меняй публичный интерфейс хука;
- не изменяй поведение для случаев, когда `dueDate` задан — оно должно остаться идентичным текущей реализации;
- не добавляй новой функциональности, кроме обработки `null`/`undefined`;
- сохрани стиль кода: используй понятные имена, вынеси магическое число `0.1` в константу (например, `MIN_PRIORITY`).

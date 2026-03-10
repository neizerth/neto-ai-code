# TaskManager (frontend)

React 19, TypeScript, Vite. Стек: React Query, React Hook Form, Zod, Tailwind CSS.

Backend по адресу `/api`. Описание API — `docs/API.md`.

## Структура

- `src/api` — слой запросов к backend
- `src/hooks` — кастомные хуки (React Query и др.)
- `src/components` — React-компоненты
- `src/schemas` — валидация (Zod)

Глобальная обработка ошибок мутаций: `defaultOptions.mutations.onError` в React Query (см. `src/main.tsx`).

## Запуск

Сначала установите зависимости (в корне и в server):

```bash
npm install
cd server && npm install && cd ..
```

Запуск фронта и backend одним скриптом (порт 5173 — Vite, 3001 — API):

```bash
npm run dev
```

Или по отдельности: в одном терминале `npm run dev:server`, в другом `npm run dev:client`.

Откройте http://localhost:5173. Запросы к `/api` проксируются на Express (порт 3001). Регистрация на фронте не реализована — задание в **TASK.md**.

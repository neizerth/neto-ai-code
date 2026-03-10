# TaskManager API (Express + TypeScript)

Backend на Express. Данные пользователей в памяти; при старте создаются тестовые пользователи.

## Тестовые пользователи (логин)

| Email | Пароль |
|-------|--------|
| demo@taskmanager.local | demo |
| test@example.com | test123 |
| admin@taskmanager.local | admin |

## Эндпоинты

- **POST /api/auth/register** — `{ email, password }` → 201 `{ id, email, createdAt }` или 409 (email занят)
- **POST /api/auth/login** — `{ email, password }` → 200 `{ token, user }` или 401

## Запуск

```bash
npm install
npm run dev   # tsx watch
# или
npm run build && npm start
```

Порт по умолчанию: 3001. Фронт (Vite) проксирует `/api` на этот порт.

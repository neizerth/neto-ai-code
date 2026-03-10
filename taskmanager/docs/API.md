# TaskManager — Backend API

Backend доступен по адресу **`/api`** (то же приложение, прокси или отдельный хост).

## Аутентификация

### POST /api/auth/login

Вход в систему.

**Request body:** `{ email: string, password: string }`

**Response 200:** `{ token: string, user: { id, email, name } }`  
**Response 401:** Неверные учётные данные.

---

### POST /api/auth/register

Регистрация нового пользователя.

**Request body:**
```json
{
  "email": "user@example.com",
  "password": "secret"
}
```

**Response 201:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "createdAt": "2025-03-10T12:00:00.000Z"
}
```

**Response 409:** Конфликт — email уже занят. Ошибку нужно показать в форме (в проекте есть глобальный `onError` в React Query; для 409 обрабатывать в компоненте формы).

**Response 400:** Ошибка валидации тела запроса.

---

## Задачи (для расширения)

### GET /api/tasks

Список задач. Заголовок: `Authorization: Bearer <token>`.

### POST /api/tasks

Создание задачи. Заголовок: `Authorization: Bearer <token>`.

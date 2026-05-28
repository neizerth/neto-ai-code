# FastAPI + JWT + GigaChat — учебный пример

Мини-приложение: регистрация, выдача JWT, защищённые эндпоинты и вызов **GigaChat** из `POST /chat`.

## Что понадобится

- Python 3.11+ (проверялось на 3.13)
- Ключ GigaChat (`GIGACHAT_CREDENTIALS`)
- Для JWT — свой секрет `JWT_SECRET_KEY` (длинная случайная строка)

## Установка

Из корня каталога `12-fastapi-example`:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Переменные окружения

1. Скопируйте шаблон и заполните секреты:

   ```bash
   cp .env.example .env
   ```

2. Обязательно задайте **`JWT_SECRET_KEY`** (минимум ~32 символа). Без него регистрация и логин не работают.

3. **GigaChat:** переменные можно держать в этом же `.env`. **дополнительно**, не затирая значения из `12-fastapi-example/.env` (см. `config.py`).

Полезные опции (как в учебном GigaChat): `GIGACHAT_SCOPE`, `GIGACHAT_MODEL`, `GIGACHAT_CA_BUNDLE_FILE`, `GIGACHAT_VERIFY_SSL_CERTS`, `DEMO_DEBUG`.

## Запуск API

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Откройте интерактивную документацию: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Там же можно нажать **Authorize** и вставить токен после логина.

## Эндпоинты (кратко)

| Метод | Путь | Доступ |
|--------|------|--------|
| GET | `/` | публично — список ссылок |
| GET | `/health` | публично — `jwt_configured`, `gigachat_configured` |
| POST | `/auth/register` | публично — JSON `{"username","password"}` |
| POST | `/auth/token` | публично — форма OAuth2 (`username`, `password`) |
| GET | `/users/me` | JWT |
| POST | `/chat` | JWT — JSON `{"message":"..."}`, ответ `{"reply":"..."}` |

Пользователи хранятся **в памяти** (после перезапуска сервера нужно снова зарегистрироваться).

## Получение токена (curl)

```bash
# регистрация
curl -s -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"secret12"}'

# логин (OAuth2 password)
curl -s -X POST http://127.0.0.1:8000/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=demo&password=secret12'

# подставьте access_token из ответа
curl -s http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer <access_token>"

curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer <access_token>" \
  -H 'Content-Type: application/json' \
  -d '{"message":"Кратко опиши FastAPI одним абзацем."}'
```

## Готовый клиент на Python

```bash
export BASE_URL=http://127.0.0.1:8000
# опционально: DEMO_USER, DEMO_PASSWORD
python client_example.py
```

Скрипт регистрирует пользователя (или продолжает, если уже есть), получает токен, вызывает `/users/me` и `/chat`.

## Типичные проблемы

- **`JWT_SECRET_KEY` не задан** — в `/health` будет `jwt_configured: false`; эндпоинты авторизации вернут 503 с подсказкой.
- **Нет ключа GigaChat** — `gigachat_configured: false`; `POST /chat` вернёт 502 с текстом про `GIGACHAT_CREDENTIALS`.
- **Ошибки SSL/сертификатов** — см. комментарии в `.env.example` и учебный `gigachat_api`; для локальной отладки иногда выставляют `GIGACHAT_VERIFY_SSL_CERTS=0` (только для демо).

## Структура проекта

- `main.py` — приложение и роуты верхнего уровня
- `config.py` — загрузка `.env`
- `security.py` — JWT и bcrypt
- `routers/` — `auth`, `users`, `chat`
- `services/gigachat_service.py` — синхронный вызов GigaChat (в обработчике уходит в thread pool)

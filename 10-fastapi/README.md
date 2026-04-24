# Пример API на FastAPI (вебинар)

Набор **учебных** эндпоинтов, разбитый по **темам из презентации** «Создание API с ИИ»: приложение, роутеры, Pydantic, OpenAPI, middleware, жизненный цикл, примеры под ИИ и REST.

## Требования

- Python 3.10+

## Установка

Из каталога `10-fastapi`:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI: <http://127.0.0.1:8000/docs>  
- ReDoc: <http://127.0.0.1:8000/redoc>  
- `GET /` — краткое меню демо + время старта процесса (см. lifecycle ниже)

## Список эндпоинтов

### REST API (приложение)

| Метод | Путь | Назначение |
|--------|------|------------|
| `GET` | `/` | Сводка демо, `started_at_utc`, подсказки |
| `POST` | `/tasks` | Создать задачу (201, тело `TaskCreate`) |
| `GET` | `/tasks/{task_id}` | Получить задачу или 404 в формате `detail` / `task_id` |
| `POST` | `/generate/text` | «Генерация» (JSON `{"prompt": "..."}` → `{"result": "..."}`, заглушка) |
| `GET` | `/users/{user_id}` | Пользователь по id или 404 (`HTTPException`) |

### Служебные (OpenAPI, FastAPI)

| Метод | Путь | Назначение |
|--------|------|------------|
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc |
| `GET` | `/openapi.json` | Схема OpenAPI (JSON) |

## Примеры по темам презентации

### 1. Приложение, роутеры, Pydantic, OpenAPI, кейс с задачами

Слайды: центральное приложение `app = FastAPI()`, `app.include_router(...)`, модели запрос/ответ, автодок.

```bash
curl http://127.0.0.1:8000/

curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Сделать задание","description":null,"priority":3}'

curl http://127.0.0.1:8000/tasks/1
curl -s http://127.0.0.1:8000/tasks/999
```

### 2. Эндпоинт в духе «ИИ-генерации» (слайд: `APIRouter` + `POST` с ответом `{"result": "..."}`)

Слайд: `APIRouter(prefix="/generate", tags=["generation"])` и эндпоинт, возвращающий `result` (в коде — **заглушка**, без реального вызова LLM).

```bash
curl -X POST http://127.0.0.1:8000/generate/text \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Объясни, что такое ASGI, в одном предложении."}'
```

### 3. Промпты: `GET` + path-параметр, 404 (шаблон «/users/{user_id}»)

Слайд «Метод и путь» и сценарий «если не найден — 404» (через `HTTPException`).

```bash
curl -s http://127.0.0.1:8000/users/1
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:8000/users/99
```

### 4. Middleware (слайд: «труба» `request` → `call_next`)

Каждый ответ с заголовком `X-Process-Time` (время обработки запроса в секундах).

```bash
curl -sD - -o /dev/null http://127.0.0.1:8000/ | grep -i x-process
```

### 5. Startup / shutdown (слайды `on_event`)

В презентации: `@app.on_event("startup")` и `shutdown`. В этом репозитории используется **`lifespan`** (современный вариант той же идеи): при старте в `app.state` сохраняется `started_at`, его видно в `GET /`.

## Структура проекта

| Файл / каталог | Тема из презентации (кратко) |
|----------------|------------------------------|
| `main.py` | `FastAPI`, `include_router`, middleware, lifecycle |
| `schemas.py` | Pydantic: задачи, пользователь, тело/ответ для «генерации» |
| `routers/tasks.py` | Кейс: память, `POST/GET` `/tasks` |
| `routers/generation.py` | `APIRouter` `/generate`, `POST` `/text` |
| `routers/users.py` | `GET` `/users/{user_id}`, 404 |
| `requirements.txt` | Зависимости |

## Остановка

В терминале с Uvicorn: **Ctrl+C**.

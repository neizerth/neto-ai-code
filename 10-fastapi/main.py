"""
Темы из презентации, собранные в одном приложении:

- «Приложение» — `app = FastAPI()`
- «Регистрация роутеров» — `app.include_router(...)` для разных доменов
- «Middleware» — `@app.middleware("http")` и цепочка `call_next`
- «Startup / Shutdown» — слайды с `@app.on_event(...)`; здесь сделано через
  `lifespan` (рекомендуемый в новых версиях FastAPI способ, логика та же)
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request

from routers.generation import router as generation_router
from routers.tasks import router as tasks_router
from routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Слайд «Startup events (on_startup)»: прогрев, конфиг, соединения с БД/ML.
    Слайд «Shutdown events (on_shutdown)»: корректное закрытие.
    """
    app.state.started_at = datetime.now(timezone.utc)
    yield
    # сюда: закрытие пулов, соединений и т.п.


app = FastAPI(
    title="Демо из вебинара: FastAPI + структура API",
    version="0.2.0",
    lifespan=lifespan,
    description="Задачи (кейс), учебная «генерация» текста, GET пользователя — + middleware и lifecycle.",
)
app.include_router(tasks_router)
app.include_router(generation_router)
app.include_router(users_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Слайд «Middleware» — обёртка над каждым HTTP-запросом, порядок важен.
    """
    t0 = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{(time.perf_counter() - t0):.4f}"
    return response


@app.get("/")
async def root() -> dict:
    started = getattr(app.state, "started_at", None)
    return {
        "name": "webinar-fastapi-demos",
        "started_at_utc": started.isoformat() if started else None,
        "docs": "/docs",
        "redoc": "/redoc",
        "demos": {
            "tasks_case": "POST/GET /tasks (кейс, память, Pydantic)",
            "ai_stub": "POST /generate/text (слайд про ИИ-эндпоинт, заглушка)",
            "user_get": "GET /users/{id} (шаблон промпта, 404 по контракту)",
        },
    }

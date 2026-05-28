"""
Расширенный пример FastAPI: JWT, несколько роутеров, вызов GigaChat из защищённого эндпоинта.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

import config
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.users import router as users_router
from schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.started_at = datetime.now(timezone.utc)
    yield


app = FastAPI(
    title="FastAPI + JWT + GigaChat",
    version="1.0.0",
    lifespan=lifespan,
    description=(
        "Регистрация и логин выдают JWT. "
        "`/users/me` и `/chat` требуют заголовок `Authorization: Bearer <token>`. "
        "Переменные GigaChat те же, что в `08-task/example/gigachat_api/.env`."
    ),
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        jwt_configured=bool(config.JWT_SECRET_KEY),
        gigachat_configured=bool(config.GIGACHAT_CREDENTIALS),
    )


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {
        "docs": "/docs",
        "auth": {"register": "POST /auth/register", "token": "POST /auth/token (form)"},
        "protected": {"me": "GET /users/me", "chat": "POST /chat"},
        "public": {"health": "GET /health"},
    }

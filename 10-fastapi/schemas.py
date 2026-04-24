"""Pydantic-модели — по промпту «Генерация моделей данных» из презентации."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, field_validator


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class TaskCreate(BaseModel):
    """Вход: создание задачи (без id и created_at)."""

    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5)

    @field_validator("title")
    @classmethod
    def title_not_only_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be empty or whitespace only")
        return v


class TaskResponse(BaseModel):
    """Ответ: задача с id и created_at (ISO 8601 в JSON)."""

    id: int
    title: str
    description: Optional[str]
    priority: int
    created_at: datetime

    model_config = {"json_schema_extra": {"example": {"id": 1, "title": "Demo", "description": None, "priority": 3, "created_at": "2026-01-15T10:00:00+00:00"}}}


# —— Слайды: эндпоинт /generate (ИИ) и «GET /users/{user_id}» из шаблона промпта


class UserOut(BaseModel):
    """Слайд «Назначение эндпоинта» — получение пользователя по id (учебная заглушка)."""

    id: int
    name: str
    email: str


class TextGenerationRequest(BaseModel):
    """
    Слайд «Архитектура: эндпоинт» в виде тела JSON (в слайде — псевдокод def generate_text(prompt: str)).
    """

    prompt: str = Field(min_length=1, max_length=4_000)


class TextGenerationResponse(BaseModel):
    """Слайд: return {\"result\": \"...\"} — контракт ответа в OpenAPI."""

    result: str

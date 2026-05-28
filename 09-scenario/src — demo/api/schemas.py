from __future__ import annotations

from pydantic import BaseModel, Field


class ShoppingRequest(BaseModel):
    dish: str = Field(default="", description="Что приготовить")
    people: str = Field(default="2", description="На сколько человек")
    output_format: str = Field(default="Список продуктов", description="Формат ответа")


class ShoppingResponse(BaseModel):
    ok: bool
    message: str


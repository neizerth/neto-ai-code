from __future__ import annotations

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    username: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4_000)


class ChatResponse(BaseModel):
    reply: str


class HealthResponse(BaseModel):
    status: str
    jwt_configured: bool
    gigachat_configured: bool

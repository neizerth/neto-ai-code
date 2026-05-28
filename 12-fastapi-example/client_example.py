#!/usr/bin/env python3
"""
Простой HTTP-клиент к API: регистрация (опционально), логин, /users/me, /chat.

Запуск сервера: uvicorn main:app --reload --app-dir .
Запуск клиента:  python client_example.py
Переменные: BASE_URL (по умолчанию http://127.0.0.1:8000)
"""

from __future__ import annotations

import os
import sys

import httpx

BASE_URL = (os.environ.get("BASE_URL") or "http://127.0.0.1:8000").rstrip("/")
USER = os.environ.get("DEMO_USER") or "demo_user"
PASSWORD = os.environ.get("DEMO_PASSWORD") or "secret123"


def main() -> int:
    with httpx.Client(base_url=BASE_URL, timeout=120.0) as client:
        r = client.get("/health")
        r.raise_for_status()
        print("health:", r.json())

        # Регистрация (игнорируем 409, если пользователь уже есть)
        reg = client.post("/auth/register", json={"username": USER, "password": PASSWORD})
        if reg.status_code == 201:
            print("registered:", reg.json())
        elif reg.status_code == 409:
            print("user already exists, logging in")
        else:
            print("register failed:", reg.status_code, reg.text)
            return 1

        token_r = client.post(
            "/auth/token",
            data={"username": USER, "password": PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_r.raise_for_status()
        token = token_r.json()["access_token"]
        print("got token (truncated):", token[:20] + "...")

        headers = {"Authorization": f"Bearer {token}"}
        me = client.get("/users/me", headers=headers)
        me.raise_for_status()
        print("me:", me.json())

        chat = client.post(
            "/chat",
            json={"message": "Напиши одно предложение: что такое FastAPI?"},
            headers=headers,
        )
        if chat.status_code != 200:
            print("chat error:", chat.status_code, chat.text)
            return 1
        print("chat:", chat.json())

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except httpx.ConnectError as e:
        print(f"Не удалось подключиться к {BASE_URL}: {e}", file=sys.stderr)
        raise SystemExit(2) from e

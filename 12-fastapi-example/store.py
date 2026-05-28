"""Учебное in-memory хранилище пользователей (без БД)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserInDB:
    username: str
    hashed_password: str


_users: dict[str, UserInDB] = {}


def get_user(username: str) -> UserInDB | None:
    return _users.get(username)


def add_user(user: UserInDB) -> None:
    _users[user.username] = user


def user_exists(username: str) -> bool:
    return username in _users

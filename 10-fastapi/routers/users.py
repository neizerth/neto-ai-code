"""
Слайд «Метод и путь» + «Формат ответа и поведение» (шаблон промпта):
  HTTP-метод: GET
  Путь: /users/{user_id}
  «Если объект не найден — вернуть 404 Not Found.»
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])

_USERS: dict[int, UserOut] = {
    1: UserOut(id=1, name="Анна", email="anna@example.com"),
    2: UserOut(id=2, name="Пётр", email="peter@example.com"),
}


@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Получить пользователя по id (учебная заглушка)",
)
async def get_user(user_id: int) -> UserOut:
    user = _USERS.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user

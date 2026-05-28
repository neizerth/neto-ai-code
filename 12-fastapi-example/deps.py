from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import config
import store
import security
from store import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=True)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    if not config.JWT_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервер не настроен: задайте JWT_SECRET_KEY в .env",
        )
    username = security.decode_token_subject(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = store.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

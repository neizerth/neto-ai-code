from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from deps import get_current_user
from schemas import UserPublic
from store import UserInDB

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def read_me(current: Annotated[UserInDB, Depends(get_current_user)]) -> UserPublic:
    return UserPublic(username=current.username)

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool

import config
from deps import get_current_user
from schemas import ChatRequest, ChatResponse
from services.gigachat_service import GigachatError, chat_sync
from store import UserInDB

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current: Annotated[UserInDB, Depends(get_current_user)],
) -> ChatResponse:
    _ = current
    try:
        reply = await run_in_threadpool(chat_sync, body.message)
    except GigachatError as e:
        if config.DEMO_DEBUG:
            print(f"[debug] GigaChat: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=e.user_message,
        ) from e
    return ChatResponse(reply=reply)

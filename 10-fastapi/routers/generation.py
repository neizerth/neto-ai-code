"""
Слайд «APIRouter» + пример с генерацией (как в презентации):
  router = APIRouter(prefix="/generate", tags=["generation"])
  @router.post("/text")
  async def generate_text(...):
      return {"result": "..."}
"""

from __future__ import annotations

from fastapi import APIRouter

from schemas import TextGenerationRequest, TextGenerationResponse

router = APIRouter(prefix="/generate", tags=["generation"])


@router.post(
    "/text",
    response_model=TextGenerationResponse,
    summary="Учебная «генерация» текста (заглушка под LLM)",
)
async def generate_text(body: TextGenerationRequest) -> TextGenerationResponse:
    """
    Тело: JSON с полем `prompt`. Ответ: `{"result": "..."}` — как в слайде, без настоящей модели.
    """
    reply = f"Эхо-ответ (демо, не вызов реальной LLM): {body.prompt[:200]!r}"
    if len(body.prompt) > 200:
        reply += f"… (+ещё {len(body.prompt) - 200} симв.)"
    return TextGenerationResponse(result=reply)

from __future__ import annotations

from dataclasses import dataclass

from config.settings import get_settings
from llm.gigachat_client import generate_shopping_list


@dataclass(frozen=True)
class ServiceResult:
    ok: bool
    message: str


MAX_INPUT_CHARS = 4000


def build_shopping_list(dish: str, people: str, output_format: str) -> ServiceResult:
    cleaned = (dish or "").strip()
    if not cleaned:
        return ServiceResult(ok=False, message="Напишите блюдо.")

    if len(cleaned) > MAX_INPUT_CHARS:
        return ServiceResult(ok=False, message="Слишком длинный текст — сократите.")

    try:
        text = generate_shopping_list(cleaned, people, output_format)
        if not text:
            return ServiceResult(ok=False, message="Пустой ответ. Попробуйте ещё раз.")
        return ServiceResult(ok=True, message=text)
    except Exception as e:
        s = get_settings()
        if s.demo_debug:
            print(f"[debug] service error: {type(e).__name__}: {e!s}")

        msg = str(e)
        lower = msg.lower()
        if "GIGACHAT_CREDENTIALS" in msg:
            return ServiceResult(ok=False, message="Нет ключа GIGACHAT_CREDENTIALS.")
        if "ssl" in lower or "certificate" in lower or "certificate_verify_failed" in lower:
            return ServiceResult(ok=False, message="Проблема с сертификатами.")
        if "401" in msg or "unauthorized" in lower:
            return ServiceResult(ok=False, message="Нет доступа. Проверьте ключ.")
        if "timeout" in lower or "timed out" in lower:
            return ServiceResult(ok=False, message="Нет связи. Попробуйте позже.")
        if any(code in msg for code in ("500", "502", "503")):
            return ServiceResult(ok=False, message="Сервис недоступен. Попробуйте позже.")

        return ServiceResult(ok=False, message="Не удалось получить ответ. Попробуйте позже.")


from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI


@dataclass(frozen=True)
class LLMResult:
    ok: bool
    message: str


MAX_INPUT_CHARS = 8000


def _load_env() -> None:
    # Подхватываем .env из окружения демо, независимо от cwd.
    # Приоритет: переменные окружения уже выставлены -> не перетираем.
    here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(here, ".env"), override=False)
    # Если ключа нет — пробуем найти .env выше по дереву (на случай запуска из другой папки).
    if not os.environ.get("OPENAI_API_KEY"):
        path = find_dotenv(usecwd=True)
        if path:
            load_dotenv(path, override=False)


def call_llm(text: str, tone: str) -> str:
    _load_env()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key, timeout=30)

    resp = client.responses.create(
        model="gpt-4.1-mini",
        instructions="Пиши по-русски, без воды. 3–6 предложений.",
        input=(
            "Сценарий: ответ студенту в учебном чате.\n"
            f"Тон: {tone}.\n"
            f"Вопрос студента:\n{text}\n"
        ),
    )

    return resp.output_text or ""


def handle_student_question(text: str, tone: str) -> LLMResult:
    cleaned = (text or "").strip()
    if not cleaned:
        return LLMResult(ok=False, message="Введите вопрос студента.")

    if len(cleaned) > MAX_INPUT_CHARS:
        return LLMResult(
            ok=False,
            message="Слишком длинный текст — сократите или разбейте на части.",
        )

    try:
        answer = call_llm(cleaned, tone)
        if not answer.strip():
            return LLMResult(ok=False, message="Пустой ответ модели. Повторите запрос.")
        return LLMResult(ok=True, message=answer)
    except Exception as e:
        debug = os.environ.get("DEMO_DEBUG") == "1"
        if debug:
            # Печатаем причину только в режиме отладки, без секретов.
            print(f"[debug] LLM call failed: {type(e).__name__}: {e!s}")
            print(f"[debug] OPENAI_API_KEY present: {bool(os.environ.get('OPENAI_API_KEY'))}")

        if isinstance(e, RuntimeError) and "OPENAI_API_KEY" in str(e):
            return LLMResult(
                ok=False,
                message="Не найден OPENAI_API_KEY. Проверьте переменную окружения или файл 07-presentation/demo/01/.env",
            )

        # Попробуем распознать типовые ошибки OpenAI SDK (v1.x)
        name = type(e).__name__
        if name in {"AuthenticationError"}:
            return LLMResult(ok=False, message="Доступ не настроен: проверьте OPENAI_API_KEY.")
        if name in {"RateLimitError"}:
            msg = str(e)
            # OpenAI часто отдаёт 429 не только за частоту, но и за недостаток квоты.
            if "insufficient_quota" in msg or "check your plan and billing details" in msg:
                return LLMResult(
                    ok=False,
                    message="Квота на запросы закончилась или не подключён биллинг. Проверьте кредиты/оплату и попробуйте снова.",
                )
            return LLMResult(ok=False, message="Слишком много запросов. Подождите и попробуйте ещё раз.")
        if name in {"APITimeoutError", "APIConnectionError"}:
            return LLMResult(ok=False, message="Нет связи с API. Попробуйте ещё раз позже.")
        if name in {"APIStatusError"}:
            return LLMResult(ok=False, message="Сервис временно недоступен. Попробуйте позже.")

        # Универсальная ошибка для пользователя
        return LLMResult(
            ok=False,
            message="Не удалось сгенерировать ответ студенту. Попробуйте ещё раз позже.",
        )


def _cli() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Быстрая проверка вызова LLM для демо (без UI).",
    )
    parser.add_argument(
        "--tone",
        choices=["Нейтрально", "Дружелюбно"],
        default="Нейтрально",
        help="Тон ответа",
    )
    parser.add_argument(
        "--text",
        default="",
        help="Вопрос студента. Если не задан — читаем из stdin.",
    )
    args = parser.parse_args()

    text = args.text.strip()
    if not text:
        try:
            text = (input("Вопрос студента: ") or "").strip()
        except EOFError:
            text = ""

    result = handle_student_question(text, args.tone)
    if result.ok:
        print(result.message)
        return 0

    print(f"Ошибка: {result.message}")
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())


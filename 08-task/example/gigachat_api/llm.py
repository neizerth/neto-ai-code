from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv
from gigachat import GigaChat


@dataclass(frozen=True)
class LLMResult:
    ok: bool
    message: str


MAX_INPUT_CHARS = 4000


def _load_env() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(here, ".env"), override=False)
    if not os.environ.get("GIGACHAT_CREDENTIALS"):
        path = find_dotenv(usecwd=True)
        if path:
            load_dotenv(path, override=False)


def call_llm(dish: str, people: str, output_format: str) -> str:
    _load_env()

    credentials = os.environ.get("GIGACHAT_CREDENTIALS")
    if not credentials:
        raise RuntimeError("GIGACHAT_CREDENTIALS is not set")

    scope = os.environ.get("GIGACHAT_SCOPE") or "GIGACHAT_API_PERS"
    model = os.environ.get("GIGACHAT_MODEL") or "GigaChat"
    verify_ssl_certs = (os.environ.get("GIGACHAT_VERIFY_SSL_CERTS") or "1") != "0"
    ca_bundle_file = (os.environ.get("GIGACHAT_CA_BUNDLE_FILE") or "").strip() or None

    prompt = (
        "Составь список покупок для блюда.\n"
        f"Блюдо: {dish}\n"
        f"На сколько человек: {people}\n"
        f"Формат: {output_format}\n"
        "\n"
        "Правила:\n"
        "- Пиши по-русски.\n"
        "- В ответе сначала список продуктов (по одному на строку).\n"
        "- Если выбрано «Список + шаги», после списка добавь шаги приготовления (5–8 пунктов).\n"
        "- Без лишних вступлений.\n"
    )

    with GigaChat(
        credentials=credentials,
        scope=scope,
        model=model,
        verify_ssl_certs=verify_ssl_certs,
        ca_bundle_file=ca_bundle_file,
    ) as client:
        resp = client.chat(prompt)

    try:
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return ""


def handle_request(dish: str, people: str, output_format: str) -> LLMResult:
    cleaned = (dish or "").strip()
    if not cleaned:
        return LLMResult(ok=False, message="Напишите, что хотите приготовить.")

    if len(cleaned) > MAX_INPUT_CHARS:
        return LLMResult(ok=False, message="Слишком длинный текст — сократите.")

    try:
        answer = call_llm(cleaned, people, output_format)
        if not answer:
            return LLMResult(ok=False, message="Пустой ответ. Попробуйте ещё раз.")
        return LLMResult(ok=True, message=answer)
    except Exception as e:
        debug = os.environ.get("DEMO_DEBUG") == "1"
        if debug:
            print(f"[debug] GigaChat call failed: {type(e).__name__}: {e!s}")
            print(f"[debug] GIGACHAT_CREDENTIALS present: {bool(os.environ.get('GIGACHAT_CREDENTIALS'))}")

        msg = str(e)
        if isinstance(e, RuntimeError) and "GIGACHAT_CREDENTIALS" in msg:
            return LLMResult(
                ok=False,
                message=(
                    "Не найден ключ. Проверьте переменную окружения GIGACHAT_CREDENTIALS "
                    "или файл 08-task/example/gigachat_api/.env"
                ),
            )

        name = type(e).__name__
        lower = msg.lower()
        if (
            "ssl" in lower
            or "certificate" in lower
            or "certifi" in lower
            or "cert" in lower
            or "certificate_verify_failed" in lower
        ):
            return LLMResult(
                ok=False,
                message="Проблема с сертификатами. Установите сертификаты НУЦ Минцифры или задайте GIGACHAT_VERIFY_SSL_CERTS=0 для демо.",
            )
        if "Authentication" in name or "Unauthorized" in name or "401" in msg:
            return LLMResult(ok=False, message="Доступ не настроен. Проверьте ключ.")
        if "Timeout" in name or "timed out" in msg:
            return LLMResult(ok=False, message="Нет связи с сервисом. Попробуйте позже.")
        if "500" in msg or "502" in msg or "503" in msg:
            return LLMResult(ok=False, message="Сервис временно недоступен. Попробуйте позже.")

        return LLMResult(ok=False, message="Не удалось получить ответ. Попробуйте позже.")


def _cli() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Пример вызова GigaChat API (без UI).")
    parser.add_argument("--dish", default="", help="Что приготовить")
    parser.add_argument("--people", choices=["1", "2", "4", "6"], default="2", help="На сколько человек")
    parser.add_argument(
        "--format",
        choices=["Список продуктов", "Список + шаги"],
        default="Список продуктов",
        help="Формат ответа",
    )
    args = parser.parse_args()

    dish = args.dish.strip()
    if not dish:
        try:
            dish = (input("Что приготовить: ") or "").strip()
        except EOFError:
            dish = ""

    result = handle_request(dish, args.people, args.format)
    if result.ok:
        print(result.message)
        return 0

    print(f"Ошибка: {result.message}")
    return 2


if __name__ == "__main__":
    raise SystemExit(_cli())


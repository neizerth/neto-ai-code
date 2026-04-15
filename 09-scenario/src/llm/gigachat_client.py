from __future__ import annotations

from gigachat import GigaChat

from config.settings import get_settings


def generate_shopping_list(dish: str, people: str, output_format: str) -> str:
    s = get_settings()
    if not s.gigachat_credentials:
        raise RuntimeError("GIGACHAT_CREDENTIALS is not set")

    prompt = (
        "Составь список покупок.\n"
        f"Блюдо: {dish}\n"
        f"На сколько человек: {people}\n"
        f"Формат: {output_format}\n"
        "\n"
        "Правила:\n"
        "- Пиши по-русски.\n"
        "- Сначала список продуктов (по одному на строку).\n"
        "- Если выбран «Список + шаги», после списка добавь шаги (5–8 пунктов).\n"
        "- Без вступления.\n"
    )

    with GigaChat(
        credentials=s.gigachat_credentials,
        scope=s.gigachat_scope,
        model=s.gigachat_model,
        verify_ssl_certs=s.gigachat_verify_ssl_certs,
        ca_bundle_file=s.gigachat_ca_bundle_file,
    ) as client:
        resp = client.chat(prompt)

    try:
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        return ""


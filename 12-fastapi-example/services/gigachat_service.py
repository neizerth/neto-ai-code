from __future__ import annotations

from gigachat import GigaChat

import config


class GigachatError(Exception):
    def __init__(self, message: str, *, user_message: str | None = None) -> None:
        super().__init__(message)
        self.user_message = user_message or message


def chat_sync(user_message: str) -> str:
    if not config.GIGACHAT_CREDENTIALS:
        raise GigachatError(
            "GIGACHAT_CREDENTIALS missing",
            user_message=(
                "Не задан GIGACHAT_CREDENTIALS. Скопируйте переменные из "
                "08-task/example/gigachat_api/.env или создайте 12-fastapi-example/.env"
            ),
        )

    text = (user_message or "").strip()
    if len(text) > config.MAX_CHAT_CHARS:
        raise GigachatError("message too long", user_message="Сообщение слишком длинное.")

    with GigaChat(
        credentials=config.GIGACHAT_CREDENTIALS,
        scope=config.GIGACHAT_SCOPE,
        model=config.GIGACHAT_MODEL,
        verify_ssl_certs=config.GIGACHAT_VERIFY_SSL_CERTS,
        ca_bundle_file=config.GIGACHAT_CA_BUNDLE_FILE,
    ) as client:
        resp = client.chat(text)

    try:
        out = (resp.choices[0].message.content or "").strip()
    except Exception:
        out = ""

    if not out:
        raise GigachatError("empty response", user_message="Пустой ответ от модели. Попробуйте ещё раз.")
    return out

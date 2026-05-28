from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv


def _load_env() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(here, ".env"), override=False)
    path = find_dotenv(usecwd=True)
    if path:
        load_dotenv(path, override=False)


@dataclass(frozen=True)
class Settings:
    gigachat_credentials: str
    gigachat_scope: str
    gigachat_model: str
    gigachat_verify_ssl_certs: bool
    gigachat_ca_bundle_file: str | None
    demo_debug: bool


def get_settings() -> Settings:
    _load_env()

    credentials = os.environ.get("GIGACHAT_CREDENTIALS", "").strip()
    scope = (os.environ.get("GIGACHAT_SCOPE") or "GIGACHAT_API_PERS").strip()
    model = (os.environ.get("GIGACHAT_MODEL") or "GigaChat").strip()
    verify_ssl_certs = (os.environ.get("GIGACHAT_VERIFY_SSL_CERTS") or "1").strip() != "0"
    ca_bundle_file = (os.environ.get("GIGACHAT_CA_BUNDLE_FILE") or "").strip() or None
    demo_debug = (os.environ.get("DEMO_DEBUG") or "").strip() == "1"

    return Settings(
        gigachat_credentials=credentials,
        gigachat_scope=scope,
        gigachat_model=model,
        gigachat_verify_ssl_certs=verify_ssl_certs,
        gigachat_ca_bundle_file=ca_bundle_file,
        demo_debug=demo_debug,
    )


from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent

load_dotenv(_ROOT / ".env")
# Те же переменные, что в учебном примере GigaChat (без дублирования .env)
_giga_shared = _ROOT.parent / "08-task" / "example" / "gigachat_api" / ".env"
if _giga_shared.is_file():
    load_dotenv(_giga_shared, override=False)


def _getenv(name: str, default: str | None = None) -> str | None:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        return default
    return v


JWT_SECRET_KEY: str = _getenv("JWT_SECRET_KEY") or ""
JWT_ALGORITHM: str = _getenv("JWT_ALGORITHM") or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(_getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or "60")

GIGACHAT_CREDENTIALS: str | None = _getenv("GIGACHAT_CREDENTIALS")
GIGACHAT_SCOPE: str = _getenv("GIGACHAT_SCOPE") or "GIGACHAT_API_PERS"
GIGACHAT_MODEL: str = _getenv("GIGACHAT_MODEL") or "GigaChat"
GIGACHAT_VERIFY_SSL_CERTS: bool = (_getenv("GIGACHAT_VERIFY_SSL_CERTS") or "1") != "0"
GIGACHAT_CA_BUNDLE_FILE: str | None = (_getenv("GIGACHAT_CA_BUNDLE_FILE") or "").strip() or None
DEMO_DEBUG: bool = _getenv("DEMO_DEBUG") == "1"

MAX_CHAT_CHARS = 4000

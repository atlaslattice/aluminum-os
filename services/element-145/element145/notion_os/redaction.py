from __future__ import annotations

import re
from typing import Any

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{10,}"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*[A-Za-z0-9_-]+"),
    re.compile(r"Bearer\s+[A-Za-z0-9\._-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----"),
]

SECRET_FIELD_NAMES = {
    "api_key",
    "apikey",
    "secret",
    "client_secret",
    "token",
    "access_token",
    "refresh_token",
    "password",
    "credential",
    "credentials",
    "auth",
    "authorization",
    "bearer",
    "private_key",
    "notion_token",
    "github_token",
    "openai_api_key",
    "anthropic_api_key",
    "gemini_api_key",
    "xai_api_key",
    "deepseek_api_key",
}


def _is_secret_field(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_").replace(" ", "_")
    return normalized in SECRET_FIELD_NAMES or any(part in normalized for part in ("api_key", "secret", "token", "password"))


def redact_secrets(obj: Any) -> Any:
    if isinstance(obj, dict):
        redacted = {}
        for k, v in obj.items():
            if _is_secret_field(str(k)):
                redacted[k] = "[REDACTED]"
            else:
                redacted[k] = redact_secrets(v)
        return redacted
    if isinstance(obj, list):
        return [redact_secrets(v) for v in obj]
    if isinstance(obj, str):
        redacted = obj
        for pat in SECRET_PATTERNS:
            redacted = pat.sub("[REDACTED]", redacted)
        return redacted
    return obj

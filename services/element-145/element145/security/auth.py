"""Minimal token auth helper for Element 145.

This is deliberately small and local. Production token minting must be gated
by settings/API policy; this module only signs/verifies tokens.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuthToken:
    sub: str
    level: str
    domains: list[str]
    exp: float

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.exp


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unb64(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


class TokenAuth:
    def __init__(self, secret: str, expiry_hours: int = 24) -> None:
        if not secret:
            raise ValueError("secret is required")
        self.secret = secret.encode()
        self.expiry_hours = expiry_hours

    def issue_token(self, sub: str, level: str = "read", domains: list[str] | None = None) -> str:
        payload = {
            "sub": sub,
            "level": level,
            "domains": domains or [],
            "exp": time.time() + (self.expiry_hours * 3600),
        }
        raw = json.dumps(payload, sort_keys=True).encode()
        sig = hmac.new(self.secret, raw, hashlib.sha256).digest()
        return f"{_b64(raw)}.{_b64(sig)}"

    def verify(self, raw_token: str) -> AuthToken | None:
        try:
            payload_b64, sig_b64 = raw_token.split(".", 1)
            raw = _unb64(payload_b64)
            sig = _unb64(sig_b64)
            expected = hmac.new(self.secret, raw, hashlib.sha256).digest()
            if not hmac.compare_digest(sig, expected):
                return None
            payload: dict[str, Any] = json.loads(raw)
            token = AuthToken(
                sub=str(payload["sub"]),
                level=str(payload.get("level", "read")),
                domains=list(payload.get("domains", [])),
                exp=float(payload["exp"]),
            )
            if token.is_expired:
                return None
            return token
        except Exception:
            return None

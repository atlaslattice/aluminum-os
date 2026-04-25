"""Handler registry for Element 145."""
from __future__ import annotations

from typing import Dict

from element145.handlers.base import BaseHandler, SimpleHandler


class HandlerRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, BaseHandler] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register("general", SimpleHandler())

    def register(self, domain: str, handler: BaseHandler) -> None:
        self._handlers[domain] = handler

    def get(self, domain: str) -> BaseHandler:
        return self._handlers.get(domain) or self._handlers["general"]

    @property
    def domains(self) -> list[str]:
        return list(self._handlers.keys())

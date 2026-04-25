"""Element 145 circuit breaker utility.

Low-risk runtime utility imported from the Microsoft Copilot Aluminum Phase-1
lineage and tightened for Aluminum OS reconciliation.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Awaitable, TypeVar, Any

T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """Small async-friendly circuit breaker for service fault isolation."""

    name: str
    failure_threshold: int = 5
    recovery_timeout_s: float = 30.0
    success_threshold: int = 2
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_at: float = 0.0
    opened_at: float = 0.0
    calls_allowed: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_open(self) -> bool:
        self._maybe_transition_to_half_open()
        return self.state == CircuitState.OPEN

    @property
    def is_closed(self) -> bool:
        return self.state == CircuitState.CLOSED

    def allow_request(self) -> bool:
        """Return whether a guarded request may be attempted."""
        self._maybe_transition_to_half_open()
        return self.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN)

    async def call(self, fn: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute an async callable through the breaker."""
        if not self.allow_request():
            raise RuntimeError(f"Circuit breaker {self.name!r} is open")
        try:
            result = await fn(*args, **kwargs)
        except Exception:
            self.record_failure()
            raise
        self.record_success()
        return result

    def record_success(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.close()
            return
        self.failure_count = 0
        self.success_count += 1

    def record_failure(self) -> None:
        self.failure_count += 1
        self.success_count = 0
        self.last_failure_at = time.time()
        if self.failure_count >= self.failure_threshold:
            self.open()

    def open(self) -> None:
        self.state = CircuitState.OPEN
        self.opened_at = time.time()
        self.calls_allowed = 0

    def close(self) -> None:
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.opened_at = 0.0

    def half_open(self) -> None:
        self.state = CircuitState.HALF_OPEN
        self.success_count = 0
        self.calls_allowed += 1

    def _maybe_transition_to_half_open(self) -> None:
        if self.state != CircuitState.OPEN:
            return
        if time.time() - self.opened_at >= self.recovery_timeout_s:
            self.half_open()

    def snapshot(self) -> dict[str, Any]:
        self._maybe_transition_to_half_open()
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_at": self.last_failure_at,
            "opened_at": self.opened_at,
            "recovery_timeout_s": self.recovery_timeout_s,
        }


class CircuitBreakerRegistry:
    """Registry of circuit breakers keyed by service/provider name."""

    def __init__(self) -> None:
        self._breakers: dict[str, CircuitBreaker] = {}

    def get_or_create(self, name: str, **kwargs: Any) -> CircuitBreaker:
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name=name, **kwargs)
        return self._breakers[name]

    def get(self, name: str) -> CircuitBreaker | None:
        return self._breakers.get(name)

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return {name: breaker.snapshot() for name, breaker in self._breakers.items()}

"""Local stub provider for safe execution testing."""
from __future__ import annotations

from element145.integrations.providers.base import ProviderExecutionResult


class LocalStubProvider:
    provider = "local_stub"

    async def execute(self, envelope: dict) -> ProviderExecutionResult:
        return ProviderExecutionResult(
            provider=self.provider,
            status="simulated",
            action=envelope.get("action", "unknown"),
            dry_run=envelope.get("dry_run", True),
            payload={"echo": envelope},
            metadata={"note": "local stub execution only"},
        )

"""Notion OS integration for Aluminum / Element 145.

Notion is the operator filesystem and JANUS checkpoint surface, not the kernel.
"""

from .config import NotionOSConfig
from .models import (
    ArtifactRecord,
    ArtifactStatus,
    DataClassification,
    IntegrationDecision,
    JanusCheckpoint,
    NotionWriteResult,
)
from .runtime import NotionOSRuntime

__all__ = [
    "ArtifactRecord",
    "ArtifactStatus",
    "DataClassification",
    "IntegrationDecision",
    "JanusCheckpoint",
    "NotionOSConfig",
    "NotionOSRuntime",
    "NotionWriteResult",
]

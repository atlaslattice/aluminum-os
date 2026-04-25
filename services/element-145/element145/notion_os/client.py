from __future__ import annotations

import json
from typing import Any

from element145.notion_os.config import NotionOSConfig
from element145.notion_os.models import NotionWriteResult
from element145.notion_os.redaction import redact_secrets


class NotionOSClient:
    """Small Notion API wrapper for operator filesystem writes.

    Notion is a visibility layer, not execution authority. This client does not
    bypass ConsentKernel and does not execute provider calls.
    """

    def __init__(self, config: NotionOSConfig | None = None) -> None:
        self.config = config or NotionOSConfig.from_env()
        self._client = None

    @property
    def enabled(self) -> bool:
        return bool(self.config.api_token)

    def _get_client(self):
        if not self.enabled:
            raise RuntimeError("NOTION_API_TOKEN is not configured")
        if self._client is None:
            try:
                from notion_client import Client
            except ImportError as e:
                raise RuntimeError("notion-client package is required for Notion writes") from e
            self._client = Client(auth=self.config.api_token)
        return self._client

    def create_database_page(
        self,
        *,
        database_id: str | None,
        title: str,
        kind: str,
        payload: dict[str, Any],
        classification: str = "INTERNAL",
    ) -> NotionWriteResult:
        if not database_id:
            raise RuntimeError(f"Missing Notion database id for {kind}")

        safe_payload = redact_secrets(payload)
        notion = self._get_client()
        payload_json = json.dumps(safe_payload, indent=2, default=str)

        page = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": title[:2000]}}]},
                "Kind": {"rich_text": [{"text": {"content": kind[:2000]}}]},
                "Classification": {"select": {"name": classification}},
                "Payload": {"rich_text": [{"text": {"content": payload_json[:1900]}}]},
            },
        )
        return NotionWriteResult(
            ok=True,
            kind=kind,
            notion_url=page.get("url"),
            notion_id=page.get("id"),
        )

    def create_child_page(
        self,
        *,
        parent_page_id: str | None,
        title: str,
        kind: str,
        markdown: str,
        classification: str = "INTERNAL",
    ) -> NotionWriteResult:
        if not parent_page_id:
            raise RuntimeError("Missing Notion root page id")

        safe_markdown = redact_secrets(markdown)
        notion = self._get_client()
        page = notion.pages.create(
            parent={"page_id": parent_page_id},
            properties={"title": {"title": [{"text": {"content": title[:2000]}}]}},
            children=[
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": f"Kind: {kind} | Classification: {classification}"}}]}},
                {"object": "block", "type": "code", "code": {"language": "markdown", "rich_text": [{"text": {"content": str(safe_markdown)[:1900]}}]}},
            ],
        )
        return NotionWriteResult(ok=True, kind=kind, notion_url=page.get("url"), notion_id=page.get("id"))

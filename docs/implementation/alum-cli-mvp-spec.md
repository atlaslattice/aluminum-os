# alum CLI MVP Specification

**Status:** Candidate implementation spec
**Owner:** Aluminum OS / Atlas Lattice
**Purpose:** Define the first runnable Aluminum OS demo using a provider-agnostic CLI routed through `uws`.

---

## 1. MVP Goal

The MVP proves the core Aluminum thesis:

> One safe, auditable command surface can operate across multiple productivity ecosystems through normalized provider drivers.

The first demo should show one human or AI agent using the same command grammar across Google Workspace and Microsoft 365 for mail, calendar, and drive operations.

This is not the full Aluminum substrate. It is the smallest useful wedge.

---

## 2. Non-goals

Do not include these in the MVP:

- bare-metal OS work;
- microkernel work;
- full Pantheon Council orchestration;
- long-term memory substrate;
- all provider support;
- full GUI;
- autonomous write operations without confirmation;
- complex sync conflict resolution.

These remain important later. They are not required for the first demo.

---

## 3. Providers

MVP providers:

```text
google
microsoft
```

Provider aliases:

```text
gws -> google
workspace -> google
graph -> microsoft
ms365 -> microsoft
o365 -> microsoft
```

Provider selector:

```bash
--provider google
--provider microsoft
--provider all
```

If `--provider` is omitted, the CLI may use a configured default provider.

---

## 4. Resources and Commands

### 4.1 Mail

```bash
alum mail list [--provider google|microsoft|all] [--limit N] [--query TEXT] [--json]
alum mail get --id ID [--provider google|microsoft] [--json]
alum mail send --to EMAIL --subject TEXT --body TEXT [--provider google|microsoft] --confirm [--json]
```

### 4.2 Calendar

```bash
alum calendar list [--provider google|microsoft|all] [--from DATE] [--to DATE] [--json]
alum calendar create --title TEXT --start ISO_DATETIME --end ISO_DATETIME [--attendee EMAIL] [--provider google|microsoft] --confirm [--json]
```

### 4.3 Drive

```bash
alum drive list [--provider google|microsoft|all] [--limit N] [--json]
alum drive search QUERY [--provider google|microsoft|all] [--limit N] [--json]
```

---

## 5. Safety Rules

### 5.1 Read operations

Read operations may run without explicit confirmation:

- `mail list`
- `mail get`
- `calendar list`
- `drive list`
- `drive search`

### 5.2 Write operations

Write operations must require confirmation:

- `mail send`
- `calendar create`

Accepted confirmation models:

```bash
--confirm
```

or interactive prompt:

```text
About to send email via microsoft:
To: alice@example.com
Subject: Hello
Proceed? [y/N]
```

Default answer must be no.

### 5.3 Dry run

Every write operation should support:

```bash
--dry-run
```

Dry run prints the normalized operation payload and provider route without executing the write.

---

## 6. Routing Through uws

Early `alum` is a wrapper over `uws`.

Example mappings:

### Google mail list

```bash
alum mail list --provider google --limit 10
```

routes to:

```bash
uws gmail users messages list --params '{"userId":"me","maxResults":10}'
```

### Microsoft mail list

```bash
alum mail list --provider microsoft --limit 10
```

routes to:

```bash
uws ms-mail messages list --params '{"$top":10}'
```

### Google calendar list

```bash
alum calendar list --provider google --from 2026-04-25 --to 2026-04-26
```

routes to:

```bash
uws calendar events list --params '{"calendarId":"primary","timeMin":"2026-04-25T00:00:00Z","timeMax":"2026-04-26T00:00:00Z","singleEvents":true}'
```

### Microsoft calendar list

```bash
alum calendar list --provider microsoft --from 2026-04-25 --to 2026-04-26
```

routes to:

```bash
uws ms-calendar events list --params '{"startDateTime":"2026-04-25T00:00:00Z","endDateTime":"2026-04-26T00:00:00Z"}'
```

---

## 7. Normalized Output Schemas

All commands return an envelope.

```json
{
  "ok": true,
  "command": "mail.list",
  "provider": "google",
  "request_id": "req_...",
  "data": [],
  "audit": {
    "timestamp": "2026-04-25T00:00:00Z",
    "actor": "local-user",
    "operation": "mail.list",
    "provider": "google",
    "write": false,
    "confirmed": false,
    "dry_run": false
  },
  "errors": []
}
```

### 7.1 Mail message

```json
{
  "id": "provider-message-id",
  "provider": "google",
  "thread_id": "provider-thread-id",
  "subject": "Subject line",
  "from": {
    "name": "Alice Example",
    "email": "alice@example.com"
  },
  "to": [
    {"name": "Dave", "email": "dave@example.com"}
  ],
  "received_at": "2026-04-25T00:00:00Z",
  "snippet": "Short preview text",
  "unread": true,
  "has_attachments": false,
  "raw": {}
}
```

### 7.2 Calendar event

```json
{
  "id": "provider-event-id",
  "provider": "microsoft",
  "title": "Team sync",
  "start": "2026-04-25T15:00:00Z",
  "end": "2026-04-25T16:00:00Z",
  "timezone": "UTC",
  "location": null,
  "attendees": [
    {"name": "Alice Example", "email": "alice@example.com", "status": "needsAction"}
  ],
  "meeting_url": null,
  "raw": {}
}
```

### 7.3 Drive item

```json
{
  "id": "provider-file-id",
  "provider": "google",
  "name": "Q1 Budget.xlsx",
  "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "kind": "file",
  "web_url": "https://...",
  "created_at": "2026-04-25T00:00:00Z",
  "updated_at": "2026-04-25T00:00:00Z",
  "owner": {
    "name": "Dave",
    "email": "dave@example.com"
  },
  "raw": {}
}
```

---

## 8. Error Model

Errors use the same envelope.

```json
{
  "ok": false,
  "command": "mail.send",
  "provider": "microsoft",
  "request_id": "req_...",
  "data": null,
  "audit": {
    "timestamp": "2026-04-25T00:00:00Z",
    "actor": "local-user",
    "operation": "mail.send",
    "provider": "microsoft",
    "write": true,
    "confirmed": false,
    "dry_run": false
  },
  "errors": [
    {
      "code": "CONFIRMATION_REQUIRED",
      "message": "mail.send requires --confirm or interactive approval",
      "provider_code": null,
      "retryable": false
    }
  ]
}
```

Standard error codes:

```text
AUTH_REQUIRED
AUTH_EXPIRED
PROVIDER_UNAVAILABLE
UNSUPPORTED_PROVIDER
UNSUPPORTED_RESOURCE
INVALID_ARGUMENT
CONFIRMATION_REQUIRED
PROVIDER_ERROR
NORMALIZATION_ERROR
RATE_LIMITED
UNKNOWN_ERROR
```

---

## 9. Audit Log

Every operation should emit an audit record.

Minimum audit fields:

```json
{
  "timestamp": "2026-04-25T00:00:00Z",
  "request_id": "req_...",
  "actor": "local-user",
  "command": "mail.list",
  "provider": "google",
  "write": false,
  "confirmed": false,
  "dry_run": false,
  "route": "uws gmail users messages list",
  "result": "ok"
}
```

MVP audit destination:

```bash
--audit-log ./alum-audit.ndjson
```

Default may be stdout/stderr until persistence is implemented.

---

## 10. Demo Script

A successful MVP demo should run:

```bash
alum mail list --provider google --limit 5 --json
alum mail list --provider microsoft --limit 5 --json
alum calendar list --provider all --from today --to tomorrow --json
alum drive search "budget" --provider all --limit 5 --json
alum mail send --provider google --to test@example.com --subject "Aluminum demo" --body "Hello from alum" --dry-run --json
alum calendar create --provider microsoft --title "Aluminum demo" --start 2026-04-25T15:00:00Z --end 2026-04-25T15:30:00Z --dry-run --json
```

No destructive action is required for the demo.

---

## 11. Acceptance Criteria

MVP is complete when:

- `alum` binary or script exists;
- commands above run locally;
- Google and Microsoft routes are both supported for at least read operations;
- write operations refuse to run without confirmation or dry-run;
- output envelope is stable;
- audit records are emitted;
- README links to this spec;
- at least one agent can invoke `alum` safely through a documented skill file.

---

## 12. Implementation Notes

Preferred implementation path:

1. Create lightweight `alum` wrapper package.
2. Parse commands with a strict CLI parser.
3. Convert friendly `alum` commands into provider-specific `uws` calls.
4. Execute `uws` as subprocess for MVP.
5. Normalize results into Aluminum schemas.
6. Add confirmation gates for writes.
7. Emit audit records.

Longer-term path:

- replace subprocess routing with direct provider driver calls;
- move normalized schemas into shared library;
- add policy engine hooks;
- add provenance graph persistence;
- add memory substrate integration.

---

## 13. Working Doctrine

Do not expand the MVP until the demo works.

The first win is not philosophical completeness. The first win is one command surface operating safely across two providers.
# Provider Driver Interface

**Status:** Candidate architecture contract
**Purpose:** Define the canonical provider-driver boundary for Aluminum OS, `alum`, and `uws`.

---

## 1. Contract Goal

Provider drivers make productivity ecosystems interchangeable.

A driver hides provider-specific APIs behind a stable Aluminum interface so that the same high-level command can operate across Google Workspace, Microsoft 365, Apple/iCloud, Android, Chrome, GitHub, Notion, and future systems.

The first implementation target is Google Workspace + Microsoft 365.

---

## 2. Design Principle

Provider-specific complexity belongs inside drivers.

Aluminum-facing commands should never need to know whether mail comes from Gmail, Outlook, iCloud Mail, or another backend.

```text
alum command
    |
    v
normalized operation
    |
    v
provider driver
    |
    v
provider API
```

---

## 3. Provider Identity

Each driver exposes a provider descriptor.

```json
{
  "provider": "google",
  "display_name": "Google Workspace",
  "driver_version": "0.1.0",
  "capabilities": ["mail", "calendar", "drive", "contacts", "tasks"],
  "auth_modes": ["oauth2"],
  "status": "experimental"
}
```

Required fields:

```text
provider          stable provider id
display_name      user-facing provider name
driver_version    semver driver version
capabilities      supported Aluminum resources
auth_modes         supported auth mechanisms
status            experimental | beta | stable | deprecated
```

---

## 4. Core Interface

Reference Rust-like trait:

```rust
#[async_trait]
pub trait ProviderDriver: Send + Sync {
    fn descriptor(&self) -> ProviderDescriptor;

    async fn auth_status(&self) -> Result<AuthStatus, DriverError>;

    async fn execute(
        &self,
        operation: NormalizedOperation,
        context: ExecutionContext,
    ) -> Result<NormalizedEnvelope, DriverError>;

    fn list_resources(&self) -> Vec<ResourceDescriptor>;
}
```

Language-specific implementations may differ, but the contract must remain equivalent.

---

## 5. Normalized Operation

Every command becomes a normalized operation before reaching a driver.

```json
{
  "operation_id": "op_01HT...",
  "resource": "mail",
  "method": "list",
  "provider": "google",
  "params": {
    "limit": 10,
    "query": "is:unread"
  },
  "body": null,
  "safety": {
    "write": false,
    "confirmed": false,
    "dry_run": false
  }
}
```

Required fields:

```text
operation_id   stable request id
resource       mail | calendar | drive | contacts | tasks | notes | search | sync
method         list | get | create | update | delete | search | send
provider       target provider id
params         query/path parameters
body           write payload when applicable
safety         write/dry-run/confirmation state
```

---

## 6. Execution Context

The execution context carries policy, audit, auth, and runtime information.

```json
{
  "actor": "local-user",
  "agent": null,
  "timestamp": "2026-04-25T00:00:00Z",
  "request_id": "req_01HT...",
  "audit_log": "./alum-audit.ndjson",
  "policy_mode": "warn",
  "auth_profile": "default"
}
```

Fields:

```text
actor          human or system actor
agent          invoking agent id if applicable
timestamp      operation time
request_id     audit correlation id
audit_log      optional audit destination
policy_mode    off | warn | enforce
auth_profile   credential profile name
```

---

## 7. Normalized Envelope

Drivers return a normalized envelope.

```json
{
  "ok": true,
  "command": "mail.list",
  "provider": "google",
  "request_id": "req_01HT...",
  "data": [],
  "audit": {
    "timestamp": "2026-04-25T00:00:00Z",
    "actor": "local-user",
    "operation": "mail.list",
    "provider": "google",
    "write": false,
    "confirmed": false,
    "dry_run": false,
    "route": "uws gmail users messages list",
    "result": "ok"
  },
  "errors": []
}
```

Envelope rules:

- `ok` is true only when operation completed successfully.
- `data` must use Aluminum-normalized schemas.
- `raw` provider payloads may be included inside individual data items, but normalized fields must exist.
- `errors` must be an array even on success.

---

## 8. Resource Contracts

### 8.1 Mail

Methods:

```text
list
get
send
search
```

Mail message schema:

```json
{
  "id": "provider-message-id",
  "provider": "google",
  "thread_id": "provider-thread-id",
  "subject": "Subject line",
  "from": {"name": "Alice Example", "email": "alice@example.com"},
  "to": [{"name": "Dave", "email": "dave@example.com"}],
  "cc": [],
  "bcc": [],
  "received_at": "2026-04-25T00:00:00Z",
  "sent_at": null,
  "snippet": "Preview text",
  "body_text": null,
  "body_html": null,
  "unread": true,
  "has_attachments": false,
  "attachments": [],
  "raw": {}
}
```

Send body:

```json
{
  "to": [{"email": "alice@example.com", "name": null}],
  "cc": [],
  "bcc": [],
  "subject": "Hello",
  "body_text": "Message body",
  "body_html": null,
  "attachments": []
}
```

### 8.2 Calendar

Methods:

```text
list
get
create
update
delete
search
```

Event schema:

```json
{
  "id": "provider-event-id",
  "provider": "microsoft",
  "title": "Team sync",
  "description": null,
  "start": "2026-04-25T15:00:00Z",
  "end": "2026-04-25T16:00:00Z",
  "timezone": "UTC",
  "location": null,
  "attendees": [
    {"name": "Alice Example", "email": "alice@example.com", "status": "needsAction"}
  ],
  "meeting_url": null,
  "recurrence": null,
  "raw": {}
}
```

Create body:

```json
{
  "title": "Team sync",
  "description": null,
  "start": "2026-04-25T15:00:00Z",
  "end": "2026-04-25T16:00:00Z",
  "timezone": "UTC",
  "location": null,
  "attendees": [{"email": "alice@example.com", "name": null}],
  "meeting_url_requested": false
}
```

### 8.3 Drive

Methods:

```text
list
get
search
create_folder
upload
delete
```

Drive item schema:

```json
{
  "id": "provider-file-id",
  "provider": "google",
  "name": "Q1 Budget.xlsx",
  "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "kind": "file",
  "web_url": "https://...",
  "download_url": null,
  "created_at": "2026-04-25T00:00:00Z",
  "updated_at": "2026-04-25T00:00:00Z",
  "owner": {"name": "Dave", "email": "dave@example.com"},
  "parents": [],
  "raw": {}
}
```

### 8.4 Contacts

Methods:

```text
list
get
search
create
update
delete
```

Contact schema:

```json
{
  "id": "provider-contact-id",
  "provider": "google",
  "display_name": "Alice Example",
  "emails": [{"email": "alice@example.com", "type": "work"}],
  "phones": [],
  "organization": null,
  "raw": {}
}
```

### 8.5 Tasks

Methods:

```text
list
get
create
update
delete
```

Task schema:

```json
{
  "id": "provider-task-id",
  "provider": "microsoft",
  "title": "Follow up",
  "notes": null,
  "status": "needsAction",
  "due": null,
  "completed_at": null,
  "raw": {}
}
```

---

## 9. Error Contract

Drivers must convert provider errors into Aluminum driver errors.

```json
{
  "code": "AUTH_REQUIRED",
  "message": "Google authentication required",
  "provider_code": "401",
  "retryable": false,
  "details": {}
}
```

Standard error codes:

```text
AUTH_REQUIRED
AUTH_EXPIRED
PERMISSION_DENIED
PROVIDER_UNAVAILABLE
UNSUPPORTED_PROVIDER
UNSUPPORTED_RESOURCE
UNSUPPORTED_METHOD
INVALID_ARGUMENT
CONFIRMATION_REQUIRED
POLICY_DENIED
DRY_RUN_ONLY
PROVIDER_ERROR
NORMALIZATION_ERROR
RATE_LIMITED
TIMEOUT
UNKNOWN_ERROR
```

---

## 10. Safety Contract

Drivers must not execute writes unless the normalized operation permits it.

Write methods include:

```text
mail.send
calendar.create
calendar.update
calendar.delete
drive.upload
drive.create_folder
drive.delete
contacts.create
contacts.update
contacts.delete
tasks.create
tasks.update
tasks.delete
```

If `safety.write == true` and neither `confirmed` nor `dry_run` is true, return:

```json
{
  "code": "CONFIRMATION_REQUIRED",
  "message": "Write operation requires confirmation or dry-run",
  "retryable": false
}
```

Dry-run must never call the provider write endpoint.

---

## 11. Audit Contract

Every driver operation must emit an audit record.

Minimum fields:

```json
{
  "timestamp": "2026-04-25T00:00:00Z",
  "request_id": "req_01HT...",
  "operation_id": "op_01HT...",
  "actor": "local-user",
  "agent": null,
  "resource": "mail",
  "method": "list",
  "provider": "google",
  "write": false,
  "confirmed": false,
  "dry_run": false,
  "route": "uws gmail users messages list",
  "result": "ok"
}
```

Audit records should be append-only NDJSON in MVP.

---

## 12. Auth Contract

MVP auth can delegate to `uws`.

Driver auth status:

```json
{
  "provider": "google",
  "authenticated": true,
  "account": "user@example.com",
  "expires_at": "2026-04-25T01:00:00Z",
  "scopes": ["mail.read", "calendar.read", "drive.read"]
}
```

Auth errors should never dump secrets, tokens, refresh tokens, or full credential paths.

---

## 13. Provider Mapping: MVP

### Google

```text
mail      Gmail API / uws gmail
calendar  Google Calendar API / uws calendar
drive     Google Drive API / uws drive
contacts  People API / uws people
tasks     Google Tasks API / uws tasks
```

### Microsoft

```text
mail      Microsoft Graph messages / uws ms-mail
calendar  Microsoft Graph calendar / uws ms-calendar
drive     OneDrive / uws ms-onedrive
contacts  Outlook contacts / uws ms-contacts
tasks     Microsoft To Do / uws ms-todo
```

---

## 14. Acceptance Criteria

This interface is accepted when:

- `alum` can route at least mail/calendar/drive reads through both Google and Microsoft drivers;
- all results use normalized schemas;
- write operations enforce confirmation;
- dry-run never performs provider writes;
- audit records are emitted;
- the same resource/method model can be implemented by Manus, Claude, GPT, or a human without additional context.

---

## 15. Implementation Order

1. Implement normalized operation struct.
2. Implement normalized envelope struct.
3. Implement error model.
4. Implement audit emitter.
5. Implement Google read routes.
6. Implement Microsoft read routes.
7. Implement dry-run write payloads.
8. Implement confirmed writes.
9. Add tests with mocked provider output.

---

## 16. Working Doctrine

Drivers are adapters, not product surfaces.

Users and agents should think in Aluminum resources. Providers should be implementation details.
# AGENTS.md — AI Agent Integration Guide

`uws` is designed from the ground up to be the **universal tool layer for AI agents**. Every response is structured JSON. Every command is deterministic and composable. Every ecosystem is accessible through the same grammar.

This document covers integration with Claude, Manus, Gemini, and Microsoft Copilot, followed by the original developer notes for contributors.

---

## Design Principles for AI Agent Use

1. **Always use `--dry-run` before write operations.** Confirm the request shape before executing.
2. **Always use `--format json`** (the default) for machine-readable output.
3. **Use `--params` for query/URL parameters** and `--json` for request bodies.
4. **Use `--page-all` to retrieve complete datasets** when you need all results, not just the first page.
5. **Check `uws auth status` and `uws ms-auth status`** before attempting API calls to confirm authentication.

---

## Claude (Anthropic)

### Tool Definition

```json
{
  "name": "uws",
  "description": "Universal Workspace CLI. Provides read and write access to Google Workspace (Gmail, Drive, Calendar, Docs, Sheets, Slides, Tasks, Chat, Keep, Meet), Microsoft 365 (Outlook Mail, OneDrive, Teams, To Do, OneNote, SharePoint), Apple iCloud (Calendar, Contacts, Drive, Notes, Reminders), Android (device management, Messages), and Chrome (policy, management, extensions). All output is JSON. Use --dry-run before any write operation.",
  "input_schema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "Full uws command string excluding the 'uws' binary name. Examples: 'gmail users messages list --params {\"userId\":\"me\",\"maxResults\":10}', 'ms-mail messages list --params {\"$top\":5}', 'drive files list --format table'"
      }
    },
    "required": ["command"]
  }
}
```

### System Prompt Addition

```
You have access to the `uws` tool which gives you read and write access to the user's
Google Workspace, Microsoft 365, Apple iCloud, Android, and Chrome accounts.

Rules for using uws:
- Always use --dry-run first to preview write operations before executing them.
- Always confirm with the user before sending emails, creating calendar events, or deleting files.
- Use --format json (default) for all calls; parse the JSON response to extract relevant data.
- Use --page-all when you need complete lists, not just the first page.
- If a command fails with an auth error, tell the user to run: uws auth status / uws ms-auth status
- Prefer --params for filtering (e.g. search queries, date ranges) to minimize response size.
```

---

## Manus

### Skill Installation

```bash
cp -r skills/uws-core ~/.manus/skills/
cp -r skills/ms-outlook ~/.manus/skills/
cp -r skills/ms-onedrive ~/.manus/skills/
cp -r skills/ms-teams ~/.manus/skills/
cp -r skills/apple-calendar ~/.manus/skills/
cp -r skills/apple-contacts ~/.manus/skills/
```

Or symlink to stay in sync with the repo:

```bash
ln -s $(pwd)/skills/uws-* ~/.manus/skills/
```

### Manus Invocation Pattern

```bash
# Read operation
uws <service> <resource> <method> --params '<json>' --format json

# Write operation — always dry-run first
uws <service> <resource> <method> --params '<json>' --json '<body>' --dry-run
uws <service> <resource> <method> --params '<json>' --json '<body>'
```

---

## Gemini (Google AI Studio)

### Python Function Tool

```python
import subprocess, json, os

def uws(command: str) -> dict:
    """Execute a uws Universal Workspace CLI command."""
    result = subprocess.run(
        ["uws"] + command.split(),
        capture_output=True, text=True, env={**os.environ}
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip(), "exit_code": result.returncode}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw_output": result.stdout.strip()}
```

### Gemini Extension

```bash
gemini extensions install https://github.com/splitmerge420/uws
```

---

## Microsoft Copilot

### System Prompt

```
You have access to the uws Universal Workspace CLI tool. Use it to read and manage
emails across Gmail and Outlook, create and manage calendar events across Google Calendar
and Outlook Calendar, list and manage files across Google Drive and OneDrive, manage tasks
across Google Tasks and Microsoft To Do, access Teams channels and messages, and read and
manage iCloud Calendar and Contacts.

Always use --dry-run before write operations. Always confirm with the user before
sending emails or deleting data. Parse JSON responses to extract relevant information.
```

---

## The Aluminum Agent Runtime

The `alum ai` command (Phase 4) provides a unified natural language interface:

```bash
alum ai "summarize my unread emails"
alum ai "what meetings do I have tomorrow?"
alum ai "find all files related to the uws project"
alum ai "create a task to review the Q1 report by Friday"
```

Configure the AI backend:

```bash
export ANTHROPIC_API_KEY=sk-ant-...    # Use Claude
export GEMINI_API_KEY=AIza...           # Use Gemini
export OPENAI_API_KEY=sk-...            # Use GPT
```

---

## Security Notes

- All credentials are stored encrypted (AES-256-GCM) in `~/.config/uws/`
- Use `--dry-run` before any destructive operation
- The Model Armor integration (`--sanitize`) scans responses for prompt injection
- Never pass raw API responses directly to an LLM without sanitization in production

---

---

# Developer Notes (Original gws Architecture)

The following section preserves the original `gws` developer documentation for contributors building on the core Rust architecture.

## Project Overview

`uws` is built on the `gws` Rust CLI core, which dynamically generates its command surface at runtime by parsing Google Discovery Service JSON documents.

> **Dynamic Discovery**: This project does NOT use generated Rust crates (e.g., `google-drive3`) for API interaction. It fetches the Discovery JSON at runtime and builds `clap` commands dynamically. When adding a new Google service, only register it in `src/services.rs`. Do NOT add new crates to `Cargo.toml` for standard Google APIs.

> **Package Manager**: Use `pnpm` instead of `npm` for Node.js package management.

## Build & Test

```bash
cargo build                       # dev build
cargo clippy -- -D warnings       # lint
cargo test                        # unit tests
./scripts/coverage.sh             # HTML coverage report
```

## Architecture

The CLI uses a **two-phase argument parsing** strategy:

1. Parse argv to extract the service name (e.g., `drive`)
2. Fetch the service's Discovery Document, build a dynamic `clap::Command` tree, then re-parse

### Source Layout

| File | Purpose |
|---|---|
| `src/main.rs` | Entrypoint, two-phase CLI parsing, method resolution |
| `src/discovery.rs` | Serde models for Discovery Document + fetch/cache |
| `src/services.rs` | Service alias → Discovery API name/version mapping |
| `src/auth.rs` | OAuth2 token acquisition via env vars, encrypted credentials, or ADC |
| `src/credential_store.rs` | AES-256-GCM encryption/decryption of credential files |
| `src/auth_commands.rs` | `uws auth` subcommands: login, logout, setup, status, export |
| `src/commands.rs` | Recursive `clap::Command` builder from Discovery resources |
| `src/executor.rs` | HTTP request construction, response handling, schema validation |
| `src/ms_graph.rs` | Microsoft Graph API integration module |
| `src/apple.rs` | Apple CalDAV/CardDAV/CloudKit integration module |
| `src/android_chrome.rs` | Android Management API and Chrome Policy integration module |
| `src/schema.rs` | `uws schema` command — introspect API method schemas |
| `src/error.rs` | Structured JSON error output |

## Input Validation & URL Safety

This CLI is frequently invoked by AI/LLM agents. Always assume inputs can be adversarial — validate paths against traversal (`../../.ssh`), restrict format strings to allowlists, reject control characters, and encode user values before embedding them in URLs.

### Path Safety (`src/validate.rs`)

| Scenario | Validator | Rejects |
|---|---|---|
| File path for writing (`--output-dir`) | `validate::validate_safe_output_dir()` | Absolute paths, `../` traversal, symlinks outside CWD, control chars |
| File path for reading (`--dir`) | `validate::validate_safe_dir_path()` | Absolute paths, `../` traversal, symlinks outside CWD, control chars |
| Enum/allowlist values | clap `value_parser` | Any value not in the allowlist |

### URL Encoding (`src/helpers/mod.rs`)

```rust
// CORRECT — encodes slashes, spaces, and special characters
let url = format!(
    "https://www.googleapis.com/drive/v3/files/{}",
    crate::helpers::encode_path_segment(file_id),
);
```

## Environment Variables

### Google Authentication

| Variable | Description |
|---|---|
| `GOOGLE_WORKSPACE_CLI_TOKEN` | Pre-obtained OAuth2 access token (highest priority) |
| `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | Path to OAuth credentials JSON |
| `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` | Override config directory (default: `~/.config/uws`) |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_TEMPLATE` | Default Model Armor template |
| `GOOGLE_WORKSPACE_CLI_SANITIZE_MODE` | `warn` (default) or `block` |

### Microsoft Authentication

| Variable | Description |
|---|---|
| `UWS_MS_CLIENT_ID` | Azure app client ID |
| `UWS_MS_CLIENT_SECRET` | Azure app client secret |
| `UWS_MS_TENANT_ID` | Azure AD tenant ID |
| `UWS_MS_TOKEN` | Pre-obtained Microsoft Graph token |

### Apple Authentication

| Variable | Description |
|---|---|
| `UWS_APPLE_ID` | Apple ID email |
| `UWS_APPLE_APP_PASSWORD` | App-specific password |
| `UWS_APPLE_CLIENT_ID` | Sign in with Apple client ID |
| `UWS_APPLE_TEAM_ID` | Apple Developer team ID |
| `UWS_APPLE_KEY_ID` | Apple private key ID |
| `UWS_APPLE_PRIVATE_KEY_FILE` | Path to Apple .p8 private key |

### AI Agents

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key |
| `GEMINI_API_KEY` | Gemini API key |
| `OPENAI_API_KEY` | OpenAI/GPT API key |

---

*See [README.md](README.md) for installation and full command reference.*
*See [ALUMINUM.md](ALUMINUM.md) for the full Aluminum OS architecture specification.*

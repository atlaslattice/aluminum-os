# CLAUDE.md — Claude Integration Guide

When contributing to this repository, follow all guidelines in [AGENTS.md](AGENTS.md).

This file provides Claude (Anthropic) with everything it needs to use `uws` effectively as a tool and to contribute to the codebase.

---

## What uws Does

`uws` is the Universal Workspace CLI. It gives Claude structured, JSON-first access to:

- **Google Workspace**: Gmail, Drive, Calendar, Docs, Sheets, Slides, Tasks, People, Chat, Forms, Keep, Meet
- **Microsoft 365**: Outlook Mail, Outlook Calendar, OneDrive, Teams, To Do, OneNote, SharePoint, Planner
- **Apple iCloud**: Calendar (CalDAV), Contacts (CardDAV), Drive (CloudKit), Notes, Reminders
- **Android**: Device management, Messages (RCS)
- **Chrome**: Management, Policy, Web Store, ChromeOS devices

All output is clean JSON. All commands follow the same grammar.

---

## Command Grammar

```
uws <service> <resource> [sub-resource] <method> [flags]
```

### Universal Flags

| Flag | Description |
|---|---|
| `--params <JSON>` | URL/query parameters |
| `--json <JSON>` | Request body (POST/PATCH/PUT) |
| `--upload <PATH>` | Upload a local file |
| `--output <PATH>` | Save binary response to file |
| `--format json\|table\|yaml\|csv` | Output format (default: json) |
| `--page-all` | Auto-paginate all results |
| `--dry-run` | Preview request without executing |

---

## Rules for Claude When Using uws

1. **Always `--dry-run` first** before any write, send, create, update, or delete operation.
2. **Always confirm with the user** before sending emails, creating calendar events, uploading files, or deleting anything.
3. **Use `--format json`** (the default) for all calls — parse the JSON to extract what you need.
4. **Use `--params` for filtering** to minimize response size (e.g., `$select`, `$filter`, `q`).
5. **Use `--page-all` sparingly** — only when you genuinely need all results.
6. **Check auth first** if a command fails: `uws auth status` (Google) or `uws ms-auth status` (Microsoft).

---

## Quick Reference: Most Common Commands

### Email

```bash
# Gmail — list unread
uws gmail users messages list --params '{"userId":"me","q":"is:unread","maxResults":10}'

# Outlook — list unread
uws ms-mail messages list --params '{"$top":10,"$filter":"isRead eq false","$select":"subject,from,receivedDateTime,bodyPreview"}'

# Outlook — send (dry-run first!)
uws ms-mail messages send --json '{
  "message": {
    "subject": "Hello",
    "body": {"contentType": "Text", "content": "Message body"},
    "toRecipients": [{"emailAddress": {"address": "recipient@example.com"}}]
  }
}' --dry-run
```

### Calendar

```bash
# Google Calendar — list today's events
uws calendar events list --params '{"calendarId":"primary","timeMin":"2026-03-08T00:00:00Z","singleEvents":true,"orderBy":"startTime"}'

# Google Calendar — create event (dry-run first!)
uws calendar events insert --params '{"calendarId":"primary"}' \
  --json '{"summary":"Meeting","start":{"dateTime":"2026-03-10T10:00:00Z"},"end":{"dateTime":"2026-03-10T11:00:00Z"}}' \
  --dry-run

# Outlook Calendar — list events
uws ms-calendar events list --params '{"$top":10,"$select":"subject,start,end,organizer"}'
```

### Files

```bash
# Google Drive — list files
uws drive files list --params '{"pageSize":10,"fields":"files(id,name,mimeType,modifiedTime)"}' --format table

# OneDrive — list root
uws ms-onedrive drive root children list --params '{"$select":"name,size,lastModifiedDateTime"}'

# OneDrive — search
uws ms-onedrive drive root search --params '{"q":"budget"}'
```

### Tasks

```bash
# Google Tasks — list
uws tasks tasks list --params '{"tasklist":"@default","showCompleted":false}'

# Microsoft To Do — create task (dry-run first!)
uws ms-todo tasks create --json '{"title":"Review PR","importance":"high"}' --dry-run
```

---

## Authentication Setup

### Google
```bash
uws auth setup    # First time: creates OAuth credentials
uws auth login    # Subsequent logins
uws auth status   # Check current state
```

### Microsoft
```bash
export UWS_MS_CLIENT_ID=<azure-app-client-id>
export UWS_MS_CLIENT_SECRET=<azure-app-client-secret>
export UWS_MS_TENANT_ID=common
uws ms-auth setup && uws ms-auth login
```

### Apple
```bash
export UWS_APPLE_ID=your@icloud.com
export UWS_APPLE_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
uws apple-auth setup
```

---

## Contributing to uws

### Architecture

`uws` uses a **two-phase parsing** strategy:

1. Read `argv[1]` to identify the service (e.g., `drive`, `ms-mail`, `apple-calendar`)
2. For Google services: fetch the Discovery Document (cached 24h) and build a dynamic `clap::Command` tree
3. For Microsoft services: route to `src/ms_graph.rs`
4. For Apple services: route to `src/apple.rs`
5. For Android/Chrome: route to `src/android_chrome.rs`
6. Re-parse remaining arguments, authenticate, build HTTP request, execute

### Adding a New Provider

Implement the `ProviderDriver` trait (see [ALUMINUM.md](ALUMINUM.md)) and register in `src/services.rs`.

### Code Quality

- All new code must have unit tests
- Use `cargo clippy -- -D warnings` before committing
- Validate all user-supplied path inputs with `validate::validate_safe_output_dir()`
- Encode all URL path segments with `helpers::encode_path_segment()`
- Every PR needs a changeset at `.changeset/<name>.md`

---

## The Aluminum OS Vision

`uws` is Phase 1 of Aluminum OS — a provider-agnostic command surface for all productivity ecosystems.

Read the full architecture: **[ALUMINUM.md](ALUMINUM.md)**

*See [README.md](README.md) for installation. See [AGENTS.md](AGENTS.md) for multi-agent patterns.*

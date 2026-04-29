# Aluminum OS — Architecture Specification

> *"You're not building three CLIs. You're building one CLI with three backends."*
> — Microsoft Copilot, reviewing the uws project, March 2026

---

## What Is Aluminum?

**Aluminum** is the governance substrate and agent runtime that sits beneath `uws`.

Where `uws` is the **command surface** — the thing humans and AI agents type — Aluminum is the **kernel** that makes it coherent: a single identity layer, a single memory substrate, a single reasoning layer, and a single plugin model that turns Google, Microsoft, and Apple from competing silos into interchangeable **drivers**.

This is the same architectural pattern that Kubernetes uses to abstract cloud providers. Aluminum does the same for productivity ecosystems.

```
┌─────────────────────────────────────────────────────────────┐
│                    Human / AI Agent                         │
│              (Claude, Manus, Gemini, Copilot)               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    uws command surface
                    alum <verb> <resource> [--provider]
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   ALUMINUM KERNEL                           │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Identity   │  │    Memory    │  │  Agent Runtime    │  │
│  │  Substrate  │  │  Substrate   │  │  (Claude/Manus/   │  │
│  │  (one user, │  │  (one graph, │  │   Gemini/Copilot) │  │
│  │  all clouds)│  │  all data)   │  │                   │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Governance │  │  Continuity  │  │  Plugin Host      │  │
│  │  Layer      │  │  Layer       │  │  (replaces 500+   │  │
│  │  (policies, │  │  (cross-     │  │   siloed apps)    │  │
│  │   consent)  │  │   session)   │  │                   │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼────┐     ┌──────▼─────┐
    │ Google  │      │Microsoft │     │   Apple    │
    │ Driver  │      │  Driver  │     │   Driver   │
    │         │      │          │     │            │
    │ Drive   │      │ OneDrive │     │iCloud Drive│
    │ Gmail   │      │ Outlook  │     │ iCloud Mail│
    │ Calendar│      │ Calendar │     │ iCalendar  │
    │ Docs    │      │ Teams    │     │ Contacts   │
    │ Sheets  │      │ OneNote  │     │ Notes      │
    │ Meet    │      │ To Do    │     │ Reminders  │
    │ Keep    │      │SharePoint│     │ Keychain   │
    │ Chat    │      │ Planner  │     │ App Intents│
    └─────────┘      └──────────┘     └────────────┘
         │                 │                 │
    ┌────▼────┐      ┌─────▼────┐
    │ Android │      │  Chrome  │
    │ Driver  │      │  Driver  │
    │         │      │          │
    │Messages │      │Bookmarks │
    │Files    │      │History   │
    │Devices  │      │Extensions│
    └─────────┘      └──────────┘
```

---

## The `alum` Command Grammar

Copilot's proposed command surface, now formalized:

```
alum <verb> <resource> [--provider google|microsoft|apple|android|chrome] [flags]
```

### Examples

```bash
# Send email — provider auto-detected from context, or specified
alum mail send --to "alice@example.com" --subject "Hello" --body "From uws"
alum mail send --to "alice@example.com" --provider microsoft

# List files — works across all providers
alum drive list
alum drive list --provider microsoft
alum drive list --provider apple

# Create a calendar event — same syntax, any backend
alum calendar create --ai "schedule a 1-hour team sync tomorrow at 10am"
alum calendar create --provider apple --ai "block Friday afternoon for deep work"

# Generate a document — AI-assisted, any provider
alum doc generate --provider google --ai "draft a project charter for uws"
alum doc generate --provider microsoft --ai "create a weekly status report template"

# Search across ALL providers simultaneously
alum search "Q1 budget" --provider all

# Cross-provider sync
alum sync calendar --from google --to microsoft
alum sync contacts --from apple --to google

# AI-native commands (no provider needed — Aluminum decides)
alum ai "summarize my unread emails"
alum ai "what meetings do I have tomorrow?"
alum ai "find all files related to the uws project"
```

---

## The Five Build Phases (Copilot's Roadmap)

### Phase 1 — Fork Google CLI → Abstract Provider Layer *(Current: uws v0.1)*

The `uws` fork establishes the pattern:
- Working reference implementation from `gws`
- Clear command grammar
- Auth model (OAuth2 per provider)
- JSON-first output for AI agents
- SKILL.md files for Claude, Manus, Gemini

**Deliverable:** `uws` — the multi-ecosystem CLI. **Status: In progress.**

### Phase 2 — Microsoft Graph Backend *(uws v0.2)*

- Full Microsoft Graph API integration
- `ms-mail`, `ms-calendar`, `ms-onedrive`, `ms-teams`, `ms-todo`, `ms-onenote`
- Microsoft OAuth2 / Azure AD auth flow
- Copilot integration via Graph AI endpoints

**Deliverable:** `uws ms-*` commands fully operational.

### Phase 3 — Apple Intents Backend *(uws v0.3)*

- CalDAV / CardDAV for Calendar, Contacts, Reminders
- CloudKit for Drive and Notes
- Sign in with Apple OAuth2
- Apple Shortcuts / App Intents bridge (macOS/iOS)

**Deliverable:** `uws apple-*` commands fully operational.

### Phase 4 — Bind to Aluminum Kernel APIs *(alum v0.1)*

- Introduce the `alum` command surface as an alias/wrapper over `uws`
- Implement the **provider abstraction layer** — `--provider` flag routes to the correct backend
- Implement the **identity substrate** — one login, all providers
- Implement the **memory substrate** — cross-session context, cross-provider search
- Implement the **agent runtime** — `alum ai "<prompt>"` dispatches to Claude/Manus/Gemini

**Deliverable:** `alum` binary. Provider-agnostic commands working.

### Phase 5 — Replace All Three with Aluminum-Native Commands *(alum v1.0)*

- `alum mail`, `alum drive`, `alum calendar`, `alum doc`, `alum task` — fully provider-agnostic
- Governance layer: consent management, data residency policies, audit logs
- Continuity layer: cross-session memory, cross-device state
- Plugin host: third-party providers (Notion, Slack, Linear, etc.) via plugin API
- The three ecosystem CLIs become internal "drivers," not user-facing tools

**Deliverable:** Aluminum OS command surface. The world's first AI-native OS layer.

---

## The Provider Abstraction Layer

The core of Aluminum's power is the **provider abstraction**. Every resource type maps to a normalized interface:

| Resource | Google Driver | Microsoft Driver | Apple Driver |
|---|---|---|---|
| `mail` | Gmail API v1 | Graph `/me/messages` | iCloud Mail (IMAP) |
| `calendar` | Calendar API v3 | Graph `/me/calendar` | CalDAV |
| `drive` | Drive API v3 | Graph `/me/drive` | CloudKit |
| `contacts` | People API v1 | Graph `/me/contacts` | CardDAV |
| `tasks` | Tasks API v1 | Graph `/me/todo/lists` | Reminders (CalDAV VTODO) |
| `notes` | Keep API v1 | Graph `/me/onenote` | CloudKit Notes |
| `chat` | Chat API v1 | Graph `/me/chats` | iMessage (local bridge) |
| `doc` | Docs API v1 | Graph `/me/drive` (DOCX) | Pages (iCloud) |

Each driver normalizes responses into a **common Aluminum schema** — so `alum mail list` always returns the same JSON shape regardless of provider.

---

## The Identity Substrate

Aluminum maintains a **single identity graph** that maps:

```
User (Daavud)
  ├── Google Account: therealdavesheldon@gmail.com
  ├── Microsoft Account: dave@outlook.com
  ├── Apple ID: dave@icloud.com
  └── Devices
        ├── Pixel 9 (Android)
        ├── Pixel Watch
        ├── iPhone 16
        ├── Chromebook
        └── MacBook Pro
```

Auth tokens for each provider are stored in the Aluminum keychain (`~/.config/uws/keychain.enc`) using the same AES-GCM encryption as the original `gws` credential store.

---

## The Agent Runtime

Aluminum's agent runtime is the bridge between the command surface and AI models:

```
alum ai "summarize my unread emails"
        │
        ▼
  Aluminum Agent Runtime
        │
        ├── Calls: uws gmail users messages list --params '{"q":"is:unread"}'
        ├── Calls: uws ms-mail messages list --params '{"$filter":"isRead eq false"}'
        │
        ▼
  Aggregates results → sends to Claude/Manus/Gemini
        │
        ▼
  Returns: natural language summary
```

Supported AI backends:
- **Claude** (Anthropic) — `ANTHROPIC_API_KEY`
- **Manus** — native integration via SKILL.md
- **Gemini** (Google) — `GEMINI_API_KEY`
- **Copilot** (Microsoft) — via Graph AI endpoints
- **GPT** (OpenAI) — `OPENAI_API_KEY`

---

## The Governance Layer

Every action in Aluminum passes through the governance layer:

```rust
pub struct GovernanceConfig {
    /// Require explicit confirmation for write operations
    pub require_confirm_writes: bool,
    /// Audit log path
    pub audit_log: Option<PathBuf>,
    /// Data residency: which providers are allowed for which data types
    pub data_residency: HashMap<ResourceType, Vec<Provider>>,
    /// Content safety: Model Armor template (inherited from gws)
    pub sanitize_template: Option<String>,
}
```

This is the **Aluminum governance substrate** — the layer that ensures AI agents operating on behalf of users do so safely, with full auditability.

---

## Why This Is the AI-Native OS

Traditional operating systems abstract hardware. Aluminum abstracts **productivity ecosystems**.

Just as Linux kernel drivers let you write `read()` and `write()` without caring whether the storage is NVMe, SATA, or NFS — Aluminum lets you write `alum drive list` without caring whether the files are in Google Drive, OneDrive, or iCloud.

The AI agent (Claude, Manus, Gemini) becomes the **shell** of this OS. The user's intent is the **program**. The provider drivers are the **device drivers**. And Aluminum is the **kernel**.

This is the architecture that makes the AI-native OS real.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new provider driver.

The minimal interface a provider driver must implement:

```rust
pub trait ProviderDriver: Send + Sync {
    fn name(&self) -> &str;
    async fn authenticate(&self) -> Result<String>;  // returns token
    async fn execute(&self, resource: &str, method: &str, params: Option<&str>, body: Option<&str>, token: &str) -> Result<serde_json::Value>;
    fn list_resources(&self) -> Vec<ResourceDescriptor>;
}
```

---

## References

- [uws GitHub Repository](https://github.com/splitmerge420/uws)
- [Original gws project](https://github.com/googleworkspace/cli) by Justin Poehnelt / Google
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/overview)
- [Apple CalDAV / CardDAV](https://developer.apple.com/documentation/devicemanagement)
- [Kubernetes Provider Abstraction Pattern](https://kubernetes.io/docs/concepts/architecture/)
- Architectural review: Microsoft Copilot, March 2026

---

> Aluminum is an independent open-source project. Not affiliated with Google, Microsoft, or Apple.
> Built by Daavud Sheldon and the open-source community.

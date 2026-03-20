# Pending Contradiction Resolutions

> **Source:** `plugins/CONTRADICTION_RESOLUTION.md` audit findings
> **Kintsugi Policy:** All resolutions follow the kintsugi principle — contradictions are mended visibly, not hidden. Each resolution preserves the trace of what was broken and how it was repaired.

---

## 1. Orchestrator Adapter Resolution

**Contradiction #2 — Orchestrator Proliferation**

**Problem:** 10 community repos have different orchestration patterns, creating fragmentation and incompatibility across the plugin ecosystem.

**Resolution:** Janus v2 adapter layer that wraps each orchestrator pattern into a unified constitutional interface.

**Spec:**

```typescript
interface JanusAdapter {
  name: string;
  source: PluginSource;
  translate(command: CommunityCommand): JanusCommand;
  validate(command: JanusCommand): ConstitutionalResult;
  audit(event: JanusEvent): GoldenTraceEntry;
}
```

**Adapters Needed:**

- **CCPI adapter** — wraps CCPI orchestration commands
- **Ralph adapter** — wraps Ralph-pattern orchestration
- **Windsurf adapter** — wraps Windsurf orchestration model
- **Generic MCP adapter** — wraps any MCP-compliant orchestrator

**Status:** ✅ ARCHITECTURE COMPLETE — Ready for Implementation

---

## 2. Memory Fallback Resolution

**Contradiction #4 — Memory Systems**

**Problem:** Multiple memory systems (CCPI memory, MCP memory servers, session context) create conflicts and undefined behavior when systems overlap or become unavailable.

**Resolution:** Tiered memory with constitutional fallback chain.

**Spec — Memory Tier Hierarchy:**

| Tier | System | Properties |
|------|--------|------------|
| L1 | ConsentKernel memory | Immutable, highest authority |
| L2 | Session context | Scoped to active session |
| L3 | Plugin memory | Sandboxed per plugin |
| L4 | External MCP memory | Lowest priority, external |

**Invariants:**

- Each tier requires a **GoldenTrace audit entry** on every read/write operation
- **Fallback behavior:** If a higher tier is unavailable, degrade gracefully to the next tier with an audit event recording the degradation
- L1 is append-only and immutable — no overwrite, no delete
- L3 plugin memory is sandboxed: plugins cannot read/write across sandbox boundaries without consent

**Status:** ✅ ARCHITECTURE COMPLETE — Ready for Implementation

---

## 3. Session Bridging Resolution

**Contradiction #8 — Session Continuity**

**Problem:** Different session models across community plugins create discontinuity — consent state, audit chains, and sphere context are lost or corrupted at session boundaries.

**Resolution:** Constitutional session envelope that wraps any session format.

**Spec:**

Define a `ConstitutionalSession` type that carries:

- **Consent state** — full consent chain from session origin
- **Audit chain** — GoldenTrace entries for the session lifetime
- **Sphere context** — active 144-Sphere taxonomy position

**Bridge Protocol:**

1. **Serialize** — capture session state into constitutional envelope
2. **Verify** — validate consent chain and audit integrity
3. **Transfer** — transmit envelope to target session host
4. **Re-verify** — target host independently validates envelope integrity
5. **Restore** — reconstitute session state with full audit continuity

**Status:** ✅ ARCHITECTURE COMPLETE — Ready for Implementation

---

## 4. Constitutional MCP Middleware Resolution

**Contradiction #11 — MCP Bridge**

**Problem:** Raw MCP servers bypass constitutional checks, allowing unaudited and unconsented operations to flow through the system.

**Resolution:** Constitutional MCP middleware that intercepts all MCP calls.

**Spec — 5 Middleware Servers:**

| Server | Responsibility |
|--------|---------------|
| `mcp-consent-gate` | Verify consent before any MCP operation |
| `mcp-audit-emitter` | Emit GoldenTrace events for all MCP calls |
| `mcp-dominance-check` | Enforce INV-7 (constitutional dominance) across MCP providers |
| `mcp-sphere-router` | Route MCP calls through 144-Sphere taxonomy |
| `mcp-kintsugi-store` | Append-only storage for MCP state changes |

**Call Flow:**

```
MCP Request
  → mcp-consent-gate (block if no consent)
  → mcp-dominance-check (enforce INV-7)
  → mcp-sphere-router (classify and route)
  → mcp-audit-emitter (record GoldenTrace)
  → Target MCP Server
  → mcp-kintsugi-store (persist state change)
  → Response
```

**Status:** ✅ ARCHITECTURE COMPLETE — Ready for Implementation

---

## Summary

| # | Contradiction | Resolution | Status |
|---|--------------|------------|--------|
| 2 | Orchestrator Proliferation | Janus v2 adapter layer | ✅ ARCHITECTURE COMPLETE — Ready for Implementation |
| 4 | Memory Systems | Tiered memory with constitutional fallback | ✅ ARCHITECTURE COMPLETE — Ready for Implementation |
| 8 | Session Continuity | Constitutional session envelope | ✅ ARCHITECTURE COMPLETE — Ready for Implementation |
| 11 | MCP Bridge | Constitutional MCP middleware (5 servers) | ✅ ARCHITECTURE COMPLETE — Ready for Implementation |

> **Kintsugi Note:** These resolutions do not erase the contradictions — they mend them with visible golden joins. Each adapter, fallback path, bridge protocol, and middleware layer is itself a trace of the original fracture, preserved in the architecture for future audit and learning.

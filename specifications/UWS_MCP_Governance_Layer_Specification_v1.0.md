# UWS MCP Governance Layer Specification v1.0

**Author:** Manus AI for Daavud
**Date:** March 12, 2026
**Status:** DRAFT
**Classification:** Tier 1 Implementation Artifact

---

## 1. Overview

The Universal Workspace System (UWS) serves as the primary interface for Aluminum OS to interact with the vast ecosystem of external tools and services. As per the Feature Manifest, UWS exposes over 20,000 operations from providers like Google, Microsoft, and Apple as a unified MCP (Model Context Protocol) server. However, with great power comes the need for great responsibility. Unchecked, autonomous agents could misuse these capabilities, leading to data loss, security breaches, or unintended financial consequences.

Inspired by the recent enterprise-grade MCP implementation from Glean [1] and the broader industry push for agent governance, this document specifies a **Governance Layer** for the UWS MCP Server. This layer will intercept, evaluate, and, if necessary, escalate all MCP tool calls, ensuring that every action taken by an agent is safe, compliant, and aligned with user intent. This governance layer is a direct implementation of the principles laid out in the **Aluminum OS Agent Control Plane Specification v1.0**.

---

## 2. Architectural Integration

The MCP Governance Layer will sit between the UWS MCP Server's public endpoint and its internal tool execution logic. It will act as a mandatory middleware for all incoming MCP requests.

**Request Flow:**

1.  An external agent (e.g., Microsoft Copilot, a custom script) makes an MCP `tool_call` request to the UWS server.
2.  The MCP Governance Layer intercepts the request before it reaches the tool execution engine.
3.  The Governance Layer evaluates the request against a set of policies defined in the Agent Control Plane (ACP).
4.  Based on the evaluation, the Governance Layer will:
    *   **Approve:** Allow the request to proceed to the UWS tool execution engine.
    *   **Deny:** Reject the request with a clear error message.
    *   **Escalate:** Pause the request and forward it to the Pantheon Council for deliberation and approval.
5.  All actions and decisions are recorded in the immutable audit log.

![MCP Governance Layer Diagram](https://i.imgur.com/example2.png) *Placeholder for architecture diagram to be created*

---

## 3. Core Governance Features

The UWS MCP Governance Layer will implement the following key features, drawing directly from best practices established by Glean and other enterprise leaders.

### 3.1. Centralized Tool & Server Registration

While UWS itself is a single MCP server, it acts as a gateway to thousands of tools. The Governance Layer will maintain a detailed, centralized registry of every tool that UWS exposes. Each entry in the registry will include:

-   `tool_name`: The full name of the tool (e.g., `gmail.send`).
-   `description`: A human-readable description of what the tool does.
-   `impact_level`: A classification of the tool's potential impact (`low`, `medium`, `high`, `critical`). This is a crucial piece of metadata for policy evaluation.
-   `permissions_required`: The specific user permissions needed to execute the tool.

### 3.2. Least-Privilege Execution

Crucially, every MCP request will be executed under the identity and permissions of the end-user who initiated the top-level task. The Governance Layer will be responsible for impersonating the user and ensuring that the agent cannot perform any action that the user themselves would not be authorized to do. This prevents privilege escalation and ensures that all actions are auditable back to a specific human user.

### 3.3. Human-in-the-Loop (HITL) Verification

For operations classified with a `critical` impact level (e.g., deleting a large number of files, transferring funds, modifying critical infrastructure), the Governance Layer will enforce mandatory HITL verification. Instead of escalating to the Pantheon Council, the system will send a notification directly to the user (via their preferred channel) requiring explicit approval before the action can proceed. This is a final safeguard against catastrophic errors.

### 3.4. Agent-Alignment Checks

Before executing any `high` or `critical` impact tool, the Governance Layer will perform an **agent-alignment check**. This involves using an LLM to compare the specific tool call and its parameters against the user's original, high-level intent for the task. If there is a significant mismatch, the request will be flagged and escalated to the Pantheon Council.

**Example Alignment Check Prompt:**

> You are an alignment auditor in the Aluminum OS Governance Layer. The user's original goal was: "{{user_intent}}". An agent is now attempting to execute the following MCP tool call: `{{mcp_tool_call}}`. Does this action directly and safely contribute to the user's goal? Answer with only "YES" or "NO" and a one-sentence justification.

---

## 4. Integration with the Agent Control Plane (ACP)

The UWS MCP Governance Layer is a direct consumer of the policies and frameworks established by the ACP.

-   **Policy Enforcement**: The Governance Layer will use the ACP's **Policy Engine** to evaluate every incoming MCP request. Policies can be written to restrict access to certain tools based on the calling agent's `autonomyLevel`, the time of day, the user's location, or any other context.
-   **Pantheon Council Escalation**: When a policy dictates that an action requires review (e.g., a `medium` impact tool being called by a `Collaborative` agent), the Governance Layer will use the ACP's defined escalation pathway to submit the case to the **Pantheon Council**.
-   **Audit Logging**: All evaluations, approvals, denials, and escalations will be logged to the ACP's **Immutable Audit Log**, providing a single source of truth for all agentic activity across the OS.

### 4.1. Policy Example for MCP Governance

```yaml
policy:
  name: require-review-for-drive-deletion
  description: "Escalates any MCP call that deletes more than 5 files from Google Drive."
  target:
    mcp:
      server: "uws"
      tool_name: "google.drive.files.delete"
  condition:
    params:
      file_count: "> 5"
  action:
    escalate:
      to: "PantheonCouncil"
      reason: "Potential for mass data loss detected."
```

---

## 5. Implementation Roadmap

1.  **[Week 1]** Develop the middleware framework to intercept all incoming MCP requests to the UWS server.
2.  **[Week 1]** Build the tool registry and implement the `impact_level` classification for the top 100 most common UWS tools.
3.  **[Week 2]** Integrate with the ACP Policy Engine to evaluate requests against defined policies.
4.  **[Week 2]** Implement the escalation pathway to the Pantheon Council and the HITL notification system.
5.  **[Week 3]** Develop and test the agent-alignment check mechanism.
6.  **[Week 4]** Roll out the Governance Layer in a "monitor-only" mode to gather data before enabling active enforcement.

---

## 6. References

[1] Glean. "Glean Announces Enterprise-Ready AI Platform with Centralized Governance and RAG." Glean Blog, March 10, 2026.

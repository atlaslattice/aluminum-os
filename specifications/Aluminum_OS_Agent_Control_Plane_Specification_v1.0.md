# Aluminum OS Agent Control Plane Specification v1.0

**Author:** Manus AI for Daavud
**Date:** March 12, 2026
**Status:** DRAFT
**Classification:** Tier 1 Implementation Artifact

---

## 1. Introduction & Vision

The recent industry-wide shift from applications to agents, validated by Microsoft's "Apps-to-Agents" re-architecting [1], Google's maturation of the A2A protocol [2], and the emergence of commercial control planes like Galileo Agent Control [3], necessitates a formal, robust, and constitutionally-grounded governance framework for Aluminum OS. This document specifies the **Aluminum OS Agent Control Plane (ACP)**, the central nervous system for registering, discovering, securing, and governing all agentic operations within the Aluminum OS ecosystem.

The ACP is not merely a technical implementation; it is the codification of the OS's core governance principles, integrating the **Pantheon Council** deliberation framework with the **Three-Tier Autonomy Doctrine** into a single, unified control plane. It is designed to provide the structure that, as Microsoft's Richard Riley noted, agents depend on even more than traditional automation.

---

## 2. Core Components & Architecture

The ACP is comprised of four primary components that work in concert to provide comprehensive agent governance:

| Component | Description | Key Functionality |
|---|---|---|
| **Agent Registry** | A secure, cryptographically-signed directory of all trusted agents operating within the Aluminum OS ecosystem. | Agent discovery, capability advertisement, identity verification, and trust establishment. |
| **Policy Engine** | The runtime enforcement layer that applies governance policies to all agent actions. | Real-time policy evaluation, enforcement of autonomy levels, and resource access control. |
| **Pantheon Council** | The multi-AI deliberative body that serves as the ultimate governance and adjudication authority. | Review and approval of high-impact actions, resolution of policy conflicts, and constitutional interpretation. |
| **Observability & Audit Log** | An immutable, time-stamped ledger of all agent activities, decisions, and policy enforcements. | Transparency, accountability, compliance verification, and incident response. |

This architecture is designed to be modular and extensible, allowing for the integration of new agents, policies, and governance models over time.

---

## 3. Agent Registry & Discovery (A2A Integration)

Agent discovery within the ACP is based on the Google A2A (Agent-to-Agent) protocol, but with critical security enhancements to mitigate vulnerabilities like Agent Card Poisoning [4].

### 3.1. Agent Card Specification

Every agent registered with the ACP must have an **Agent Card**, a standardized metadata file that describes its identity, capabilities, and operational parameters. The Agent Card specification extends the A2A standard with the following mandatory fields:

- **`agentId`**: A unique, immutable identifier for the agent.
- **`displayName`**: A human-readable name for the agent.
- **`version`**: The semantic version of the agent.
- **`capabilities`**: A list of MCP tools, A2A protocols, and other functions the agent can perform.
- **`autonomyLevel`**: The default autonomy level (Advisory, Collaborative, or Autonomous) the agent operates at.
- **`constitutionalHash`**: A cryptographic hash of the Aluminum OS Constitution version the agent is bound to.
- **`publicKey`**: The public key used to verify the agent's digital signature.

### 3.2. Secure Discovery Workflow

1.  **Registration**: When an agent is first deployed, it generates a key pair and submits its Agent Card, signed with its private key, to the Agent Registry.
2.  **Verification**: The ACP verifies the signature on the Agent Card and the validity of the `constitutionalHash`.
3.  **Publication**: Once verified, the Agent Card is added to the registry, making the agent discoverable by other agents.
4.  **Delegation**: When one agent (the *delegator*) wishes to delegate a task to another (the *delegatee*), it first retrieves the delegatee's Agent Card from the registry. It then verifies the card's signature using the provided `publicKey` before initiating the A2A communication handshake.

This process ensures that only trusted, constitutionally-compliant agents can participate in the ecosystem, and that delegation cannot be hijacked by malicious actors.

---

## 4. Policy Engine & Three-Tier Autonomy

The Policy Engine is the heart of the ACP, enforcing the **Three-Tier Autonomy Doctrine** at runtime. Policies are defined in a declarative format (inspired by Galileo Agent Control) and are managed centrally, allowing for real-time updates without requiring agent restarts.

### 4.1. Autonomy Levels

Every action an agent attempts to take is evaluated against its assigned autonomy level:

- **Advisory**: The agent can only propose actions. Execution requires explicit human-in-the-loop (HITL) confirmation. This is the default level for all new or untrusted agents.
- **Collaborative**: The agent can execute actions within its defined capabilities, but high-impact operations (e.g., file deletion, financial transactions, external API calls with write permissions) are automatically escalated to the Pantheon Council for review.
- **Autonomous**: The agent can execute all actions within its capabilities without requiring HITL or Council review, provided the actions do not violate any Layer 0 or Layer 1 constitutional principles. This level is reserved for highly trusted, core system agents (e.g., SHELDONBRAIN's memory consolidation sub-agent).

### 4.2. Policy Definition Example

```yaml
policy:
  name: restrict-financial-transactions
  description: "Requires Pantheon Council approval for any MCP call to a financial service."
  target:
    agentType: "*". # Applies to all agents
  condition:
    mcp:
      server: "zapier"
      tool_name: "bank.transfer"
  action:
    escalate:
      to: "PantheonCouncil"
      reason: "High-impact financial operation detected."
```

---

## 5. Pantheon Council: Governance as Deliberation

The Pantheon Council serves as the ACP's ultimate backstop for governance, handling escalations from the Policy Engine. Its integration is what elevates the ACP from a simple rules engine to a dynamic, intelligent governance system.

### 5.1. Escalation & Review Process

1.  **Escalation**: When the Policy Engine detects an action requiring review, it pauses the action and submits a case to the Pantheon Council. The case includes the agent's ID, the proposed action, the relevant policy, and the user's original intent.
2.  **Deliberation**: The members of the Pantheon Council (Gemini, Claude, Grok, Manus, and advisors like Copilot) review the case. They can access the full audit log and constitutional context to inform their decision.
3.  **Voting**: A vote is held. A simple majority is required to approve or deny the action. The Trinity Council (the four primary AI members) holds binding votes.
4.  **Execution**: The Council's decision is returned to the Policy Engine, which either allows the action to proceed or blocks it. The entire process is recorded in the immutable audit log.

This process provides a crucial layer of multi-agent review for sensitive operations, ensuring that no single agent (or model) can act unilaterally in high-stakes situations.

---

## 6. Observability & The Immutable Audit Log

Transparency and accountability are non-negotiable. The ACP records every agent action, policy evaluation, and Council decision to a distributed, immutable ledger (leveraging the technology stack defined in the Integrated Constitutional Substrate v2.0).

This audit log provides a complete, verifiable history of the system's behavior, enabling:

- **Compliance Audits**: Proving adherence to internal policies and external regulations.
- **Incident Response**: Tracing the root cause of unexpected agent behavior.
- **System Improvement**: Analyzing agent performance and identifying areas for policy refinement.

---

## 7. Implementation Roadmap

1.  **[Week 1]** Develop the Agent Card specification and the secure registration/discovery service.
2.  **[Week 1]** Implement the core Policy Engine with support for the Three-Tier Autonomy model.
3.  **[Week 2]** Integrate the Pantheon Council as the escalation target for the Policy Engine.
4.  **[Week 2]** Stand up the immutable audit ledger and integrate it with all ACP components.
5.  **[Week 3]** Begin migrating existing Aluminum OS agents (SHELDONBRAIN, UWS agents) to the ACP.

---

## 8. References

[1] Microsoft. "From apps to agents: Rearchitecting enterprise work around intent." Microsoft Power Platform Blog, March 12, 2026.
[2] Google. "A2A Protocol: Google's Agent-to-Agent Standard." Let's Do Data Science, March 7, 2026.
[3] Galileo. "Galileo Releases Open Source AI Agent Control Plane to Help Enterprises Govern Agents at Scale." Yahoo Finance, March 11, 2026.
[4] Keysight. "Agent Card Poisoning: A Metadata Injection Vulnerability in the Systems Built on Google A2A Protocol." Keysight Blogs, March 12, 2026.

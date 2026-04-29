# Aluminum OS + Copilot 365 Integration Guide

**Version:** 1.0
**Last Updated:** March 8, 2026

This document outlines the technical strategy for integrating the full **12,000-20,000+ feature surface** of Aluminum OS with Microsoft Copilot 365. The integration leverages Copilot Studio and the Model Context Protocol (MCP) to expose the `uws` CLI as a powerful, unified tool for Copilot.

---

## The "Alexandria Library" Concept

What Copilot metaphorically called the "Alexandria Library" is, in practice, the combination of two key Aluminum OS components:

1.  **The Alexandria Provider Driver:** The Rust-based module (`ms_graph.rs`) that connects Aluminum OS to the Microsoft Graph API.
2.  **The Knowledge Substrate:** Copilot's ability to ground prompts in enterprise data stored in SharePoint, OneDrive, and other Microsoft 365 services.

Our integration makes this concept a reality by turning the entire `uws` CLI into a massive, queryable library for Copilot.

---

## Integration Architecture

The integration follows a three-step architecture:

1.  **`uws` as an MCP Server:** The `uws` binary will be wrapped in a simple web server that exposes its full command surface over the Model Context Protocol (MCP). Every command, every flag, and every API method becomes a tool that MCP-compliant agents can discover and call.

2.  **Copilot Studio Connection:** A new "Aluminum OS Connector" will be created in Copilot Studio. This connector will point to the `uws` MCP server, allowing Copilot to see and understand all 12,000+ available tools.

3.  **Declarative Agent Definition:** The `ALEXANDRIA_CLI_SPEC.md` will be used as the basis for a declarative agent in Copilot Studio. This agent will be configured to use the Aluminum OS Connector, effectively giving it access to the entire unified feature manifest.

```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────────────┐
│                  │      │                  │      │                          │
│  Copilot 365     ├──────►  Copilot Studio  ├──────►   uws as MCP Server      │
│  (User Interface)│      │  (Connector Hub) │      │   (12,000+ Tools)        │
│                  │      │                  │      │                          │
└──────────────────┘      └──────────────────┘      └──────────────────────────┘
```

---

## How It Works in Practice

Once integrated, a user can ask Copilot a high-level question like:

> "Find the latest sales presentation from the Q4 planning meeting, summarize it, and email the summary to the marketing team."

Copilot, using the Aluminum OS agent, will break this down into a series of `uws` commands:

1.  **Search for the presentation:**
    - `uws drive files list --query "name contains 'sales presentation' and 'Q4' in parents" --provider google`
    - `uws onedrive search "sales presentation Q4" --provider microsoft`

2.  **Read the content:**
    - `uws slides presentations get --presentation-id <google_slide_id> --provider google`
    - `uws graph api get /drives/<drive-id>/items/<item-id>/content --provider microsoft`

3.  **Summarize the content:** (Using Copilot's internal summarization skill)

4.  **Email the summary:**
    - `uws gmail users messages send --json '{"to":"marketing@company.com", "subject":"Sales Presentation Summary", "body":"..."}' --provider google`

This workflow seamlessly combines features from Google Drive, OneDrive, Gmail, and Microsoft Graph, all orchestrated by Copilot through the unified `uws` command surface.

---

## Unifying Killer Features

The true power of this integration is not just exposing individual features, but creating **cross-ecosystem workflows** that were previously impossible. Examples include:

-   **Universal Search:** Search for a document across Google Drive, OneDrive, and SharePoint simultaneously.
-   **Cross-Platform Scheduling:** Find an open time slot across Google Calendar and Outlook Calendar.
-   **Unified Task Management:** Create a task in Microsoft To Do that links to a Google Doc.
-   **Multi-Cloud File Sync:** Copy a file from Google Drive to a shared folder in OneDrive.

By mapping the 18,000+ inherited features into the unified `alum` command structure, we provide Copilot with a powerful and consistent set of tools to solve complex, real-world problems that span multiple digital ecosystems.

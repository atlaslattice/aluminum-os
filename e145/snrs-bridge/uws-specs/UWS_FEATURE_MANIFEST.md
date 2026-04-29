# Aluminum OS — Unified Feature Manifest

**Version:** 1.0
**Last Updated:** March 8, 2026

This document provides a comprehensive, categorized manifest of all features, capabilities, and API endpoints unified under the Aluminum OS and exposed through the `uws` (Universal Workspace CLI) and `alum` command surfaces. The total addressable feature surface is estimated to be between **12,000 and 20,000+** unified operations.

---

## 1. Core Aluminum OS Features

These are foundational capabilities of the kernel itself, independent of any single provider.

| Feature | Description |
|---|---|
| **Unified Command Surface** | A single command grammar (`alum <verb> <resource>`) to interact with all integrated ecosystems. |
| **Provider Abstraction** | Interchangeable provider drivers for Google, Microsoft, Apple, and more. |
| **Multi-Agent Runtime** | First-class support for Claude, Manus, Gemini, and Copilot as council members. |
| **Constitutional Governance** | Enforces principles of dignity, neutrality, and non-exploitation at the agent runtime level. |
| **Unified Identity Substrate** | Manages authentication and identity across all connected accounts. |
| **Unified Memory Substrate** | A single graph for representing data and relationships across all ecosystems. |
| **Dynamic Skill Generation** | Automatically generates CLI commands and AI agent skills from API discovery documents. |

---

## 2. Google Provider (`--provider google`)

Leverages Google API Discovery Documents to dynamically generate commands for over 300+ Google APIs. The core Google Workspace surface area is detailed below.

| Service | Endpoints | Description |
|---|---|---|
| **Gmail** | 79 | Send, read, manage email, labels, and settings. |
| **Google Drive** | 57 | Manage files, folders, shared drives, permissions, and comments. |
| **Google Calendar** | 37 | Manage calendars, events, and scheduling. |
| **Google Sheets** | 17 | Read, write, and format spreadsheet data. |
| **Google Docs** | 3 | Read and perform basic edits on documents. |
| **Google Slides** | 5 | Read and perform basic edits on presentations. |
| **Google Tasks** | 14 | Manage task lists and individual tasks. |
| **Google People** | 24 | Manage contacts, contact groups, and profile information. |
| **Google Chat** | 37 | Manage spaces, members, and messages. |
| **Google Classroom** | 104 | Manage classes, rosters, coursework, and grades. |
| **Admin SDK** | 139 | Manage users, groups, licenses, and audit logs (Reports & Directory APIs). |
| **Other Workspace APIs** | ~50 | Includes Alert Center, Groups Settings, Reseller, Data Transfer, etc. |
| **All Other Google APIs** | 10,000-18,000+ | Dynamically available via discovery (e.g., YouTube, Maps, BigQuery, etc.). |

---

## 3. Microsoft Provider (`--provider microsoft`)

Integrates with the Microsoft 365 ecosystem via the Microsoft Graph API, exposing over 2,000+ endpoints.

| Service | Endpoints | Description |
|---|---|---|
| **Outlook Mail** | ~200+ | Send, read, and manage email, folders, and rules. |
| **Outlook Calendar** | ~150+ | Manage calendars, events, scheduling, and reminders. |
| **OneDrive** | ~100+ | Manage files, folders, permissions, and sharing. |
| **Microsoft Teams** | ~300+ | Manage teams, channels, messages, meetings, and apps. |
| **SharePoint** | ~500+ | Manage sites, lists, libraries, and pages. |
| **OneNote** | ~50+ | Manage notebooks, sections, and pages. |
| **Planner & To Do** | ~100+ | Manage plans, buckets, tasks, and checklists. |
| **Azure Active Directory** | ~400+ | Manage users, groups, devices, and identity. |
| **Other Graph APIs** | ~200+ | Includes Excel, Word, PowerPoint, Bookings, Viva, Intune, Security. |

---

## 4. Apple Provider (`--provider apple`)

Integrates with the Apple iCloud ecosystem via open standards and proprietary APIs.

| Service | Protocol/API | Description |
|---|---|---|
| **iCloud Calendar** | CalDAV | Manage calendars and events. |
| **iCloud Reminders** | CalDAV | Manage reminder lists and tasks. |
| **iCloud Contacts** | CardDAV | Manage contacts and groups. |
| **iCloud Drive** | CloudKit | Manage files and folders (requires further implementation). |
| **iCloud Notes** | Proprietary | Manage notes and folders (requires further implementation). |

---

## 5. Android & Chrome Provider

Integrates with Google's mobile and browser management ecosystems.

| Service | API | Description |
|---|---|---|
| **Android Management** | Android Management API | Manage enterprise devices, policies, and apps. |
| **Chrome Management** | Chrome Browser Cloud Management | Manage Chrome browsers across an organization. |
| **Chrome Policy** | Chrome Policy API | Manage user and browser policies for Chrome. |

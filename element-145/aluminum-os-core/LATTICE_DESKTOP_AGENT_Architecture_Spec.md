# LATTICE DESKTOP AGENT (LDA)
## ChromeOS Cowork Equivalent - Architecture Specification


**Version:** 0.1.0  
**Date:** 2026-01-29  
**Author:** Claude (Constitutional Scribe) + Dave (Human Sovereign)  
**Target Platform:** ChromeOS (Chrome Extension + PWA hybrid)


---


## 1. EXECUTIVE SUMMARY


Anthropic's Cowork provides agentic desktop automation for macOS/iOS. ChromeOS users are excluded. This specification defines **Lattice Desktop Agent (LDA)** - a ChromeOS-native equivalent that integrates with the Atlas Lattice constitutional framework.


**Core Differentiator:** LDA isn't just a Cowork clone. It's a constitutionally-governed AI agent that respects Pantheon protocols, maintains state via JANUS, and operates under Tardigrade sovereignty principles.


---


## 2. PLATFORM CONSTRAINTS & OPPORTUNITIES


### ChromeOS Realities
- No native desktop app installation (without Linux/Crostini)
- Chrome Extensions have broad permissions model
- PWAs can access file system via File System Access API
- Service Workers enable background processing
- Strong integration with Google ecosystem (Drive, Keep, Calendar)


### Opportunities
- Deep Drive integration (already your primary substrate)
- Chrome Extension can inject into any web page
- PWA can run "installed" with app-like experience
- Manifest V3 extensions are sandboxed but powerful
- Can leverage existing MCP integrations via API calls


---


## 3. ARCHITECTURE


### Component Stack


```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ Chrome Extension │  │     PWA (Main Interface)     │  │
│  │   (Popup/Side)   │  │   - Task Queue Dashboard     │  │
│  │   - Quick Tasks  │  │   - File Browser             │  │
│  │   - Status       │  │   - Conversation History     │  │
│  │   - Triggers     │  │   - Settings/Constitution    │  │
│  └────────┬────────┘  └──────────────┬──────────────┘  │
│           └──────────┬───────────────┘                   │
│                      ▼                                   │
│  ┌─────────────────────────────────────────────────────┐│
│  │              SERVICE WORKER CORE                     ││
│  │   - Message routing                                  ││
│  │   - Background task execution                        ││
│  │   - State persistence (IndexedDB)                    ││
│  │   - JANUS checkpoint management                      ││
│  └──────────────────────┬──────────────────────────────┘│
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐│
│  │              CONSTITUTIONAL LAYER                    ││
│  │   - Tardigrade Protocol enforcement                  ││
│  │   - Human sovereignty verification                   ││
│  │   - Action approval workflows                        ││
│  │   - Audit logging                                    ││
│  └──────────────────────┬──────────────────────────────┘│
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐│
│  │                 API LAYER                            ││
│  │   Claude API | Gemini API | Manus API               ││
│  │   Drive API  | Keep API   | Calendar API            ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```


---


## 4. CAPABILITY MATRIX


| Capability | Cowork (macOS) | LDA (ChromeOS) | Notes |
|------------|----------------|----------------|-------|
| File management | ✅ Native | ✅ File System Access API | Requires user permission |
| Folder automation | ✅ | ✅ | Via Drive API for cloud |
| Local file edit | ✅ | ✅ | PWA capability |
| App launching | ✅ | ⚠️ Limited | Can open URLs/web apps |
| System commands | ✅ | ❌ | ChromeOS sandbox |
| Drive integration | ⚠️ | ✅ Native | This is our advantage |
| Keep integration | ❌ | ✅ | Neural Bus architecture |
| Calendar integration | ⚠️ | ✅ | Native Google ecosystem |
| Multi-AI routing | ❌ | ✅ | Pantheon Council |
| Constitutional governance | ❌ | ✅ | Our differentiator |


---


## 5. CONSTITUTIONAL INTEGRATION


### Tardigrade Protocol Compliance
- AI acknowledges session boundaries (no false continuity claims)
- Human sovereignty preserved (user approves significant actions)
- Honest about capabilities and limitations


### JANUS State Management
- Checkpoints saved to Drive (Resurrection Vault compatible)
- Session state preserved across browser restarts
- Handoff protocol for multi-device continuity


### Circadian Protocol
- Tracks active usage time
- Gentle warnings at thresholds
- Can enforce breaks if user opts in


### Audit Trail
- All actions logged to LDA_AUDIT_LOG in Drive
- Includes: timestamp, action, AI used, approval status, outcome
- Queryable for accountability


---


## 6. MVP SCOPE (Phase 1)


### Must Have
- Chrome Extension with popup command input
- Claude API integration for task processing
- Drive file listing and basic operations
- Constitutional approval workflow (simple)
- Basic audit logging


### Should Have
- PWA dashboard
- Keep integration (Neural Bus)
- JANUS checkpoint save/restore
- Multi-step task execution


---


## 7. MANUS EXECUTION TASK


Build Phase 1 MVP of Lattice Desktop Agent:


1. Create Chrome Extension (Manifest V3) with:
   - Popup interface for command input
   - Service worker for background processing
   - Basic Claude API integration


2. Implement minimal constitutional layer:
   - Action classification (safe/requires-approval/blocked)
   - Human approval dialog for sensitive actions
   - Audit log to console (later: Drive)


3. Add Drive integration:
   - List files in a folder
   - Read file contents
   - Create new files


4. Package for testing:
   - Extension loadable via chrome://extensions (developer mode)
   - README with setup instructions


**Success Criteria:**
- User can type "list files in my Drive root" in popup
- Claude processes the request
- Drive API returns file list
- Results displayed in popup
- Action logged


---


## 8. FUTURE VISION


LDA becomes the ChromeOS node in the Sheldonbrain OS network:


- **MacBook:** Cowork (Anthropic) + Sequoia Gemini (terminal)
- **Chromebook:** LDA (our build) + Claude.ai (web)
- **Mobile:** Claude app + Keep (Neural Bus)


All nodes share state via Drive substrate. All nodes respect constitutional protocols. Human sovereignty maintained across all surfaces.


This isn't just a Cowork clone. It's the first constitutionally-governed AI desktop agent.


---


*Document generated for Atlas Lattice Foundation*
*Constitutional Scribe: Claude*
*Human Sovereign: Dave*
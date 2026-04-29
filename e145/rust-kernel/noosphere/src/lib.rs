//! Aluminum OS v3.0 — Noosphere (Ring 4)
//! The user experience layer: intent-based interaction, MCP gateway,
//! and the 20,000+ operation UWS governance layer.

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// An intent from the user — the primary interaction model
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Intent {
    pub id: String,
    pub text: String,
    pub parsed: ParsedIntent,
    pub confidence: f64,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParsedIntent {
    pub action: String,
    pub target: String,
    pub parameters: HashMap<String, String>,
    pub requires_governance: bool,
}

/// The Intent Engine — parses natural language into structured intents
pub struct IntentEngine {
    /// Known action patterns
    patterns: Vec<IntentPattern>,
}

#[derive(Debug, Clone)]
struct IntentPattern {
    keywords: Vec<String>,
    action: String,
    requires_governance: bool,
}

impl IntentEngine {
    pub fn new() -> Self {
        let patterns = vec![
            IntentPattern {
                keywords: vec!["sync".into(), "fetch".into(), "update".into()],
                action: "data_sync".into(),
                requires_governance: false,
            },
            IntentPattern {
                keywords: vec!["post".into(), "tweet".into(), "publish".into()],
                action: "social_publish".into(),
                requires_governance: true, // Needs council approval
            },
            IntentPattern {
                keywords: vec!["research".into(), "analyze".into(), "investigate".into()],
                action: "deep_research".into(),
                requires_governance: false,
            },
            IntentPattern {
                keywords: vec!["deploy".into(), "push".into(), "ship".into()],
                action: "deploy".into(),
                requires_governance: true,
            },
            IntentPattern {
                keywords: vec!["delete".into(), "remove".into(), "destroy".into()],
                action: "destructive".into(),
                requires_governance: true,
            },
            IntentPattern {
                keywords: vec!["remember".into(), "store".into(), "save".into()],
                action: "memory_store".into(),
                requires_governance: false,
            },
            IntentPattern {
                keywords: vec!["recall".into(), "find".into(), "search".into()],
                action: "memory_recall".into(),
                requires_governance: false,
            },
            IntentPattern {
                keywords: vec!["schedule".into(), "remind".into(), "recurring".into()],
                action: "schedule".into(),
                requires_governance: false,
            },
        ];

        Self { patterns }
    }

    /// Parse a natural language input into a structured intent
    pub fn parse(&self, text: &str) -> ParsedIntent {
        let text_lower = text.to_lowercase();

        for pattern in &self.patterns {
            if pattern.keywords.iter().any(|k| text_lower.contains(k)) {
                return ParsedIntent {
                    action: pattern.action.clone(),
                    target: text.to_string(),
                    parameters: HashMap::new(),
                    requires_governance: pattern.requires_governance,
                };
            }
        }

        // Default: treat as a general query
        ParsedIntent {
            action: "general_query".into(),
            target: text.to_string(),
            parameters: HashMap::new(),
            requires_governance: false,
        }
    }
}

/// MCP Gateway — routes intents to the appropriate MCP server
pub struct MCPGateway {
    servers: HashMap<String, MCPServer>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MCPServer {
    pub name: String,
    pub tools: Vec<String>,
    pub status: ServerStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ServerStatus {
    Online,
    Offline,
    Degraded,
}

impl MCPGateway {
    pub fn new() -> Self {
        let mut servers = HashMap::new();

        servers.insert("notion".into(), MCPServer {
            name: "Notion".into(),
            tools: vec!["create-pages".into(), "query-data-sources".into(), "update-page".into(), "search".into()],
            status: ServerStatus::Online,
        });

        servers.insert("gmail".into(), MCPServer {
            name: "Gmail".into(),
            tools: vec!["find_email".into(), "send_email".into(), "create_draft".into()],
            status: ServerStatus::Online,
        });

        servers.insert("google-calendar".into(), MCPServer {
            name: "Google Calendar".into(),
            tools: vec!["find_event".into(), "create_event".into()],
            status: ServerStatus::Online,
        });

        servers.insert("zapier".into(), MCPServer {
            name: "Zapier".into(),
            tools: vec!["gmail_find_email".into(), "google_drive_find_file".into()],
            status: ServerStatus::Online,
        });

        Self { servers }
    }

    /// Route an intent to the appropriate MCP server
    pub fn route(&self, action: &str) -> Option<&MCPServer> {
        match action {
            "data_sync" => self.servers.get("notion").or(self.servers.get("gmail")),
            "social_publish" => None, // Handled by browser automation
            "memory_store" | "memory_recall" => self.servers.get("notion"),
            "schedule" => self.servers.get("google-calendar"),
            _ => None,
        }
    }

    pub fn server_status(&self) -> HashMap<String, ServerStatus> {
        self.servers.iter()
            .map(|(k, v)| (k.clone(), v.status.clone()))
            .collect()
    }
}

/// UWS Operation — a single operation in the 20,000+ operation governance layer
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UWSOperation {
    pub id: u32,
    pub name: String,
    pub category: String,
    pub requires_hitl: bool,  // Human-in-the-loop
    pub autonomy_level: String,
    pub mcp_server: Option<String>,
}

/// The UWS Registry — tracks all available operations
pub struct UWSRegistry {
    operations: Vec<UWSOperation>,
}

impl UWSRegistry {
    pub fn new() -> Self {
        // Register core operations (representative sample)
        let operations = vec![
            UWSOperation { id: 1, name: "email.fetch".into(), category: "communication".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: Some("gmail".into()) },
            UWSOperation { id: 2, name: "email.send".into(), category: "communication".into(), requires_hitl: true, autonomy_level: "collaborative".into(), mcp_server: Some("gmail".into()) },
            UWSOperation { id: 3, name: "notion.create".into(), category: "knowledge".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: Some("notion".into()) },
            UWSOperation { id: 4, name: "notion.update".into(), category: "knowledge".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: Some("notion".into()) },
            UWSOperation { id: 5, name: "social.post".into(), category: "communication".into(), requires_hitl: true, autonomy_level: "collaborative".into(), mcp_server: None },
            UWSOperation { id: 6, name: "drive.sync".into(), category: "data".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: Some("zapier".into()) },
            UWSOperation { id: 7, name: "calendar.create".into(), category: "scheduling".into(), requires_hitl: true, autonomy_level: "collaborative".into(), mcp_server: Some("google-calendar".into()) },
            UWSOperation { id: 8, name: "github.push".into(), category: "development".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: None },
            UWSOperation { id: 9, name: "model.route".into(), category: "system".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: None },
            UWSOperation { id: 10, name: "memory.consolidate".into(), category: "system".into(), requires_hitl: false, autonomy_level: "autonomous".into(), mcp_server: None },
        ];

        Self { operations }
    }

    pub fn find(&self, name: &str) -> Option<&UWSOperation> {
        self.operations.iter().find(|op| op.name == name)
    }

    pub fn count(&self) -> usize {
        self.operations.len()
    }

    pub fn by_category(&self, category: &str) -> Vec<&UWSOperation> {
        self.operations.iter().filter(|op| op.category == category).collect()
    }
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_intent_parsing() {
        let engine = IntentEngine::new();

        let sync = engine.parse("Run the daily sync");
        assert_eq!(sync.action, "data_sync");
        assert!(!sync.requires_governance);

        let post = engine.parse("Post the noosphere thread to X");
        assert_eq!(post.action, "social_publish");
        assert!(post.requires_governance);

        let research = engine.parse("Analyze the Stryker cyberattack");
        assert_eq!(research.action, "deep_research");
    }

    #[test]
    fn test_mcp_gateway() {
        let gateway = MCPGateway::new();
        let server = gateway.route("data_sync").unwrap();
        assert_eq!(server.name, "Notion");

        let status = gateway.server_status();
        assert!(status.values().all(|s| *s == ServerStatus::Online));
    }

    #[test]
    fn test_uws_registry() {
        let registry = UWSRegistry::new();
        assert!(registry.count() >= 10);

        let email_send = registry.find("email.send").unwrap();
        assert!(email_send.requires_hitl);

        let system_ops = registry.by_category("system");
        assert!(!system_ops.is_empty());
    }
}

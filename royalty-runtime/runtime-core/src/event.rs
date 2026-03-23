use std::time::{SystemTime, UNIX_EPOCH};
use serde::{Deserialize, Serialize};

/// An execution event — the atomic unit of the Royalty ledger.
///
/// When code runs, this fires. It captures the session identity,
/// the package being executed, the cryptographic lineage hash,
/// and a timestamp. This event is emitted to the Royalty Collector
/// for immutable storage and later attribution.
#[derive(Debug, Serialize, Deserialize)]
pub struct ExecutionEvent {
    pub session_id: String,
    pub primary_package: String,
    pub dependency_tree_hash: String,
    pub lineage_payload_version: String,
    pub timestamp: u64,
    pub sdk_version: String,
    /// Whether the premium (leased) execution path was enabled
    pub premium_path_enabled: bool,
    /// The lease ID if a commercial lease was used
    pub lease_id: Option<String>,
}

impl ExecutionEvent {
    /// Emit an execution event for the given package and lineage hash.
    ///
    /// In v0.1, this prints to stdout. In production, this would
    /// be shipped to the Royalty Collector via gRPC or HTTP.
    pub fn emit(
        package: &str,
        tree_hash: &str,
        premium: bool,
        lease_id: Option<String>,
    ) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let event = ExecutionEvent {
            session_id: uuid::Uuid::new_v4().to_string(),
            primary_package: package.to_string(),
            dependency_tree_hash: tree_hash.to_string(),
            lineage_payload_version: "1".to_string(),
            timestamp,
            sdk_version: "0.1.0".to_string(),
            premium_path_enabled: premium,
            lease_id,
        };

        println!(
            "[ROYALTY] Execution registered: {} | hash: {}...{} | premium: {} | ts: {}",
            event.primary_package,
            &event.dependency_tree_hash[..8],
            &event.dependency_tree_hash[event.dependency_tree_hash.len()-4..],
            event.premium_path_enabled,
            event.timestamp
        );

        event
    }
}
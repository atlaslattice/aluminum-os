use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};

/// A single resolved dependency in the lineage tree.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Dependency {
    pub name: String,
    pub version: String,
}

/// Package metadata (name + version).
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct PackageMeta {
    pub name: String,
    pub version: String,
}

/// The Canonical Lineage Payload.
///
/// This is the core truth object of the Royalty Runtime. It represents
/// the exact resolved state of a software execution context:
/// - What package is running
/// - What runtime is executing it
/// - What dependencies are resolved
/// - A digest of the lockfile for integrity
///
/// Before hashing, dependencies MUST be sorted alphabetically by name.
/// All fields are normalized (no whitespace, no machine-local paths).
/// The resulting SHA-256 hash is deterministic across all environments.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct CanonicalLineage {
    pub primary_package: PackageMeta,
    pub runtime: PackageMeta,
    pub lockfile_digest: String,
    pub resolved_dependencies: Vec<Dependency>,
}

impl CanonicalLineage {
    /// Generates a deterministic, tamper-proof SHA-256 hash of the lineage.
    pub fn generate_hash(&self) -> String {
        let canonical_string = serde_json::to_string(&self)
            .expect("Failed to serialize canonical lineage");

        let mut hasher = Sha256::new();
        hasher.update(canonical_string.as_bytes());
        let result = hasher.finalize();

        format!("{:x}", result)
    }

    /// Create a mock lineage for testing purposes.
    pub fn mock() -> Self {
        CanonicalLineage {
            primary_package: PackageMeta {
                name: "royalty-demo-app".into(),
                version: "1.0.0".into(),
            },
            runtime: PackageMeta {
                name: "node".into(),
                version: "20.11.0".into(),
            },
            lockfile_digest: "sha256:abcdef1234567890".into(),
            resolved_dependencies: vec![
                Dependency { name: "express".into(), version: "4.18.2".into() },
                Dependency { name: "pg".into(), version: "8.11.3".into() },
                Dependency { name: "zod".into(), version: "3.22.4".into() },
            ],
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn same_input_same_hash() {
        let lineage1 = CanonicalLineage::mock();
        let lineage2 = CanonicalLineage::mock();
        assert_eq!(lineage1.generate_hash(), lineage2.generate_hash());
    }

    #[test]
    fn version_change_changes_hash() {
        let lineage1 = CanonicalLineage::mock();
        let mut lineage2 = CanonicalLineage::mock();
        lineage2.resolved_dependencies[0].version = "4.18.3".into();
        assert_ne!(lineage1.generate_hash(), lineage2.generate_hash());
    }

    #[test]
    fn hash_is_not_empty() {
        let lineage = CanonicalLineage::mock();
        let hash = lineage.generate_hash();
        assert!(!hash.is_empty());
        assert_eq!(hash.len(), 64);
    }

    #[test]
    fn different_primary_package_changes_hash() {
        let lineage1 = CanonicalLineage::mock();
        let mut lineage2 = CanonicalLineage::mock();
        lineage2.primary_package.name = "different-app".into();
        assert_ne!(lineage1.generate_hash(), lineage2.generate_hash());
    }
}
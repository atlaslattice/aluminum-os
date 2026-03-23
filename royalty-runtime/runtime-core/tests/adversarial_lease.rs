use runtime_core::tracer::{CanonicalLineage, PackageMeta, Dependency};
use runtime_core::engine::RoyaltyEngine;
use jsonwebtoken::{encode, Header, EncodingKey, Algorithm};
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize)]
struct LeaseClaims {
    sub: String,
    lineage_hash: String,
    capabilities: Vec<String>,
    exp: usize,
}

fn get_test_lineage(app_name: &str) -> CanonicalLineage {
    CanonicalLineage {
        primary_package: PackageMeta {
            name: app_name.into(),
            version: "1.0.0".into(),
        },
        runtime: PackageMeta {
            name: "node".into(),
            version: "20.11.0".into(),
        },
        lockfile_digest: "sha256:test".into(),
        resolved_dependencies: vec![
            Dependency { name: "express".into(), version: "4.18.2".into() },
        ],
    }
}

fn generate_mock_token(lineage_hash: &str, exp: usize) -> String {
    let claims = LeaseClaims {
        sub: "test_tenant".into(),
        lineage_hash: lineage_hash.into(),
        capabilities: vec!["enterprise_concurrency".into()],
        exp,
    };
    encode(
        &Header::new(Algorithm::HS256),
        &claims,
        &EncodingKey::from_secret(b"royalty-runtime-dev-secret"),
    )
    .unwrap()
}

#[test]
fn test_expired_lease_downgrades_to_free_tier() {
    let lineage = get_test_lineage("app_A");
    let expired_token = generate_mock_token(&lineage.generate_hash(), 0);
    let engine = RoyaltyEngine::unlock(Some(&expired_token), &lineage);
    assert!(!engine.is_enterprise);
}

#[test]
fn test_stolen_lease_fails_on_hash_mismatch() {
    let lineage_a = get_test_lineage("app_A");
    let valid_token_for_a = generate_mock_token(&lineage_a.generate_hash(), 9999999999);
    let lineage_b = get_test_lineage("app_B");
    let engine_b = RoyaltyEngine::unlock(Some(&valid_token_for_a), &lineage_b);
    assert!(!engine_b.is_enterprise);
}

#[test]
fn test_forged_signature_fails() {
    let lineage = get_test_lineage("app_A");
    let forged_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmYWtlIn0.fake_signature";
    let engine = RoyaltyEngine::unlock(Some(forged_token), &lineage);
    assert!(!engine.is_enterprise);
}

#[test]
fn test_valid_lease_unlocks_premium_path() {
    let lineage = get_test_lineage("app_A");
    let valid_token = generate_mock_token(&lineage.generate_hash(), 9999999999);
    let engine = RoyaltyEngine::unlock(Some(&valid_token), &lineage);
    assert!(engine.is_enterprise);
    assert!(engine.thread_pool_size > 1);
}

#[test]
fn test_no_lease_gives_free_tier() {
    let lineage = get_test_lineage("app_A");
    let engine = RoyaltyEngine::unlock(None, &lineage);
    assert!(!engine.is_enterprise);
    assert_eq!(engine.thread_pool_size, 1);
}

#[test]
fn test_empty_string_lease_gives_free_tier() {
    let lineage = get_test_lineage("app_A");
    let engine = RoyaltyEngine::unlock(Some(""), &lineage);
    assert!(!engine.is_enterprise);
}
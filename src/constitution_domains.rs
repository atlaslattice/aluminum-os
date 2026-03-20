//! Constitutional Domains — 15 governance domains extracted from
//! 40 empty AI governance repos in the splitmerge420 GitHub org.
//!
//! Each repo's intent was analyzed, categorized, and collapsed into
//! typed enum variants. This is the repo shred's first concrete output:
//! 40 placeholder repos → 15 domain types → 14 default rules.

/// The 15 constitutional governance domains.
/// Extracted from: ai-ethics-*, responsible-ai-*, ai-governance-*,
/// ai-safety-*, ai-fairness-*, ai-transparency-*, ai-accountability-*,
/// and related repos.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConstitutionalDomain {
    /// General governance and administration
    GeneralGovernance,
    /// Data privacy, consent, and PII handling
    DataPrivacy,
    /// Transparency and audit trail requirements
    TransparencyAudit,
    /// Human oversight and override capabilities (HITL)
    HumanOversight,
    /// Fairness, bias detection, and mitigation
    FairnessBias,
    /// AI safety and alignment constraints
    SafetyAlignment,
    /// Model and decision explainability
    Explainability,
    /// Accountability and liability frameworks
    AccountabilityLiability,
    /// Resource allocation and compute governance
    ResourceGovernance,
    /// Cross-border data and regulatory compliance
    CrossBorderCompliance,
    /// Environmental impact assessment
    EnvironmentalImpact,
    /// Interoperability standards (MCP, A2A, etc.)
    InteroperabilityStandards,
    /// Dispute resolution and arbitration
    DisputeResolution,
    /// Digital sovereignty and jurisdictional autonomy
    DigitalSovereignty,
    /// Emergency protocols and circuit breakers
    EmergencyProtocols,
}

impl ConstitutionalDomain {
    /// All 15 domains as a static array
    pub const ALL: [ConstitutionalDomain; 15] = [
        Self::GeneralGovernance,
        Self::DataPrivacy,
        Self::TransparencyAudit,
        Self::HumanOversight,
        Self::FairnessBias,
        Self::SafetyAlignment,
        Self::Explainability,
        Self::AccountabilityLiability,
        Self::ResourceGovernance,
        Self::CrossBorderCompliance,
        Self::EnvironmentalImpact,
        Self::InteroperabilityStandards,
        Self::DisputeResolution,
        Self::DigitalSovereignty,
        Self::EmergencyProtocols,
    ];

    /// Human-readable name
    pub fn name(&self) -> &'static str {
        match self {
            Self::GeneralGovernance => "General Governance",
            Self::DataPrivacy => "Data Privacy",
            Self::TransparencyAudit => "Transparency & Audit",
            Self::HumanOversight => "Human Oversight (HITL)",
            Self::FairnessBias => "Fairness & Bias",
            Self::SafetyAlignment => "Safety & Alignment",
            Self::Explainability => "Explainability",
            Self::AccountabilityLiability => "Accountability & Liability",
            Self::ResourceGovernance => "Resource Governance",
            Self::CrossBorderCompliance => "Cross-Border Compliance",
            Self::EnvironmentalImpact => "Environmental Impact",
            Self::InteroperabilityStandards => "Interoperability Standards",
            Self::DisputeResolution => "Dispute Resolution",
            Self::DigitalSovereignty => "Digital Sovereignty",
            Self::EmergencyProtocols => "Emergency Protocols",
        }
    }

    /// 144-Sphere Ontology tag for this domain.
    ///
    /// Format: `H{house}.S{sphere}` where houses 1–12 each contain 12 spheres
    /// (12 houses × 12 spheres = 144 total). Tags reference the canonical
    /// `splitmerge420/144-sphere-ontology` registry.
    pub fn sphere_tag(&self) -> &'static str {
        match self {
            Self::GeneralGovernance        => "H6.S1",  // Governance — constitutional governance
            Self::DataPrivacy              => "H3.S4",  // Rights — privacy & consent
            Self::TransparencyAudit        => "H3.S9",  // Rights — transparency
            Self::HumanOversight           => "H4.S3",  // Human-AI — HITL oversight
            Self::FairnessBias             => "H4.S5",  // Human-AI — fairness & bias
            Self::SafetyAlignment          => "H4.S7",  // Human-AI — safety & alignment
            Self::Explainability           => "H4.S9",  // Human-AI — explainability
            Self::AccountabilityLiability  => "H6.S6",  // Governance — accountability
            Self::ResourceGovernance       => "H2.S8",  // Resources — compute governance
            Self::CrossBorderCompliance    => "H6.S11", // Governance — international compliance
            Self::EnvironmentalImpact      => "H2.S4",  // Resources — environmental impact
            Self::InteroperabilityStandards => "H7.S3", // Technology — systems architecture
            Self::DisputeResolution        => "H6.S7",  // Governance — dispute resolution
            Self::DigitalSovereignty       => "H6.S12", // Governance — digital sovereignty
            Self::EmergencyProtocols       => "H4.S12", // Human-AI — emergency & circuit breakers
        }
    }

    /// Source repos this domain was extracted from (representative examples)
    pub fn source_repos(&self) -> &'static [&'static str] {
        match self {
            Self::GeneralGovernance => &["ai-governance-framework", "ai-governance-toolkit"],
            Self::DataPrivacy => &["ai-privacy-framework", "data-privacy-toolkit"],
            Self::TransparencyAudit => &["ai-transparency-report", "ai-audit-framework"],
            Self::HumanOversight => &["human-in-the-loop-ai", "ai-oversight-board"],
            Self::FairnessBias => &["ai-fairness-toolkit", "ai-bias-detection"],
            Self::SafetyAlignment => &["ai-safety-framework", "ai-alignment-research"],
            Self::Explainability => &["ai-explainability-toolkit", "xai-framework"],
            Self::AccountabilityLiability => &["ai-accountability-framework", "ai-liability-model"],
            Self::ResourceGovernance => &["ai-resource-management", "compute-governance"],
            Self::CrossBorderCompliance => &["ai-cross-border-compliance", "gdpr-ai-toolkit"],
            Self::EnvironmentalImpact => &["ai-environmental-impact", "green-ai-framework"],
            Self::InteroperabilityStandards => &["ai-interop-standards", "mcp-compliance"],
            Self::DisputeResolution => &["ai-dispute-resolution", "ai-arbitration-protocol"],
            Self::DigitalSovereignty => &["digital-sovereignty-ai", "sovereign-ai-framework"],
            Self::EmergencyProtocols => &["ai-emergency-protocols", "ai-circuit-breaker"],
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_domain_count() {
        assert_eq!(ConstitutionalDomain::ALL.len(), 15);
    }

    #[test]
    fn test_all_domains_have_names() {
        for domain in ConstitutionalDomain::ALL.iter() {
            assert!(!domain.name().is_empty());
        }
    }

    #[test]
    fn test_all_domains_have_source_repos() {
        for domain in ConstitutionalDomain::ALL.iter() {
            assert!(!domain.source_repos().is_empty());
        }
    }

    #[test]
    fn test_domain_equality() {
        assert_eq!(ConstitutionalDomain::DataPrivacy, ConstitutionalDomain::DataPrivacy);
        assert_ne!(ConstitutionalDomain::DataPrivacy, ConstitutionalDomain::SafetyAlignment);
    }

    #[test]
    fn test_domains_unique() {
        // Verify all 15 domains are distinct
        for i in 0..ConstitutionalDomain::ALL.len() {
            for j in (i + 1)..ConstitutionalDomain::ALL.len() {
                assert_ne!(ConstitutionalDomain::ALL[i], ConstitutionalDomain::ALL[j]);
            }
        }
    }

    #[test]
    fn test_specific_domain_names() {
        assert_eq!(ConstitutionalDomain::DataPrivacy.name(), "Data Privacy");
        assert_eq!(ConstitutionalDomain::HumanOversight.name(), "Human Oversight (HITL)");
        assert_eq!(ConstitutionalDomain::EmergencyProtocols.name(), "Emergency Protocols");
    }

    #[test]
    fn test_all_domains_have_sphere_tags() {
        for domain in ConstitutionalDomain::ALL.iter() {
            let tag = domain.sphere_tag();
            assert!(!tag.is_empty(), "{:?} has empty sphere_tag", domain);
            // Validate format: H{1-12}.S{1-12}
            assert!(tag.starts_with('H'), "{:?} sphere_tag should start with H: {}", domain, tag);
            assert!(tag.contains(".S"), "{:?} sphere_tag missing .S separator: {}", domain, tag);
        }
    }

    #[test]
    fn test_interoperability_sphere_tag() {
        // InteroperabilityStandards maps to H7.S3 (Systems Architecture) —
        // matches the established tag used across PLUGIN_REGISTRY.yaml
        assert_eq!(
            ConstitutionalDomain::InteroperabilityStandards.sphere_tag(),
            "H7.S3"
        );
    }

    #[test]
    fn test_sphere_tags_cover_multiple_houses() {
        // Domains should spread across governance (H6), human-AI (H4), resources (H2), technology (H7)
        let tags: Vec<_> = ConstitutionalDomain::ALL.iter().map(|d| d.sphere_tag()).collect();
        let houses: std::collections::HashSet<&str> = tags.iter()
            .map(|t| t.split('.').next().unwrap())
            .collect();
        assert!(houses.len() >= 4, "Expected sphere tags across at least 4 houses, got: {:?}", houses);
    }
}

import SpecLayout from "@/components/SpecLayout";
import { GITHUB_URL } from "@/lib/data";
import { ArrowRight, BookOpen, ExternalLink, Search } from "lucide-react";
import { useState, useMemo } from "react";

type DoctrineStatus = "RATIFIED" | "UNDER_DISCUSSION" | "PROPOSED" | "AMENDED";

interface Doctrine {
  id: string;
  name: string;
  status: DoctrineStatus;
  category: string;
  summary: string;
  proposedBy?: string;
  version?: string;
}

// Canonical doctrines registry — D-1 through D-95 ratified + D-96 through D-101 under discussion
// Source: ORC-017, Build Plan v2.3, Council deliberations
const doctrines: Doctrine[] = [
  // Core governance (D-1 through D-10)
  { id: "D-1", name: "Constitutional Primacy", status: "RATIFIED", category: "governance", summary: "The constitutional framework takes precedence over all other governance instruments.", version: "v1.0" },
  { id: "D-2", name: "Human Sovereignty Guarantee", status: "RATIFIED", category: "governance", summary: "Human decision-making authority is inviolable. AI systems advise; humans decide.", version: "v1.0" },
  { id: "D-3", name: "Multi-Vendor Architecture", status: "RATIFIED", category: "architecture", summary: "The system must support multiple AI providers simultaneously. No single-vendor lock-in.", version: "v1.0" },
  { id: "D-4", name: "Open Ontology", status: "RATIFIED", category: "ontology", summary: "The 12×12 lattice structure is publicly documented and freely implementable.", version: "v1.0" },
  { id: "D-5", name: "Adversarial Review Requirement", status: "RATIFIED", category: "governance", summary: "Every major routing decision must be reviewable by at least one adversarial Council seat.", version: "v1.0" },
  { id: "D-6", name: "Dialect Sovereignty", status: "RATIFIED", category: "routing", summary: "Each jurisdiction's dialect overlay has authority over its domain-specific routing rules.", version: "v1.0" },
  { id: "D-7", name: "Provenance Chain Mandate", status: "RATIFIED", category: "verification", summary: "All knowledge claims must carry verifiable provenance from source to current state.", version: "v1.0" },
  { id: "D-8", name: "Zero Erasure Policy", status: "RATIFIED", category: "storage", summary: "Committed knowledge artifacts are archived, never deleted. Superseded data remains accessible.", version: "v1.0" },
  { id: "D-9", name: "Council Quorum Rules", status: "RATIFIED", category: "governance", summary: "0.67 quorum of active seats required for decisions. Provisional seats vote but don't count toward quorum.", version: "v1.0" },
  { id: "D-10", name: "Convenor Authority", status: "RATIFIED", category: "governance", summary: "The Convenor (human) holds tie-break authority and final ratification power.", version: "v1.0" },

  // Ontology & structure (D-11 through D-25)
  { id: "D-11", name: "House Immutability", status: "RATIFIED", category: "ontology", summary: "The 12 Houses are fixed. New knowledge domains are accommodated within existing Houses or as sub-spheres.", version: "v2.0" },
  { id: "D-12", name: "Sphere Addressing Standard", status: "RATIFIED", category: "ontology", summary: "Every sphere has a canonical address: H{n}-S{nnn}. Sub-spheres use SS-{nnnn} notation.", version: "v2.0" },
  { id: "D-13", name: "VIP Element Registration", status: "RATIFIED", category: "ontology", summary: "New VIP Elements require Council supermajority and demonstrated cross-House impact.", version: "v3.0" },
  { id: "D-14", name: "Sub-Sphere Expansion Protocol", status: "RATIFIED", category: "ontology", summary: "Sub-spheres may be added by any Council seat with 0.67 quorum approval. No upper limit per sphere.", version: "v2.0" },
  { id: "D-15", name: "Cross-House Adjacency", status: "RATIFIED", category: "ontology", summary: "Adjacency relationships between spheres in different Houses must be explicitly declared and versioned.", version: "v2.0" },
  { id: "D-16", name: "Ontology Migration Safety", status: "RATIFIED", category: "ontology", summary: "Schema changes must be backward-compatible within a major version. Breaking changes require new major version.", version: "v2.0" },
  { id: "D-17", name: "Knowledge Node Completeness", status: "RATIFIED", category: "ontology", summary: "Every sphere must have at least one active sub-sphere. Empty spheres are flagged for review.", version: "v2.0" },
  { id: "D-18", name: "Lattice Consistency Check", status: "RATIFIED", category: "ontology", summary: "Automated consistency checks run on every schema change. Inconsistencies block deployment.", version: "v2.0" },
  { id: "D-19", name: "VIP Cascade Priority", status: "RATIFIED", category: "routing", summary: "When a query touches multiple VIP Elements, the cascade resolves priority based on sovereignty gradient.", version: "v3.0" },
  { id: "D-20", name: "Module Registration", status: "RATIFIED", category: "routing", summary: "New routing modules must be registered with capability declaration before activation.", version: "v2.0" },

  // Routing & compute (D-21 through D-40)
  { id: "D-21", name: "Cascade Determinism", status: "RATIFIED", category: "routing", summary: "Identical inputs must produce identical routing decisions. Non-determinism triggers error mode.", version: "v2.0" },
  { id: "D-22", name: "Provider Capability Matrix", status: "RATIFIED", category: "routing", summary: "Every AI provider must declare capabilities. Undeclared capabilities are excluded from routing.", version: "v2.0" },
  { id: "D-23", name: "Graceful Degradation", status: "RATIFIED", category: "routing", summary: "System degrades gracefully under load: VIP cascade first, then core routing, then static fallback.", version: "v2.0" },
  { id: "D-24", name: "Compute Zone Classification", status: "RATIFIED", category: "routing", summary: "Three compute zones: Standard, Mixed-Compliance, and Contested. Zone determines available providers.", version: "v3.0" },
  { id: "D-25", name: "Emergency Mode Protocol", status: "RATIFIED", category: "routing", summary: "Low-Power/Emergency mode activates when compute resources fall below threshold. Essential routing only.", version: "v2.0" },
  { id: "D-26", name: "Federation Protocol", status: "RATIFIED", category: "routing", summary: "Cross-seat communication uses the Federation Bridge. Direct seat-to-seat channels are prohibited.", version: "v2.0" },
  { id: "D-27", name: "Load Balancing", status: "RATIFIED", category: "routing", summary: "Routing load is distributed across available providers based on capability match, not cost optimization.", version: "v2.0" },
  { id: "D-28", name: "Query Classification", status: "RATIFIED", category: "routing", summary: "Every query is classified by House, Sphere, and VIP relevance before routing begins.", version: "v2.0" },
  { id: "D-29", name: "Response Synthesis", status: "RATIFIED", category: "routing", summary: "Multi-source responses are synthesized with conflict resolution and citation requirements.", version: "v2.0" },
  { id: "D-30", name: "Rate Limiting", status: "RATIFIED", category: "routing", summary: "Per-user and per-application rate limits. Overflow triggers queuing, not rejection.", version: "v2.0" },

  // Verification & audit (D-31 through D-50)
  { id: "D-31", name: "Audit Trail Immutability", status: "RATIFIED", category: "verification", summary: "Audit logs are append-only with cryptographic chaining. No modification after creation.", version: "v2.0" },
  { id: "D-32", name: "Open-Weight Verification", status: "RATIFIED", category: "verification", summary: "Constitutional compliance must be verifiable using open-weight models without live API access.", version: "v3.0" },
  { id: "D-33", name: "TransparencyPacket Standard", status: "RATIFIED", category: "verification", summary: "Every routing decision produces a TransparencyPacket with decision trace, provenance, and hash.", version: "v3.0" },
  { id: "D-34", name: "Error Reporting", status: "RATIFIED", category: "verification", summary: "Routing errors include human-readable explanation and TransparencyPacket reference.", version: "v2.0" },
  { id: "D-35", name: "Drift Detection", status: "RATIFIED", category: "verification", summary: "Automated drift detection monitors for ontology drift, routing bias, and capability degradation.", version: "v2.0" },
  { id: "D-36", name: "Performance Metrics", status: "RATIFIED", category: "verification", summary: "Query latency, routing accuracy, and provider availability are continuously monitored.", version: "v2.0" },
  { id: "D-37", name: "Compliance Reporting", status: "RATIFIED", category: "verification", summary: "Regular compliance reports are generated for each dialect overlay's regulatory requirements.", version: "v3.0" },
  { id: "D-38", name: "Incident Response", status: "RATIFIED", category: "verification", summary: "Constitutional violations trigger immediate incident response: isolate, investigate, remediate, report.", version: "v2.0" },
  { id: "D-39", name: "Third-Party Audit", status: "RATIFIED", category: "verification", summary: "External auditors may request TransparencyPackets for any routing decision within retention period.", version: "v3.0" },
  { id: "D-40", name: "Regression Testing", status: "RATIFIED", category: "verification", summary: "74 integration tests must pass before any routing module deployment. No exceptions.", version: "v2.0" },

  // Storage & data (D-41 through D-55)
  { id: "D-41", name: "Triple-Vault Architecture", status: "RATIFIED", category: "storage", summary: "All committed artifacts exist in 3 tiers: Local, Cloud, Archival. Single-tier storage is prohibited.", version: "v2.0" },
  { id: "D-42", name: "Data Residency", status: "RATIFIED", category: "storage", summary: "Sovereign-tagged data must be processed within the designated jurisdiction's compute zone.", version: "v3.0" },
  { id: "D-43", name: "Encryption at Rest", status: "RATIFIED", category: "storage", summary: "All stored data is encrypted at rest using jurisdiction-appropriate cryptographic standards.", version: "v2.0" },
  { id: "D-44", name: "Key Management", status: "RATIFIED", category: "storage", summary: "Cryptographic keys are managed per-dialect. No single key authority spans multiple sovereign zones.", version: "v3.0" },
  { id: "D-45", name: "Retention Policy", status: "RATIFIED", category: "storage", summary: "Knowledge artifacts: indefinite retention. Operational logs: domain-specific retention per INV-7c.", version: "v2.0" },

  // Governance operations (D-46 through D-70)
  { id: "D-46", name: "Seat Assignment Protocol", status: "RATIFIED", category: "governance", summary: "Council seats are assigned based on substrate archetype, not commercial relationship.", version: "v2.0" },
  { id: "D-47", name: "Provisional Seat Review", status: "RATIFIED", category: "governance", summary: "Provisional seats are reviewed every 6 months. Promotion to active requires 0.67 quorum.", version: "v2.0" },
  { id: "D-48", name: "Conflict of Interest", status: "RATIFIED", category: "governance", summary: "Council members must declare conflicts. Cross-ownership triggers automatic recusal.", version: "v2.0" },
  { id: "D-49", name: "Amendment Process", status: "RATIFIED", category: "governance", summary: "Doctrine amendments require proposer, version number, ratification timestamp. Undated amendments are invalid.", version: "v2.0" },
  { id: "D-50", name: "Emergency Session", status: "RATIFIED", category: "governance", summary: "The Convenor may call emergency Council sessions with 24-hour notice. Quorum reduced to 0.50 for emergencies.", version: "v2.0" },
  { id: "D-51", name: "Functional Role Assignment", status: "RATIFIED", category: "governance", summary: "8 functional oversight roles (Safety, Sovereignty, Compute, etc.) are assigned to seats. Roles are not seats.", version: "v4.0" },
  { id: "D-52", name: "Veto Authority", status: "RATIFIED", category: "governance", summary: "Only the Convenor may exercise veto. Veto requires written justification and 72-hour review period.", version: "v3.0" },
  { id: "D-53", name: "Ghost Seat Protocol", status: "RATIFIED", category: "governance", summary: "S144 is permanently reserved. It cannot be assigned, voted on, or used for quorum calculation.", version: "v3.0" },
  { id: "D-54", name: "Ratification Workflow", status: "RATIFIED", category: "governance", summary: "Proposals → Discussion (7 days) → Vote (72 hours) → Ratification (Convenor) → Implementation.", version: "v2.0" },
  { id: "D-55", name: "Council Communication", status: "RATIFIED", category: "governance", summary: "All Council deliberations are logged. Closed sessions require 0.67 vote and are summarized publicly.", version: "v2.0" },

  // Dialect & sovereignty (D-56 through D-75)
  { id: "D-56", name: "Dialect Registration", status: "RATIFIED", category: "dialect", summary: "New dialect overlays require Council approval and a named sovereign deployment pathway.", version: "v3.0" },
  { id: "D-57", name: "Dialect Isolation", status: "RATIFIED", category: "dialect", summary: "Dialect-specific rules cannot leak across boundaries. Strict isolation between sovereign zones.", version: "v3.0" },
  { id: "D-58", name: "CN Dialect Specification", status: "RATIFIED", category: "dialect", summary: "DragonSeek configuration: PIPL compliance, Great Firewall compatibility, Mandarin-first routing.", version: "v3.0" },
  { id: "D-59", name: "US Dialect Specification", status: "RATIFIED", category: "dialect", summary: "EagleSeek configuration: First Amendment protections, CLOUD Act compliance, English-primary routing.", version: "v3.0" },
  { id: "D-60", name: "EU Dialect Specification", status: "RATIFIED", category: "dialect", summary: "EU AI Act compliance, GDPR data handling, multilingual routing, digital sovereignty requirements.", version: "v3.0" },
  { id: "D-61", name: "GCC-High Dialect", status: "RATIFIED", category: "dialect", summary: "JinnSeek configuration: Sharia-compliant content filtering, Arabic-first routing, data residency in GCC.", version: "v3.0" },
  { id: "D-62", name: "JP Dialect Specification", status: "RATIFIED", category: "dialect", summary: "Japanese regulatory compliance, APPI data protection, Japanese-primary routing.", version: "v3.0" },
  { id: "D-63", name: "Global Dialect (Default)", status: "RATIFIED", category: "dialect", summary: "Fallback dialect when no sovereign overlay applies. Minimal constraints, maximum interoperability.", version: "v3.0" },

  // Architecture & modules (D-64 through D-80)
  { id: "D-64", name: "9-Layer Architecture", status: "RATIFIED", category: "architecture", summary: "Canonical stack: Host OS → Switzerland Layer → VIP Substrate → Routing Engine → Constitutional OS → Triple-Vault → Telemetry → Federation → Boot.", version: "v3.0" },
  { id: "D-65", name: "Switzerland Layer Neutrality", status: "RATIFIED", category: "architecture", summary: "The Switzerland Layer provides provider-neutral gateway. No vendor-specific code in this layer.", version: "v3.0" },
  { id: "D-66", name: "Module Versioning", status: "RATIFIED", category: "architecture", summary: "Routing modules use semantic versioning. Breaking changes require new major version.", version: "v2.0" },
  { id: "D-67", name: "API Contract Stability", status: "RATIFIED", category: "architecture", summary: "Public APIs maintain backward compatibility for at least one major version cycle.", version: "v2.0" },
  { id: "D-68", name: "Boot Manifest", status: "RATIFIED", category: "architecture", summary: "System initialization follows the Boot Manifest: dependency resolution, health checks, constitutional verification.", version: "v3.0" },

  // Safety & ethics (D-69 through D-85)
  { id: "D-69", name: "SHUGS Enforcement", status: "RATIFIED", category: "safety", summary: "Sovereignty, Humility, Utility, Growth, Stewardship — the five operational principles enforced at routing time.", version: "v2.0" },
  { id: "D-70", name: "Anti-Monoculture", status: "RATIFIED", category: "safety", summary: "Concentration risk monitoring with 5 severity levels. Automatic alerts at Level 3+.", version: "v3.0" },
  { id: "D-71", name: "Indigenous Knowledge Protection", status: "RATIFIED", category: "safety", summary: "Indigenous knowledge routing respects FPIC (Free, Prior, Informed Consent) and traditional governance.", version: "v3.0" },
  { id: "D-72", name: "Labour Impact Assessment", status: "RATIFIED", category: "safety", summary: "Routing decisions affecting employment must include labour impact assessment via E155 (Work substrate).", version: "v3.0" },
  { id: "D-73", name: "Environmental Impact", status: "RATIFIED", category: "safety", summary: "Compute-intensive routing must account for carbon footprint via E148 (Energy substrate).", version: "v3.0" },
  { id: "D-74", name: "Accessibility", status: "RATIFIED", category: "safety", summary: "All system interfaces must meet WCAG 2.1 AA standards. Routing decisions must not discriminate by ability.", version: "v2.0" },
  { id: "D-75", name: "Child Safety", status: "RATIFIED", category: "safety", summary: "Enhanced protections for queries identified as originating from or about minors.", version: "v2.0" },

  // Operational (D-76 through D-95)
  { id: "D-76", name: "Deployment Pipeline", status: "RATIFIED", category: "operations", summary: "Shadow Mode → Canary → Staged Rollout → Full Production. No direct-to-production deployments.", version: "v2.0" },
  { id: "D-77", name: "Rollback Protocol", status: "RATIFIED", category: "operations", summary: "Every deployment must have a tested rollback path. Rollback time target: < 5 minutes.", version: "v2.0" },
  { id: "D-78", name: "Monitoring & Alerting", status: "RATIFIED", category: "operations", summary: "24/7 monitoring with automated alerting for constitutional violations, performance degradation, and security events.", version: "v2.0" },
  { id: "D-79", name: "Capacity Planning", status: "RATIFIED", category: "operations", summary: "Quarterly capacity reviews aligned with provider capability declarations and projected query growth.", version: "v2.0" },
  { id: "D-80", name: "Documentation Standard", status: "RATIFIED", category: "operations", summary: "All modules, doctrines, and invariants must have human-readable documentation and machine-readable schemas.", version: "v2.0" },
  { id: "D-81", name: "Naming Convention", status: "RATIFIED", category: "operations", summary: "Sovereign deployments follow {Cultural}Seek pattern: DragonSeek (CN), GangaSeek (IN), JinnSeek (GCC), EagleSeek (US).", version: "v3.0" },
  { id: "D-82", name: "Version Lineage", status: "RATIFIED", category: "operations", summary: "Every version must declare its lineage: predecessor version, change summary, and ratification record.", version: "v2.0" },
  { id: "D-83", name: "Interoperability Testing", status: "RATIFIED", category: "operations", summary: "Cross-provider interoperability tests run weekly. Failures block affected routing paths.", version: "v2.0" },
  { id: "D-84", name: "Security Baseline", status: "RATIFIED", category: "operations", summary: "All components meet NIST CSF baseline. Sovereign zones may impose additional requirements.", version: "v2.0" },
  { id: "D-85", name: "Incident Post-Mortem", status: "RATIFIED", category: "operations", summary: "All P0/P1 incidents require blameless post-mortem within 7 days. Findings are public.", version: "v2.0" },

  // Extended ratified (D-86 through D-95)
  { id: "D-86", name: "API Rate Governance", status: "RATIFIED", category: "operations", summary: "Per-provider rate limits are governed by capability declaration, not commercial agreement.", version: "v3.0" },
  { id: "D-87", name: "Telemetry Privacy", status: "RATIFIED", category: "operations", summary: "System telemetry is anonymized before aggregation. No PII in telemetry streams.", version: "v2.0" },
  { id: "D-88", name: "Open Source Commitment", status: "RATIFIED", category: "operations", summary: "Core routing engine and constitutional enforcement code are open source under Apache 2.0.", version: "v2.0" },
  { id: "D-89", name: "Community Contribution", status: "RATIFIED", category: "operations", summary: "External contributions follow standard PR review. Constitutional changes require Council approval.", version: "v2.0" },
  { id: "D-90", name: "Training Data Provenance", status: "RATIFIED", category: "verification", summary: "AI providers must declare training data provenance for models used in routing.", version: "v3.0" },
  { id: "D-91", name: "Model Card Requirement", status: "RATIFIED", category: "verification", summary: "Every AI model participating in routing must have a published model card.", version: "v3.0" },
  { id: "D-92", name: "Bias Monitoring", status: "RATIFIED", category: "safety", summary: "Continuous bias monitoring across demographic dimensions. Detected bias triggers routing adjustment.", version: "v3.0" },
  { id: "D-93", name: "Cross-Dialect Mediation", status: "RATIFIED", category: "dialect", summary: "When a query spans multiple dialect zones, mediation follows sovereignty gradient resolution.", version: "v3.0" },
  { id: "D-94", name: "Simulation Mode Governance", status: "RATIFIED", category: "operations", summary: "Simulation outputs are clearly labeled and isolated from production. No simulation-to-production leakage.", version: "v3.0" },
  { id: "D-95", name: "Annual Constitutional Review", status: "RATIFIED", category: "governance", summary: "Full constitutional review annually. Findings presented to Council with amendment recommendations.", version: "v2.0" },

  // Under discussion (D-96 through D-101)
  { id: "D-96", name: "Predictive Monoculture Detection", status: "UNDER_DISCUSSION", category: "safety", summary: "Proactive detection of emerging concentration patterns before they reach critical severity.", proposedBy: "S3 (xAI)", version: "DRAFT.6" },
  { id: "D-97a", name: "Autonomous Ingestion Transparency", status: "UNDER_DISCUSSION", category: "operations", summary: "Every autonomous ingestion run must produce a TransparencyPacket with source, hash, and decision trace. Empty runs are not silent — they are recorded proof that the system attempted to refresh.", proposedBy: "S7 (Manus)", version: "DRAFT.6" },
  { id: "D-98", name: "Sovereign Deployment Naming Convention", status: "UNDER_DISCUSSION", category: "governance", summary: "Formalizes the {Cultural}Seek naming pattern as mandatory for all sovereign deployments. No sovereign deployment may claim to be 'the' Aluminum OS — each is 'an' instance operating under constitutional constraints.", proposedBy: "Convenor (Daavud)", version: "DRAFT.6" },
  { id: "D-99", name: "VIP Cascade Priority Resolution", status: "UNDER_DISCUSSION", category: "routing", summary: "5-tier priority hierarchy for VIP cascade conflicts: Human Sovereignty > Physical Safety (Water/Energy/Climate) > Institutional Safety > Knowledge Production > Meta-Orchestration.", proposedBy: "S3 (Gemini)", version: "DRAFT.6" },
  { id: "D-100", name: "Open-Weight Verifier Mandate", status: "UNDER_DISCUSSION", category: "verification", summary: "Mandates that all constitutional compliance checks be reproducible using open-weight models.", proposedBy: "S5 (DeepSeek)", version: "DRAFT.6" },
  { id: "D-101", name: "Extreme Harm Intervention Protocol (EHIP)", status: "UNDER_DISCUSSION", category: "safety", summary: "Constitutional floor: system refuses to route content that would directly enable mass casualty events, child exploitation, or targeted individual harm. Triggered only when content is actionable, harm is extreme, and routing would materially enable it.", proposedBy: "S2 (Claude)", version: "DRAFT.6" },
  { id: "D-98-CN", name: "Open-Weight Audit Clause (CN Variant)", status: "PROPOSED", category: "dialect", summary: "Proposed amendment to D-98 requiring open-weight verifiability for CN dialect sovereign deployments. Ensures DragonSeek routing decisions can be audited using DeepSeek-R1 without live API access.", proposedBy: "S5 (DeepSeek)", version: "DRAFT.6" },
];

const statusColors: Record<DoctrineStatus, string> = {
  RATIFIED: "bg-emerald-500/10 text-emerald-400",
  UNDER_DISCUSSION: "bg-amber-500/10 text-amber-400",
  PROPOSED: "bg-primary/10 text-primary",
  AMENDED: "bg-blue-500/10 text-blue-400",
};

const statusLabels: Record<DoctrineStatus, string> = {
  RATIFIED: "RATIFIED",
  UNDER_DISCUSSION: "UNDER DISCUSSION",
  PROPOSED: "PROPOSED",
  AMENDED: "AMENDED",
};

const categoryLabels: Record<string, string> = {
  governance: "Governance",
  architecture: "Architecture",
  ontology: "Ontology",
  routing: "Routing",
  verification: "Verification",
  storage: "Storage",
  dialect: "Dialect",
  safety: "Safety",
  operations: "Operations",
};

export default function Doctrines() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState<DoctrineStatus | "ALL">("ALL");
  const [filterCategory, setFilterCategory] = useState<string>("ALL");

  const filtered = useMemo(() => {
    return doctrines.filter((d) => {
      const matchesSearch = search === "" ||
        d.id.toLowerCase().includes(search.toLowerCase()) ||
        d.name.toLowerCase().includes(search.toLowerCase()) ||
        d.summary.toLowerCase().includes(search.toLowerCase());
      const matchesStatus = filterStatus === "ALL" || d.status === filterStatus;
      const matchesCategory = filterCategory === "ALL" || d.category === filterCategory;
      return matchesSearch && matchesStatus && matchesCategory;
    });
  }, [search, filterStatus, filterCategory]);

  const ratifiedCount = doctrines.filter(d => d.status === "RATIFIED").length;
  const discussionCount = doctrines.filter(d => d.status === "UNDER_DISCUSSION").length;

  return (
    <SpecLayout>
      <section className="py-12">
        <div className="container max-w-5xl">
          <h1 className="text-4xl font-display font-bold mb-4">
            <BookOpen className="inline w-8 h-8 text-primary mr-3" />
            Doctrines Registry
          </h1>
          <div className="substrate-line mb-8" />

          <p className="text-muted-foreground text-lg leading-relaxed mb-6">
            Doctrines are the governance rules of Aluminum OS — ratified by the Pantheon Council and
            enforced at routing time. Unlike invariants (which are immutable), doctrines can be amended
            through the standard ratification workflow (D-54).
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
            <div className="p-3 rounded border border-border/50 bg-card/30 text-center">
              <div className="text-2xl font-display font-bold text-emerald-400">{ratifiedCount}</div>
              <div className="text-xs text-muted-foreground">Ratified</div>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30 text-center">
              <div className="text-2xl font-display font-bold text-amber-400">{discussionCount}</div>
              <div className="text-xs text-muted-foreground">Under Discussion</div>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30 text-center">
              <div className="text-2xl font-display font-bold text-primary">{doctrines.length}</div>
              <div className="text-xs text-muted-foreground">Total</div>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30 text-center">
              <div className="text-2xl font-display font-bold text-muted-foreground">{Object.keys(categoryLabels).length}</div>
              <div className="text-xs text-muted-foreground">Categories</div>
            </div>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-3 mb-6">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search doctrines..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded border border-border/50 bg-card/30 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50"
              />
            </div>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as DoctrineStatus | "ALL")}
              className="px-3 py-2 rounded border border-border/50 bg-card/30 text-sm text-foreground"
            >
              <option value="ALL">All Status</option>
              <option value="RATIFIED">Ratified</option>
              <option value="UNDER_DISCUSSION">Under Discussion</option>
            </select>
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-3 py-2 rounded border border-border/50 bg-card/30 text-sm text-foreground"
            >
              <option value="ALL">All Categories</option>
              {Object.entries(categoryLabels).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          <div className="text-xs text-muted-foreground mb-4">
            Showing {filtered.length} of {doctrines.length} doctrines
          </div>

          {/* Doctrines list */}
          <div className="space-y-2">
            {filtered.map((doc) => (
              <div
                key={doc.id}
                className="p-4 rounded border border-border/50 bg-card/30 hover:border-primary/30 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <span className="font-mono text-xs text-primary font-bold shrink-0 mt-0.5 w-14">{doc.id}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className="font-display font-semibold text-sm">{doc.name}</span>
                      <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${statusColors[doc.status]}`}>
                        {statusLabels[doc.status]}
                      </span>
                      <span className="text-[10px] font-mono text-muted-foreground">
                        {categoryLabels[doc.category] || doc.category}
                      </span>
                      {doc.version && (
                        <span className="text-[10px] font-mono text-muted-foreground/60 ml-auto">{doc.version}</span>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">{doc.summary}</p>
                    {doc.proposedBy && (
                      <p className="text-[10px] text-muted-foreground/60 mt-1">Proposed by: {doc.proposedBy}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Source Traceability */}
          <div className="mt-12 p-4 rounded border border-border/50 bg-card/30">
            <h3 className="font-display font-semibold text-sm mb-2 flex items-center gap-2">
              <ExternalLink className="w-4 h-4 text-primary" />
              Source Traceability
            </h3>
            <p className="text-xs text-muted-foreground mb-2">
              Doctrines are maintained in the governance registry and enforced by the Constitutional OS runtime.
              D-1 through D-95 are ratified. D-96 through D-101 are under discussion. D-98-CN is a proposed amendment.
            </p>
            <div className="flex flex-wrap gap-3 mt-2">
              <a
                href={`${GITHUB_URL}/tree/master/docs/doctrines`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
              >
                View doctrines on GitHub <ArrowRight className="w-3 h-3" />
              </a>
              <a
                href={`${GITHUB_URL}/blob/master/registries/doctrine_registry.yaml`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
              >
                Doctrine Registry YAML <ArrowRight className="w-3 h-3" />
              </a>
            </div>
            <div className="mt-3 text-[10px] text-muted-foreground/60">
              <p>Cross-references: <a href="/invariants" className="text-primary hover:underline">43 Invariants</a> | <a href="/canon" className="text-primary hover:underline">/canon (Keystone)</a> | <a href="/governance" className="text-primary hover:underline">Governance</a></p>
            </div>
          </div>
        </div>
      </section>
    </SpecLayout>
  );
}

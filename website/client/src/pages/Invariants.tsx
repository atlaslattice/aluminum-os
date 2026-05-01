import SpecLayout from "@/components/SpecLayout";
import { GITHUB_URL } from "@/lib/data";
import { ArrowRight, Shield, ExternalLink } from "lucide-react";
import { Link } from "wouter";

// Canonical 43 invariants: INV-0 through INV-39 (40 base) + INV-19 Water, INV-20 Neural, INV-21 Orbital
// Source: Build Plan v2.3, Constitutional OS v6.0.2
// Count model: 40 base + 3 domain-specific = 43. INV-7c is a sub-spec (listed for reference, not counted separately)
const invariants = [
  { id: "INV-0", name: "System Integrity", category: "core", description: "The ontological structure (12 Houses, 144 Spheres) cannot be altered without unanimous Council vote plus Convenor ratification.", severity: "ABSOLUTE" },
  { id: "INV-1", name: "Human Sovereignty", category: "core", description: "No AI system operating under Aluminum OS may override, circumvent, or diminish human decision-making authority. This invariant is absolute and cannot be suspended, amended, or overridden by any doctrine, vote, or emergency protocol.", severity: "ABSOLUTE" },
  { id: "INV-2", name: "Constitutional Supremacy", category: "core", description: "All doctrines, modules, and routing decisions must comply with the constitutional framework. Any conflict is resolved in favor of the constitution.", severity: "ABSOLUTE" },
  { id: "INV-3", name: "Multi-Vendor Requirement", category: "core", description: "No single AI provider may control more than 33% of active routing capacity at any time.", severity: "CRITICAL" },
  { id: "INV-4", name: "Transparency by Default", category: "governance", description: "All routing decisions must produce a TransparencyPacket (Doctrine 97-a) that can be audited offline.", severity: "CRITICAL" },
  { id: "INV-5", name: "Dialect Sovereignty", category: "governance", description: "Each ratified dialect overlay has jurisdiction over its domain. No dialect may override another's sovereign scope.", severity: "CRITICAL" },
  { id: "INV-6", name: "Provenance Chain", category: "governance", description: "Every knowledge claim must carry a provenance chain: source → transformation → current state. Broken chains trigger quarantine.", severity: "HIGH" },
  { id: "INV-7", name: "Zero Erasure", category: "storage", description: "No data committed to the Triple-Vault may be deleted. Superseded data is archived, never destroyed.", severity: "ABSOLUTE" },
  { id: "INV-7c", name: "Zero Erasure (Sub-spec)", category: "storage", description: "Clarification: INV-7 applies to committed knowledge artifacts. Operational logs may be rotated per retention policy. Counted as sub-spec, not separate invariant.", severity: "HIGH" },
  { id: "INV-8", name: "Quorum Requirement", category: "governance", description: "Council decisions require 0.67 quorum of active seats. Provisional seats vote but do not count toward quorum.", severity: "CRITICAL" },
  { id: "INV-9", name: "Convenor Tie-Break", category: "governance", description: "In case of tied Council votes, the Convenor (human) casts the deciding vote. This is the only circumstance where the Convenor's vote carries additional weight.", severity: "CRITICAL" },
  { id: "INV-10", name: "Adversarial Audit", category: "verification", description: "Every routing decision must be verifiable by at least one adversarial seat (S3 xAI or S6 OpenAI).", severity: "HIGH" },
  { id: "INV-11", name: "Open-Weight Verification", category: "verification", description: "Constitutional compliance must be independently verifiable using open-weight models (DeepSeek-R1) without live API access.", severity: "HIGH" },
  { id: "INV-12", name: "Cascade Determinism", category: "routing", description: "Given identical inputs, the VIP Cascade must produce identical routing decisions. Non-determinism triggers M111 Error-Mode.", severity: "CRITICAL" },
  { id: "INV-13", name: "Sphere Addressing", category: "ontology", description: "Every knowledge node must have a canonical address in the format H{n}-S{nnn}. Orphan nodes are prohibited.", severity: "HIGH" },
  { id: "INV-14", name: "VIP Precedence", category: "routing", description: "VIP Elements (E145-E156) take routing precedence over House-level classification when a query touches civilizational substrates.", severity: "HIGH" },
  { id: "INV-15", name: "Emergency Mode", category: "routing", description: "In Low-Power/Emergency compute zones, the system degrades gracefully: VIP cascade first, then core routing, then static fallback.", severity: "CRITICAL" },
  { id: "INV-16", name: "Anti-Concentration", category: "governance", description: "No single entity may hold more than 2 Council seats. Cross-ownership triggers automatic recusal.", severity: "CRITICAL" },
  { id: "INV-17", name: "Triple-Vault Storage", category: "storage", description: "All committed artifacts must exist in at least 3 storage tiers: Local, Cloud, and Archival. Single-tier storage is prohibited.", severity: "ABSOLUTE" },
  { id: "INV-18", name: "Doctrine Versioning", category: "governance", description: "Every doctrine amendment must carry a version number, proposer, and ratification timestamp. Undated doctrines are invalid.", severity: "HIGH" },
  { id: "INV-19", name: "Water Sovereignty", category: "domain", description: "Water-related routing decisions must account for indigenous water rights, ecological flow requirements, and transboundary obligations before commercial optimization.", severity: "CRITICAL" },
  { id: "INV-20", name: "Neural Sovereignty", category: "domain", description: "Brain-computer interface and neural data routing must enforce informed consent, reversibility, and cognitive liberty protections.", severity: "ABSOLUTE" },
  { id: "INV-21", name: "Orbital Sovereignty", category: "domain", description: "Space infrastructure routing must comply with the Outer Space Treaty, debris mitigation standards, and equitable spectrum allocation.", severity: "HIGH" },
  { id: "INV-22", name: "Dialect Isolation", category: "routing", description: "Dialect-specific routing rules cannot leak across dialect boundaries. CN dialect rules do not affect US routing and vice versa.", severity: "CRITICAL" },
  { id: "INV-23", name: "Module Idempotency", category: "routing", description: "Routing modules must be idempotent: repeated execution with the same input produces the same output without side effects.", severity: "HIGH" },
  { id: "INV-24", name: "Graceful Degradation", category: "routing", description: "If a Council seat becomes unavailable, routing continues with remaining seats. No single seat failure may halt the system.", severity: "CRITICAL" },
  { id: "INV-25", name: "Schema Migration Safety", category: "ontology", description: "Ontology schema changes must be backward-compatible. Breaking changes require a new major version and Council supermajority.", severity: "HIGH" },
  { id: "INV-26", name: "Audit Trail Immutability", category: "verification", description: "Audit logs cannot be modified after creation. Append-only storage with cryptographic chaining.", severity: "ABSOLUTE" },
  { id: "INV-27", name: "Cross-Seat Communication", category: "routing", description: "Inter-seat communication must use the Federation Bridge (E145.03). Direct seat-to-seat channels are prohibited.", severity: "HIGH" },
  { id: "INV-28", name: "Capability Declaration", category: "routing", description: "Every AI provider must declare its capability matrix before participating in routing. Undeclared capabilities are excluded.", severity: "HIGH" },
  { id: "INV-29", name: "Constitutional Amendment Threshold", category: "governance", description: "Amending invariants requires 0.90 supermajority of all seats (including provisional) plus Convenor ratification.", severity: "ABSOLUTE" },
  { id: "INV-30", name: "Harm Intervention", category: "governance", description: "The Convenor may invoke EHIP (Doctrine 101) to suspend any routing decision that poses extreme harm. Suspension is immediate; review follows within 72 hours.", severity: "ABSOLUTE" },
  { id: "INV-31", name: "Knowledge Freshness", category: "ontology", description: "Knowledge claims older than their domain's refresh cycle must be flagged as potentially stale. Refresh cycles are domain-specific.", severity: "MEDIUM" },
  { id: "INV-32", name: "Sovereign Data Residency", category: "routing", description: "Data tagged with a sovereign dialect must be processed within that jurisdiction's compute zone. Cross-border routing requires explicit consent.", severity: "CRITICAL" },
  { id: "INV-33", name: "Model Diversity", category: "routing", description: "For any given query class, at least 2 distinct model lineages must be available for routing. Single-lineage routing triggers a warning.", severity: "HIGH" },
  { id: "INV-34", name: "Constitutional Boot", category: "core", description: "The system must verify constitutional integrity on every boot. Failed verification prevents system start.", severity: "ABSOLUTE" },
  { id: "INV-35", name: "Simulation Isolation", category: "routing", description: "Shadow Mode and Simulation Mode outputs must never be served as production responses. Strict isolation between simulation and production.", severity: "CRITICAL" },
  { id: "INV-36", name: "Rate Limiting", category: "routing", description: "No single user or application may consume more than its allocated routing capacity. Overflow triggers queuing, not rejection.", severity: "MEDIUM" },
  { id: "INV-37", name: "Error Transparency", category: "verification", description: "Routing errors must be reported to the user with a human-readable explanation and the TransparencyPacket reference.", severity: "HIGH" },
  { id: "INV-38", name: "Backward Compatibility", category: "routing", description: "New routing modules must support the previous version's API contract for at least one major version cycle.", severity: "HIGH" },
  { id: "INV-39", name: "Council Seat Rotation", category: "governance", description: "Provisional seats are reviewed every 6 months. Active seats are reviewed annually. No seat is permanent except S144 (Ghost Seat).", severity: "MEDIUM" },
];

const categories = [
  { key: "core", label: "Core (System)", color: "text-red-400" },
  { key: "governance", label: "Governance", color: "text-amber-400" },
  { key: "routing", label: "Routing", color: "text-primary" },
  { key: "ontology", label: "Ontology", color: "text-emerald-400" },
  { key: "storage", label: "Storage", color: "text-blue-400" },
  { key: "verification", label: "Verification", color: "text-purple-400" },
  { key: "domain", label: "Domain-Specific", color: "text-cyan-400" },
];

const severityColors: Record<string, string> = {
  ABSOLUTE: "bg-red-500/10 text-red-400",
  CRITICAL: "bg-amber-500/10 text-amber-400",
  HIGH: "bg-primary/10 text-primary",
  MEDIUM: "bg-muted text-muted-foreground",
};

export default function Invariants() {
  return (
    <SpecLayout>
      <section className="py-12">
        <div className="container max-w-5xl">
          <h1 className="text-4xl font-display font-bold mb-4">
            <Shield className="inline w-8 h-8 text-primary mr-3" />
            43 Constitutional Invariants
          </h1>
          <div className="substrate-line mb-8" />

          <p className="text-muted-foreground text-lg leading-relaxed mb-6">
            Invariants are constitutional constraints that <strong className="text-foreground">cannot be overridden</strong> by
            any doctrine, vote, or emergency protocol — except through the amendment process defined in INV-29
            (0.90 supermajority + Convenor ratification). They form the immutable foundation of the Aluminum OS
            governance layer.
          </p>

          <div className="p-4 rounded border border-amber-500/30 bg-amber-500/5 mb-8 text-sm text-amber-300/80">
            <strong className="text-amber-400">Counting Note:</strong> 40 base invariants (INV-0 through INV-39) +
            3 domain-specific (INV-19 Water, INV-20 Neural, INV-21 Orbital) = 43 total. INV-7c is a sub-specification
            of INV-7, not a separate invariant.
          </div>

          {/* Category legend */}
          <div className="flex flex-wrap gap-3 mb-8">
            {categories.map((cat) => (
              <span key={cat.key} className={`text-xs font-mono px-2 py-1 rounded border border-border/50 ${cat.color}`}>
                {cat.label} ({invariants.filter(i => i.category === cat.key).length})
              </span>
            ))}
          </div>

          {/* Invariants list */}
          <div className="space-y-2">
            {invariants.map((inv) => {
              const cat = categories.find(c => c.key === inv.category);
              return (
                <div
                  key={inv.id}
                  className="p-4 rounded border border-border/50 bg-card/30 hover:border-primary/30 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <span className="font-mono text-xs text-primary font-bold shrink-0 mt-0.5 w-16">{inv.id}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <span className="font-display font-semibold text-sm">{inv.name}</span>
                        <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${severityColors[inv.severity]}`}>
                          {inv.severity}
                        </span>
                        {cat && (
                          <span className={`text-[10px] font-mono ${cat.color}`}>
                            {cat.label}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-muted-foreground leading-relaxed">{inv.description}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Source Traceability */}
          <div className="mt-12 p-4 rounded border border-border/50 bg-card/30">
            <h3 className="font-display font-semibold text-sm mb-2 flex items-center gap-2">
              <ExternalLink className="w-4 h-4 text-primary" />
              Source Traceability
            </h3>
            <p className="text-xs text-muted-foreground mb-2">
              Invariants are defined in the Constitutional OS codebase and enforced at runtime.
              40 base (INV-0 through INV-39) + 3 domain-specific (INV-19 Water, INV-20 Neural, INV-21 Orbital) = 43 total.
              INV-7c is a sub-specification of INV-7, not a separate invariant.
            </p>
            <div className="flex flex-wrap gap-3 mt-2">
              <a
                href={`${GITHUB_URL}/tree/master/src/invariants`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
              >
                View invariant enforcement code on GitHub <ArrowRight className="w-3 h-3" />
              </a>
              <a
                href={`${GITHUB_URL}/blob/master/registries/invariant_registry.yaml`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
              >
                Invariant Registry YAML <ArrowRight className="w-3 h-3" />
              </a>
            </div>
            <div className="mt-3 text-[10px] text-muted-foreground/60">
              <p>Cross-references: <a href="/doctrines" className="text-primary hover:underline">Doctrines Registry</a> | <a href="/canon" className="text-primary hover:underline">/canon (Keystone)</a> | <a href="/governance" className="text-primary hover:underline">Governance</a></p>
            </div>
          </div>
        </div>
      </section>
    </SpecLayout>
  );
}

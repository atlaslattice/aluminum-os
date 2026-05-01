import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import { Link } from "wouter";
import { ArrowRight } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.08 } },
};

const layers = [
  {
    id: 1,
    name: "Host OS",
    description: "The underlying operating system — Windows, macOS, Linux, Android, iOS. Aluminum OS sits above this layer, never replacing it.",
    detail: "Provider-neutral. No lock-in to any hardware or OS vendor. The lattice runs wherever compute exists.",
    link: null,
  },
  {
    id: 2,
    name: "Switzerland Layer",
    description: "One-click federation and provider-neutral gateway. All frontier AI models connect here without privileging any single vendor.",
    detail: "Implements INV-7c (47%/60% provider cap), ensuring no single model or company dominates routing decisions.",
    link: "/routing",
  },
  {
    id: 3,
    name: "VIP Substrate Cascade",
    description: "12 VIP Elements (E145–E156) — civilizational substrates that cross-cut all Houses. Water, Energy, AI, Governance, Security, Economics, Compute, Provenance, Education, Health, Climate, Meta-Orchestrator.",
    detail: "The cascade determines routing priority: when a query touches multiple substrates, the cascade resolves which VIP takes precedence based on sovereignty gradient and constitutional invariants.",
    link: "/elements",
  },
  {
    id: 4,
    name: "Constitutional Enforcement",
    description: "43 invariants that cannot be overridden. Human sovereignty (INV-1) is absolute. Every routing decision passes through constitutional validation.",
    detail: "Implements the 5-tier VIP Cascade Priority: Safety → Sovereignty → Governance → Provenance → Performance.",
    link: "/governance",
  },
  {
    id: 5,
    name: "Dialect Overlay",
    description: "6 ratified dialect profiles (US, EU, CN, GCC-High, JP, Global) + 2 planned (IN, SA). Each dialect shapes how content is filtered, routed, and presented.",
    detail: "Dialects compose five dimensions: regulatory, cultural, compute, risk, and industry. CN dialect is fully specified; US is partial.",
    link: "/dialects",
  },
  {
    id: 6,
    name: "Sovereignty Vector",
    description: "Six-dimensional sovereignty assessment: legal, data, compute, economic, provenance, operational. Every routing decision carries a sovereignty score.",
    detail: "Enables sovereign deployment pathways: DragonSeek (CN), GangaSeek (IN), JinnSeek (GCC), EagleSeek (US). Each pathway enforces jurisdiction-specific constraints.",
    link: "/sovereignty",
  },
  {
    id: 7,
    name: "Routing Engine",
    description: "~100 compute modules implementing the core cascade (M3), substrate cascade, dialect-bound routing, and provider capability matrix.",
    detail: "Core cascade: COMPLETE. Substrate cascade: IN SPEC. M111 Error-Mode Routing provides graceful degradation when providers fail.",
    link: "/routing",
  },
  {
    id: 8,
    name: "Provenance & Audit",
    description: "Every decision is traceable. Model lineage, provider lineage, evidence lineage, compute zone, timestamp, and spec version are recorded.",
    detail: "Open-weight verifiable: DeepSeek-R1 can deterministically replay and verify routing decisions without live API access.",
    link: "/provenance",
  },
  {
    id: 9,
    name: "Ontology Graph (12×12 Lattice)",
    description: "12 Houses × 12 Spheres (144 total) with ~499 enumerated sub-spheres. The knowledge substrate that makes cross-domain discovery a graph traversal.",
    detail: "Every node has a canonical address. Adjacency is encoded at schema time, making novel-insight discovery cheap.",
    link: "/lattice",
  },
];

export default function Layers() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">9-Layer Architecture</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Aluminum OS is organized as a 9-layer stack. Each layer has a single responsibility,
            clear interfaces, and constitutional constraints. No layer can override the one above it.
          </p>
        </motion.div>

        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-sm font-mono text-primary uppercase tracking-wider mb-4">How to Read This</h2>
          <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">
            Layers are numbered bottom-up (Layer 1 = Host OS, Layer 9 = Ontology Graph). Higher layers
            depend on lower layers but never bypass them. Constitutional enforcement (Layer 4) sits
            above the routing substrate, meaning every routing decision must pass constitutional validation
            before reaching the user.
          </p>
        </motion.div>

        {/* Architecture Stack */}
        <motion.div variants={fadeUp} className="space-y-2">
          {[...layers].reverse().map((layer, idx) => (
            <motion.div
              key={layer.id}
              variants={fadeUp}
              className="group relative"
            >
              <div className={`p-5 rounded border transition-all ${
                idx === 0
                  ? "border-primary/40 bg-primary/5"
                  : "border-border/50 bg-card/30 hover:border-primary/30"
              }`}>
                <div className="flex items-start gap-4">
                  <div className="shrink-0 w-10 h-10 rounded flex items-center justify-center bg-primary/10 text-primary font-mono text-sm font-bold">
                    L{layer.id}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <h3 className="font-display font-semibold">{layer.name}</h3>
                      {layer.link && (
                        <Link
                          href={layer.link}
                          className="text-[10px] font-mono text-primary hover:underline flex items-center gap-1"
                        >
                          Details <ArrowRight className="w-3 h-3" />
                        </Link>
                      )}
                    </div>
                    <p className="text-sm text-muted-foreground mb-2">{layer.description}</p>
                    <p className="text-xs text-muted-foreground/70 italic">{layer.detail}</p>
                  </div>
                </div>
              </div>
              {idx < layers.length - 1 && (
                <div className="absolute left-[2.25rem] -bottom-2 w-px h-2 bg-border/50" />
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* Schema Block */}
        <motion.div variants={fadeUp} className="mt-12">
          <h2 className="text-lg font-display font-semibold mb-4">Layer Dependency Rule</h2>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground">
            <pre>{`// Constitutional invariant: layer dependency is strictly upward
// No layer may bypass a layer above it in the stack
// INV-1: Human sovereignty is absolute (Layer 4 cannot be overridden)
// INV-7c: No single provider > 47% of routing decisions (Layer 2)

layer_dependency_rule: {
  direction: "bottom-up",
  bypass: "forbidden",
  override: "constitutional_only",
  audit: "every_decision_logged"
}`}</pre>
          
          {/* Source Traceability */}
          <div className="mt-16 pt-8 border-t border-border/30">
            <h3 className="text-sm font-mono text-muted-foreground/60 mb-3">Source Traceability</h3>
            <div className="flex flex-wrap gap-3">
              <a href={`${GITHUB_URL}/blob/master/docs/architecture/SOURCE_OF_TRUTH.md`} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ SOURCE_OF_TRUTH.md</a>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ GitHub Repository</a>
            </div>
          </div>
</div>
        </motion.div>
      </motion.div>
    </SpecLayout>
  );
}

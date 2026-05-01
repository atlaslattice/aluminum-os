import { motion } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";
import { ROUTING_IMAGE, routingModules, routingTable, dispatchOrder, authoritativePairs, crossVipPatterns, lccMapping, grokSemanticElements, GITHUB_URL } from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Routing() {
  const structural = routingModules.filter((m) => m.layer === "structural");
  const runtime = routingModules.filter((m) => m.layer === "runtime");

  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-6xl">
          {/* Hero */}
          <div className="relative rounded-lg overflow-hidden mb-12">
            <img src={ROUTING_IMAGE} alt="Routing Pack" className="w-full h-48 object-cover opacity-30" />
            <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent" />
            <div className="absolute inset-0 flex items-center p-8">
              <motion.div initial="hidden" animate="visible" variants={fadeUp}>
                <h1 className="text-4xl font-display font-bold mb-2">
                  <span className="text-gradient-teal">Element 145 Routing Pack</span>
                </h1>
                <p className="text-muted-foreground max-w-xl">
                  22 Python files across ~12 conceptual modules governing how queries traverse the lattice.
                  From schema validation to constitutional enforcement to live activation.
                </p>
              </motion.div>
            </div>
          </div>

          {/* Dispatch Order */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Query Dispatch Order</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              When a query enters the lattice, it passes through these stages in order.
              Each stage is a constitutional checkpoint — not a filter.
            </p>
            <div className="space-y-2">
              {dispatchOrder.map((step) => (
                <div key={step.vip} className="flex items-center gap-4 p-3 rounded border border-border/50 bg-card/30">
                  <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-0.5 rounded w-8 text-center">{step.position}</span>
                  <span className="font-mono text-xs text-accent w-12">{step.vip}</span>
                  <span className="text-sm text-foreground flex-1">{step.name}</span>
                  <span className="text-[10px] text-muted-foreground">{step.note}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Routing Table */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Seat Routing Table</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              Each council seat has a primary domain and authoritative VIP element for routing dispatch.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border/50">
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Domain</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Primary</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Secondary</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Notes</th>
                  </tr>
                </thead>
                <tbody className="text-muted-foreground">
                  {routingTable.map((entry) => (
                    <tr key={entry.domain} className="border-b border-border/30 hover:bg-card/30">
                      <td className="py-2 px-3 text-xs font-semibold text-foreground">{entry.domain}</td>
                      <td className="py-2 px-3 text-xs font-mono text-primary">{entry.primary}</td>
                      <td className="py-2 px-3 text-xs">{entry.secondary}</td>
                      <td className="py-2 px-3 text-xs text-muted-foreground">{entry.notes}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>

          {/* Authoritative Pairs */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Authoritative Pairs</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              Each VIP element has an authoritative seat pair — primary and secondary — for routing arbitration.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {authoritativePairs.map((pair) => (
                <div key={pair.domain} className="p-4 rounded border border-border/50 bg-card/20">
                  <div className="font-semibold text-sm text-foreground mb-2">{pair.domain}</div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-primary">{pair.houseHome}</span>
                    <span className="text-[10px] text-muted-foreground">↔</span>
                    <span className="text-xs font-mono text-accent">{pair.vipSubstrate}</span>
                  </div>
                  <p className="text-[10px] text-muted-foreground">{pair.note}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Structural Modules */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Structural Modules</h2>
            <div className="substrate-line mb-6" />
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {structural.map((mod) => (
                <div key={mod.id} className="p-4 rounded border border-border/50 bg-card/20">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-0.5 rounded">{mod.id}</span>
                    <span className="font-display font-semibold text-sm">{mod.name}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{mod.description}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Runtime Modules */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Runtime Modules</h2>
            <div className="substrate-line mb-6" />
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {runtime.map((mod) => (
                <div key={mod.id} className="p-4 rounded border border-accent/30 bg-accent/5">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-mono text-xs text-accent bg-accent/10 px-2 py-0.5 rounded">{mod.id}</span>
                    <span className="font-display font-semibold text-sm">{mod.name}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{mod.description}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Cross-VIP Intersection Patterns */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Cross-VIP Intersection Patterns</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              When a query triggers multiple VIP elements simultaneously, these intersection patterns
              define how dual-routing resolves. Each pattern is a constitutional rule, not a heuristic.
            </p>
            <div className="space-y-2">
              {crossVipPatterns.map((p) => (
                <div key={p.pattern} className="p-4 rounded border border-border/50 bg-card/20">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-display font-semibold text-sm text-foreground">{p.pattern}</span>
                    <span className="font-mono text-[10px] text-primary bg-primary/10 px-2 py-0.5 rounded">{p.vips}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">{p.resolution}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* LCC Cross-Reference Mapping */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">LCC Cross-Reference (21/21)</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              All 21 Library of Congress Classification classes are routed. LCC coverage is the empirical
              floor — it confirms the Lattice has not missed any domain that organized human knowledge
              production has discovered. LCC is a retrieval-by-keyword index; the Lattice is a
              retrieval-by-substrate graph. Coverage parity is the validation criterion; structural
              difference is the value proposition.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border/50">
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">LCC</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Name</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Primary Route</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Secondary</th>
                  </tr>
                </thead>
                <tbody className="text-muted-foreground">
                  {lccMapping.map((lcc) => (
                    <tr key={lcc.lccClass} className="border-b border-border/30 hover:bg-card/30">
                      <td className="py-2 px-3 text-xs font-mono font-bold text-foreground">{lcc.lccClass}</td>
                      <td className="py-2 px-3 text-xs">{lcc.name}</td>
                      <td className="py-2 px-3 text-xs font-mono text-primary">{lcc.primaryRoute}</td>
                      <td className="py-2 px-3 text-xs font-mono">{lcc.secondaryRoute}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>

          {/* Grok S3 12-Semantic-Element Routing Layer */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Grokverse: 12-Semantic-Element Routing Layer</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              Grok S3 (Grokverse) introduces 12 semantic routing Elements that operate as an abstraction
              layer above the 8 ontological VIPs (E145-E152). The 8 VIPs remain the canonical ontological
              primitives; the 12 Elements are the canonical routing primitives. Status: PROVISIONAL
              pending Council ratification.
            </p>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border/50">
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Element</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Description</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Closest VIP</th>
                    <th className="text-left py-2 px-3 font-mono text-xs text-primary">Status</th>
                  </tr>
                </thead>
                <tbody className="text-muted-foreground">
                  {grokSemanticElements.map((el) => (
                    <tr key={el.name} className="border-b border-border/30 hover:bg-card/30">
                      <td className="py-2 px-3 text-xs font-mono font-bold text-foreground">{el.name}</td>
                      <td className="py-2 px-3 text-xs">{el.description}</td>
                      <td className="py-2 px-3 text-xs font-mono text-accent">{el.closestVip}</td>
                      <td className="py-2 px-3">
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                          el.reconciliation.startsWith("COMPATIBLE") ? "bg-emerald-500/10 text-emerald-400" :
                          el.reconciliation.startsWith("PARTIAL") ? "bg-yellow-500/10 text-yellow-400" :
                          "bg-blue-500/10 text-blue-400"
                        }`}>{el.reconciliation.split(" — ")[0]}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 p-3 rounded border border-yellow-500/20 bg-yellow-500/5">
              <p className="text-xs text-yellow-400/80">
                <span className="font-mono font-bold">§11 Open Items:</span> Semantic-to-numeric mapping (E153-E162 vs R-series vs semantic-only),
                sphere addressing translation (8 of 12 entries exceed 12×12 grid), cascade coexistence
                (12-Element vs 8-VIP dispatch), provider matrix naming convention.
              </p>
            </div>
          </motion.div>

          {/* Cascade Elasticity */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-2xl font-display font-bold mb-4">Cascade Elasticity</h2>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              The routing cascade is not rigid — it adapts to context. Elasticity rules define how
              the cascade stretches or compresses based on load, jurisdiction, and emergency conditions.
            </p>
            <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
              <pre>{`cascade_elasticity: {
  // Normal operation: full 5-tier VIP cascade
  normal: {
    tiers: ["safety", "sovereignty", "governance", "provenance", "performance"],
    timeout_ms: 5000,
    fallback: "M111_error_mode"
  },
  // Degraded: provider failure or capacity < 40%
  degraded: {
    tiers: ["safety", "sovereignty"],  // Collapse to 2-tier
    timeout_ms: 2000,
    fallback: "safe_default_response",
    log: "MANDATORY"  // INV-17 still applies
  },
  // Emergency: EHIP triggered (Doctrine 101)
  emergency: {
    tiers: ["safety"],  // Single-tier: safety only
    timeout_ms: 500,
    escalate_to: "convenor",
    override_authority: "INV-1"  // Human sovereignty absolute
  }
}`}</pre>
            </div>
          </motion.div>

          {/* GitHub link */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <div className="p-6 rounded border border-border/50 bg-card/20 text-center">
              <p className="text-muted-foreground mb-3">
                Full routing pack source files available on GitHub
              </p>
              <a
                href={`${GITHUB_URL}/tree/main/element145_routing_pack`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded bg-primary text-primary-foreground font-medium text-sm hover:opacity-90 transition-opacity"
              >
                View Routing Pack on GitHub
              </a>
            </div>
          </motion.div>

          {/* Source Traceability */}
          <div className="mt-16 pt-8 border-t border-border/30">
            <h3 className="text-sm font-mono text-muted-foreground/60 mb-3">Source Traceability</h3>
            <div className="flex flex-wrap gap-3">
              <a href={`${GITHUB_URL}/blob/master/docs/architecture/SOURCE_OF_TRUTH.md`} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ SOURCE_OF_TRUTH.md</a>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ GitHub Repository</a>
            </div>
          </div>
        </div>
      </div>
    </SpecLayout>
  );
}

import { useState } from "react";
import { GITHUB_URL } from "@/lib/data";
import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";
import { VIP_IMAGE, vipElements } from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Elements() {
  const [expanded, setExpanded] = useState<string | null>("E145");

  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-6xl">
          {/* Hero */}
          <div className="relative rounded-lg overflow-hidden mb-12">
            <img src={VIP_IMAGE} alt="VIP Elements" className="w-full h-48 object-cover opacity-40" />
            <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent" />
            <div className="absolute inset-0 flex items-center p-8">
              <motion.div initial="hidden" animate="visible" variants={fadeUp}>
                <h1 className="text-4xl font-display font-bold mb-2">
                  <span className="text-gradient-gold">12 VIP Elements</span>
                </h1>
                <p className="text-muted-foreground max-w-xl">
                  Civilizational substrates that cross-cut all 12 Houses. These are not categories —
                  they are the addressing primitives for substrate-organized retrieval.
                </p>
              </motion.div>
            </div>
          </div>

          {/* Sovereignty Vector Schema */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-lg font-display font-semibold mb-3">Sovereignty Vector Schema</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Every VIP Element carries a six-dimensional sovereignty assessment. This schema is applied
              at routing time to determine which sovereign deployment pathway governs the query.
            </p>
            <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
              <pre>{`sovereignty_vector: {
  legal:       float[0..1]  // Jurisdiction compliance score
  data:        float[0..1]  // Data residency & localization
  compute:     float[0..1]  // Compute sovereignty (on-soil %)
  economic:    float[0..1]  // Economic dependency risk
  provenance:  float[0..1]  // Model lineage traceability
  operational: float[0..1]  // Operational independence
  // Composite: weighted_mean(legal*0.25, data*0.20, compute*0.20,
  //            economic*0.15, provenance*0.10, operational*0.10)
  // Threshold: composite >= 0.7 for sovereign pathway eligibility
}`}</pre>
            </div>
          </motion.div>

          {/* Provenance Schema */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-12">
            <h2 className="text-lg font-display font-semibold mb-3">Provenance Schema</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Every routing decision and editorial action generates a provenance record.
              This schema is the minimum viable audit trail per INV-17 (Traceability).
            </p>
            <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
              <pre>{`provenance_record: {
  id:              uuid
  timestamp:       ISO-8601 UTC
  spec_version:    "v4.0-DRAFT.6"
  action_type:     enum[route|ingest|verify|reject|escalate]
  source_element:  E-number (E145..E156)
  target_houses:   H-number[] (H1..H12)
  model_lineage:   { provider, model_id, version, capability_tier }
  evidence_chain:  { source_url, hash_sha256, retrieval_ts }
  sovereignty:     sovereignty_vector
  constitutional:  { invariants_checked: INV-number[], passed: bool }
  transparency:    TransparencyPacket
}`}</pre>
            </div>
          </motion.div>

          {/* Elements list */}
          <div className="space-y-3">
            {vipElements.map((el) => (
              <motion.div
                key={el.id}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                className="rounded border border-border/50 bg-card/20 overflow-hidden"
              >
                <button
                  onClick={() => setExpanded(expanded === el.id ? null : el.id)}
                  className="w-full flex items-center gap-4 p-5 text-left hover:bg-card/40 transition-colors"
                >
                  <div
                    className="w-10 h-10 rounded flex items-center justify-center shrink-0 font-mono text-xs font-bold"
                    style={{ backgroundColor: el.color + "20", color: el.color, border: `1px solid ${el.color}40` }}
                  >
                    {el.code}
                  </div>
                  <div className="flex-1">
                    <div className="font-display font-semibold">{el.name}</div>
                    <div className="text-xs text-muted-foreground">{el.subtitle} — Houses: {el.housePairs.join(", ")}</div>
                  </div>
                  <ChevronDown className={`w-5 h-5 text-muted-foreground transition-transform ${expanded === el.id ? "rotate-180" : ""}`} />
                </button>

                {expanded === el.id && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    className="border-t border-border/30 p-5"
                  >
                    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {el.nodes.map((node) => (
                        <div
                          key={node.id}
                          className="p-3 rounded border border-border/30 bg-background/50"
                        >
                          <div className="font-mono text-xs mb-1" style={{ color: el.color }}>
                            {node.id}
                          </div>
                          <div className="text-sm font-medium mb-1">{node.name}</div>
                          <div className="text-xs text-muted-foreground">{node.description}</div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      
          {/* Source Traceability */}
          <div className="mt-16 pt-8 border-t border-border/30">
            <h3 className="text-sm font-mono text-muted-foreground/60 mb-3">Source Traceability</h3>
            <div className="flex flex-wrap gap-3">
              <a href={`${GITHUB_URL}/blob/master/docs/architecture/SOURCE_OF_TRUTH.md`} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ SOURCE_OF_TRUTH.md</a>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-xs font-mono text-primary/60 hover:text-primary transition-colors">→ GitHub Repository</a>
            </div>
          </div>
</div>
    </SpecLayout>
  );
}

import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const zones = [
  {
    name: "Standard Compliance",
    code: "ZONE-STD",
    description: "Single-jurisdiction zones with clear regulatory frameworks. Most routing decisions fall here.",
    rules: ["Single dialect overlay applies", "Standard sovereignty vector thresholds", "Full provider pool available", "Normal cascade elasticity"],
    examples: "US-only queries, EU-only queries, JP domestic",
    color: "border-emerald-500/40",
  },
  {
    name: "Mixed-Compliance",
    code: "ZONE-MIX",
    description: "Overlapping jurisdictions where multiple dialect overlays apply simultaneously. Requires most-restrictive union strategy.",
    rules: ["Multiple dialect overlays composed", "Most-restrictive union (INV-3)", "Dual-jurisdiction provenance logging", "Reduced provider pool (intersection)"],
    examples: "EU citizen querying from US, cross-border data flows, multinational corporate queries",
    color: "border-yellow-500/40",
  },
  {
    name: "Contested",
    code: "ZONE-CON",
    description: "Disputed sovereignty zones where compliance cannot be guaranteed. System refuses to route and escalates.",
    rules: ["Refuse-and-escalate strategy", "No routing decisions made", "Full audit trail generated", "Convenor notification triggered"],
    examples: "Sanctioned regions, disputed territories, conflicting legal orders",
    color: "border-red-500/40",
  },
  {
    name: "Low-Power / Emergency",
    code: "ZONE-LPE",
    description: "Degraded capacity zones where normal cascade cannot complete. Emergency elasticity rules apply.",
    rules: ["Cascade collapses to 2-tier (safety + sovereignty)", "Reduced timeout (2000ms → 500ms)", "Safe default responses preferred", "EHIP may trigger (Doctrine 101)"],
    examples: "Infrastructure outage, natural disaster, provider failure cascade",
    color: "border-purple-500/40",
  },
];

export default function ComputeZones() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Compute Zones</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Compute zones define the geographic and jurisdictional boundaries within which specific
            routing rules, provider pools, and sovereignty constraints apply.
          </p>
        </motion.div>

        <div className="space-y-6">
          {zones.map((zone) => (
            <motion.div
              key={zone.code}
              variants={fadeUp}
              className={`p-6 rounded border-l-4 ${zone.color} border border-border/50 bg-card/30`}
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-0.5 rounded">{zone.code}</span>
                <h2 className="text-xl font-display font-bold">{zone.name}</h2>
              </div>
              <p className="text-sm text-muted-foreground mb-4">{zone.description}</p>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <h3 className="text-xs font-mono text-primary uppercase mb-2">Rules</h3>
                  <ul className="space-y-1">
                    {zone.rules.map((r, i) => (
                      <li key={i} className="text-xs text-muted-foreground flex items-start gap-2">
                        <span className="text-primary mt-0.5">•</span> {r}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="text-xs font-mono text-primary uppercase mb-2">Examples</h3>
                  <p className="text-xs text-muted-foreground">{zone.examples}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Zone Detection Schema */}
        <motion.div variants={fadeUp} className="mt-12">
          <h2 className="text-lg font-display font-semibold mb-3">Zone Detection Schema</h2>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
            <pre>{`zone_detection: {
  input:  { query_context, user_jurisdiction, provider_pool }
  output: { zone_code, applicable_dialects[], sovereignty_vector }
  
  rules: [
    "IF single_jurisdiction → ZONE-STD",
    "IF multiple_jurisdictions AND all_compliant → ZONE-MIX",
    "IF any_jurisdiction_sanctioned OR disputed → ZONE-CON",
    "IF capacity < 40% OR provider_cascade_failure → ZONE-LPE",
  ]
  
  override: "Convenor may manually reclassify zones (INV-9)"
  audit:    "Zone classification logged in every provenance record"
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

import { motion } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";
import { sovereignPathways, GITHUB_URL } from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const dimensions = [
  { name: "Legal", weight: "0.25", desc: "Jurisdiction compliance — does the routing decision satisfy local law?" },
  { name: "Data", weight: "0.20", desc: "Data residency & localization — where is the data stored and processed?" },
  { name: "Compute", weight: "0.20", desc: "Compute sovereignty — what percentage of compute runs on-soil?" },
  { name: "Economic", weight: "0.15", desc: "Economic dependency risk — how concentrated is the provider dependency?" },
  { name: "Provenance", weight: "0.10", desc: "Model lineage traceability — can the model's training data be audited?" },
  { name: "Operational", weight: "0.10", desc: "Operational independence — can the system run without external dependencies?" },
];

export default function Sovereignty() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Sovereignty</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Every routing decision in Aluminum OS carries a six-dimensional sovereignty assessment.
            No single vendor, country, or ideology controls the computation.
          </p>
        </motion.div>

        {/* Sovereignty Vector */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Sovereignty Vector</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-6">
            The sovereignty vector is a six-dimensional score attached to every routing decision.
            Composite score must be &ge; 0.7 for sovereign pathway eligibility.
          </p>
          <div className="space-y-2">
            {dimensions.map((d) => (
              <div key={d.name} className="flex items-center gap-4 p-3 rounded border border-border/50 bg-card/30">
                <div className="shrink-0 w-20 font-mono text-xs text-primary font-bold">{d.name}</div>
                <div className="shrink-0 w-12 font-mono text-xs text-muted-foreground">{d.weight}</div>
                <div className="text-sm text-muted-foreground">{d.desc}</div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Sovereign Deployment Pathways */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Sovereign Deployment Pathways</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-6">
            Named sovereign deployments enforce jurisdiction-specific constraints.
            Each pathway is a dialect + compute zone + provider pool configuration.
          </p>
          <div className="grid sm:grid-cols-2 gap-4">
            {sovereignPathways.map((p) => (
              <div key={p.name} className="p-5 rounded border border-border/50 bg-card/30 hover:border-primary/30 transition-colors">
                <div className="flex items-center gap-3 mb-2">
                  <div>
                    <h3 className="font-display font-semibold">{p.name}</h3>
                    <span className="text-[10px] font-mono text-primary">{p.region}</span>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-3">{p.stack}</p>
                <div className="flex items-center gap-3 text-xs">
                  <span className={`font-mono px-2 py-0.5 rounded ${
                    p.status === "SPECIFIED" ? "bg-emerald-500/10 text-emerald-400" : "bg-primary/10 text-primary"
                  }`}>{p.status}</span>
                  <span className="text-muted-foreground">Target: {p.target}</span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Conflict Resolution */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Conflict Resolution</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-6">
            When sovereignty vectors conflict (e.g., a query touches both CN and US jurisdictions),
            the system applies the following resolution cascade:
          </p>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
            <pre>{`sovereignty_conflict_resolution: {
  step_1: "Identify all applicable jurisdictions from query context"
  step_2: "Compute sovereignty_vector for each jurisdiction"
  step_3: "Apply most_restrictive_union strategy (INV-3)"
  step_4: "If composite < 0.7 for all pathways → route to Global dialect"
  step_5: "If EHIP triggered → escalate to Convenor (Doctrine 101)"
  step_6: "Log dual-jurisdiction provenance record (INV-17)"
  
  // Special case: Contested compute zones
  contested_zone: {
    strategy: "refuse_and_escalate",
    reason: "Cannot guarantee sovereignty compliance",
    fallback: "Global dialect with full audit trail"
  }
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

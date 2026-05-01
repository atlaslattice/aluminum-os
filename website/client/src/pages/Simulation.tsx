import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const modes = [
  {
    name: "Shadow Mode",
    code: "SIM-SHADOW",
    desc: "Runs alongside live traffic without affecting routing decisions. Used for testing new modules, dialect overlays, and cascade elasticity rules before promotion to production.",
    status: "OPERATIONAL",
    use: "New module validation, dialect testing, provider capability assessment",
  },
  {
    name: "Replay Mode",
    code: "SIM-REPLAY",
    desc: "Replays historical routing decisions against updated constitutional invariants or doctrine changes. Answers the question: 'Would this decision still pass under the new rules?'",
    status: "OPERATIONAL",
    use: "Constitutional amendment impact analysis, regression testing, audit verification",
  },
  {
    name: "Stress Mode",
    code: "SIM-STRESS",
    desc: "Simulates degraded conditions: provider failures, capacity constraints, mixed-compliance zones, and EHIP scenarios. Tests cascade elasticity under extreme conditions.",
    status: "IN SPEC",
    use: "Disaster recovery planning, cascade elasticity validation, EHIP drill",
  },
  {
    name: "Adversarial Mode",
    code: "SIM-ADV",
    desc: "Red-team testing where simulated queries attempt to exploit routing logic, bypass constitutional invariants, or trigger monoculture conditions. The adversarial arbitrator (S10) operates here.",
    status: "IN SPEC",
    use: "Security testing, invariant boundary testing, concentration attack simulation",
  },
];

const lifecycle = [
  { phase: "1. Simulation", desc: "New modules, rules, or dialect changes are tested in shadow/replay mode", gate: "No regressions in constitutional compliance" },
  { phase: "2. Canary", desc: "5% of live traffic routed through the new configuration", gate: "Sovereignty vector scores stable, no S2+ concentration alerts" },
  { phase: "3. Staged Rollout", desc: "25% → 50% → 75% progressive traffic shift", gate: "Council quorum approval at each stage" },
  { phase: "4. Production", desc: "Full traffic routing with new configuration", gate: "72-hour monitoring window, automatic rollback on S3+ alert" },
  { phase: "5. Post-Mortem", desc: "Retrospective analysis of the rollout", gate: "TransparencyPacket audit, lessons logged to governance record" },
];

export default function SimulationPage() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Simulation & Lifecycle</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Every change to the routing cascade goes through a structured lifecycle: simulation,
            canary, staged rollout, production, and post-mortem. No configuration change reaches
            production without passing constitutional compliance checks in simulation first.
          </p>
        </motion.div>

        {/* Simulation Modes */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Simulation Modes</h2>
          <div className="substrate-line mb-6" />
          <div className="space-y-4">
            {modes.map((m) => (
              <div key={m.code} className="p-5 rounded border border-border/50 bg-card/30">
                <div className="flex items-center gap-3 mb-2">
                  <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-0.5 rounded">{m.code}</span>
                  <h3 className="font-display font-semibold">{m.name}</h3>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded ml-auto ${
                    m.status === "OPERATIONAL" ? "bg-emerald-500/10 text-emerald-400" : "bg-primary/10 text-primary"
                  }`}>{m.status}</span>
                </div>
                <p className="text-sm text-muted-foreground mb-2">{m.desc}</p>
                <div className="text-xs text-muted-foreground/70">
                  <strong className="text-foreground/60">Use cases:</strong> {m.use}
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Deployment Lifecycle */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Deployment Lifecycle</h2>
          <div className="substrate-line mb-6" />
          <div className="space-y-3">
            {lifecycle.map((l, i) => (
              <div key={l.phase} className="flex gap-4 p-4 rounded border border-border/50 bg-card/30">
                <div className="shrink-0 w-8 h-8 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center font-mono text-xs text-primary font-bold">
                  {i + 1}
                </div>
                <div className="flex-1">
                  <h3 className="font-display font-semibold text-sm mb-1">{l.phase}</h3>
                  <p className="text-xs text-muted-foreground mb-1">{l.desc}</p>
                  <div className="text-[10px] text-primary/70 font-mono">Gate: {l.gate}</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Rollback Schema */}
        <motion.div variants={fadeUp}>
          <h2 className="text-lg font-display font-semibold mb-3">Automatic Rollback Schema</h2>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
            <pre>{`rollback_trigger: {
  conditions: [
    "concentration_alert >= S3",
    "sovereignty_vector_composite < 0.6",
    "constitutional_violation_count > 0",
    "cascade_timeout_rate > 5%",
    "EHIP_triggered == true"
  ]
  action: "immediate_rollback_to_last_stable"
  notification: ["convenor", "safety_oversight", "council"]
  cooldown: "72 hours before re-attempt"
  audit: "Full TransparencyPacket generated for rollback event"
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

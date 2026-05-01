import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const severityLevels = [
  { level: "S1 — Watch", threshold: "Single provider > 30%", action: "Log warning, no intervention", color: "text-yellow-400", bg: "bg-yellow-500/10" },
  { level: "S2 — Alert", threshold: "Single provider > 40%", action: "Notify Council, begin rebalancing", color: "text-orange-400", bg: "bg-orange-500/10" },
  { level: "S3 — Breach", threshold: "Single provider > 47% (INV-7c)", action: "Automatic routing redistribution", color: "text-red-400", bg: "bg-red-500/10" },
  { level: "S4 — Critical", threshold: "Single provider > 55%", action: "Emergency Council session, provider cap enforced", color: "text-red-500", bg: "bg-red-600/10" },
  { level: "S5 — Existential", threshold: "Single provider > 60%", action: "System-wide halt, Convenor veto authority activated", color: "text-red-600", bg: "bg-red-700/10" },
];

const mechanisms = [
  { name: "Provider Cap (INV-7c)", desc: "No single provider may handle more than 47% of routing decisions in any rolling 30-day window. Hard cap at 60% triggers system halt." },
  { name: "Diversity Index", desc: "Shannon entropy of provider distribution must remain above 1.5 bits. Below this threshold, the system is considered monocultural." },
  { name: "Capability Matrix Rotation", desc: "Provider capability assessments are re-evaluated quarterly. No provider receives preferential routing based on historical performance alone." },
  { name: "Open-Weight Verification", desc: "DeepSeek-R1 can independently verify that routing decisions are not biased toward any single provider. Offline audit capability." },
  { name: "Sovereign Pathway Diversity", desc: "Each sovereign deployment pathway must support at least 3 independent providers. Single-provider pathways are prohibited." },
  { name: "Predictive Modeling", desc: "The system models concentration risk 90 days forward. If projected concentration exceeds S2 threshold, preemptive rebalancing begins." },
];

export default function AntiMonoculture() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Anti-Monoculture</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            The single most important structural guarantee in Aluminum OS: no single vendor,
            country, model, or ideology may dominate the computation. This is not a policy
            preference — it is a constitutional invariant (INV-7c).
          </p>
        </motion.div>

        {/* Severity Table */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Concentration Severity Table</h2>
          <div className="substrate-line mb-6" />
          <div className="space-y-2">
            {severityLevels.map((s) => (
              <div key={s.level} className={`flex items-center gap-4 p-4 rounded border border-border/50 ${s.bg}`}>
                <div className={`shrink-0 w-32 font-mono text-xs font-bold ${s.color}`}>{s.level}</div>
                <div className="flex-1 text-sm text-muted-foreground">{s.threshold}</div>
                <div className="flex-1 text-sm text-muted-foreground">{s.action}</div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Mechanisms */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Anti-Concentration Mechanisms</h2>
          <div className="substrate-line mb-6" />
          <div className="grid sm:grid-cols-2 gap-4">
            {mechanisms.map((m) => (
              <div key={m.name} className="p-4 rounded border border-border/50 bg-card/30">
                <h3 className="font-display font-semibold text-sm mb-2">{m.name}</h3>
                <p className="text-xs text-muted-foreground">{m.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Operational Response Levels */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Operational Response Levels</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-4">
            Beyond the quantitative severity table, the system defines three broad operational
            response postures that guide human and automated decision-making:
          </p>
          <div className="grid sm:grid-cols-3 gap-4">
            <div className="p-4 rounded border border-yellow-500/30 bg-yellow-500/5">
              <h3 className="font-display font-semibold text-sm mb-2 text-yellow-400">Mild</h3>
              <p className="text-xs text-muted-foreground mb-2">Early signs of concentration detected.</p>
              <ul className="text-[10px] text-muted-foreground space-y-1 list-disc list-inside">
                <li>Diversify routing paths proactively</li>
                <li>Increase monitoring frequency</li>
                <li>Log concentration metrics for trend analysis</li>
              </ul>
            </div>
            <div className="p-4 rounded border border-orange-500/30 bg-orange-500/5">
              <h3 className="font-display font-semibold text-sm mb-2 text-orange-400">Moderate</h3>
              <p className="text-xs text-muted-foreground mb-2">Dominant provider or dialect identified.</p>
              <ul className="text-[10px] text-muted-foreground space-y-1 list-disc list-inside">
                <li>Enforce minimum diversity thresholds</li>
                <li>Activate secondary provider pathways</li>
                <li>Council notification triggered</li>
              </ul>
            </div>
            <div className="p-4 rounded border border-red-500/30 bg-red-500/5">
              <h3 className="font-display font-semibold text-sm mb-2 text-red-400">Severe</h3>
              <p className="text-xs text-muted-foreground mb-2">Single-provider or single-model collapse.</p>
              <ul className="text-[10px] text-muted-foreground space-y-1 list-disc list-inside">
                <li>Emergency diversification protocol</li>
                <li>Governance review initiated</li>
                <li>Convenor veto authority activated</li>
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Predictive Modeling Note */}
        <motion.div variants={fadeUp}>
          <div className="p-5 rounded border border-primary/30 bg-primary/5">
            <h3 className="font-display font-semibold mb-2">Predictive Modeling Note</h3>
            <p className="text-sm text-muted-foreground">
              The anti-monoculture system does not merely react to concentration — it predicts it.
              Using 90-day rolling projections of provider usage patterns, the system can identify
              emerging monoculture risks before they breach INV-7c thresholds. This predictive
              capability is what distinguishes Aluminum OS from reactive governance frameworks.
              The model runs in shadow mode alongside live traffic, generating alerts without
              affecting routing decisions until validated by the Council.
            </p>
          
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

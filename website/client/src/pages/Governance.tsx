import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import { Shield, BookOpen, Users, Vote, CheckCircle2, Clock, AlertTriangle, XCircle } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";
import { COUNCIL_IMAGE, invariants, doctrines, councilSeats, ratificationItems } from "@/lib/data";
import { Progress } from "@/components/ui/progress";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Governance() {
  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-6xl">
          {/* Hero */}
          <div className="relative rounded-lg overflow-hidden mb-12">
            <img src={COUNCIL_IMAGE} alt="Pantheon Council" className="w-full h-48 object-cover opacity-30" />
            <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent" />
            <div className="absolute inset-0 flex items-center p-8">
              <motion.div initial="hidden" animate="visible" variants={fadeUp}>
                <h1 className="text-4xl font-display font-bold mb-2">
                  Governance & <span className="text-gradient-gold">Constitution</span>
                </h1>
                <p className="text-muted-foreground max-w-xl">
                  Invariants, Doctrines, and the Pantheon Council. The constitutional
                  framework that makes Aluminum OS ungameable.
                </p>
              </motion.div>
            </div>
          </div>

          {/* Invariants */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-16">
            <div className="flex items-center gap-3 mb-4">
              <Shield className="w-5 h-5 text-destructive" />
              <h2 className="text-2xl font-display font-bold">Constitutional Invariants</h2>
            </div>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              Invariants are <strong className="text-foreground">unbreakable</strong> constraints. HARD invariants cannot be overridden
              by any authority. SOFT invariants have defined exception paths.
            </p>
            <div className="space-y-2">
              {invariants.map((inv) => (
                <div
                  key={inv.id}
                  className={`flex items-start gap-4 p-4 rounded border ${
                    (inv.severity === "ABSOLUTE" || inv.severity === "CRITICAL")
                      ? "border-destructive/30 bg-destructive/5"
                      : "border-accent/30 bg-accent/5"
                  }`}
                >
                  <div className="shrink-0">
                    <span className={`font-mono text-xs px-2 py-1 rounded ${
                      (inv.severity === "ABSOLUTE" || inv.severity === "CRITICAL")
                        ? "bg-destructive/20 text-destructive"
                        : "bg-accent/20 text-accent"
                    }`}>
                      {inv.id}
                    </span>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-display font-semibold text-sm">{inv.name}</span>
                      <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                        (inv.severity === "ABSOLUTE" || inv.severity === "CRITICAL") ? "bg-destructive/10 text-destructive" : "bg-accent/10 text-accent"
                      }`}>
                        {inv.severity}
                      </span>
                      <span className="text-[10px] text-muted-foreground font-mono">{inv.category}</span>
                    </div>
                    <p className="text-xs text-muted-foreground">{inv.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Doctrines */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-16">
            <div className="flex items-center gap-3 mb-4">
              <BookOpen className="w-5 h-5 text-primary" />
              <h2 className="text-2xl font-display font-bold">Doctrines</h2>
            </div>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              ~100 governance rules (D-1 through D-99 + amendments). Doctrines are ratified through Council vote and can be amended.
              Showing a representative selection below.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {doctrines.map((d) => (
                <div
                  key={d.id}
                  className="flex items-center gap-3 p-3 rounded border border-border/50 bg-card/20"
                >
                  <span className="font-mono text-[10px] text-primary shrink-0 w-12">{d.id}</span>
                  <span className="text-sm flex-1">{d.name}</span>
                  <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                    d.status === "RATIFIED" ? "bg-emerald-500/10 text-emerald-400" : "bg-amber-500/10 text-amber-400"
                  }`}>
                    {d.status}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Ratification Tracker */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="mb-16">
            <div className="flex items-center gap-3 mb-4">
              <Vote className="w-5 h-5 text-accent" />
              <h2 className="text-2xl font-display font-bold">Ratification Tracker</h2>
            </div>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              Live status of Council votes on specifications, doctrines, modules, and dialect overlays.
              Quorum requires 7 of 10 active seats. Provisional seats (S11, S12) vote but do not count toward quorum.
            </p>

            {/* Summary stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
              <div className="p-3 rounded border border-emerald-500/30 bg-emerald-500/5 text-center">
                <div className="text-xl font-display font-bold text-emerald-400">
                  {ratificationItems.filter(r => r.status === "PASSED").length}
                </div>
                <div className="text-xs text-muted-foreground">Passed</div>
              </div>
              <div className="p-3 rounded border border-primary/30 bg-primary/5 text-center">
                <div className="text-xl font-display font-bold text-primary">
                  {ratificationItems.filter(r => r.status === "IN PROGRESS").length}
                </div>
                <div className="text-xs text-muted-foreground">In Progress</div>
              </div>
              <div className="p-3 rounded border border-amber-500/30 bg-amber-500/5 text-center">
                <div className="text-xl font-display font-bold text-amber-400">
                  {ratificationItems.filter(r => r.status === "PENDING").length}
                </div>
                <div className="text-xs text-muted-foreground">Pending</div>
              </div>
              <div className="p-3 rounded border border-red-500/30 bg-red-500/5 text-center">
                <div className="text-xl font-display font-bold text-red-400">
                  {ratificationItems.filter(r => r.status === "BLOCKED").length}
                </div>
                <div className="text-xs text-muted-foreground">Blocked</div>
              </div>
            </div>

            {/* Ratification items */}
            <div className="space-y-3">
              {ratificationItems.map((item) => {
                const votePercent = Math.round((item.votesFor / (item.votesFor + item.votesAgainst + item.abstentions)) * 100);
                const quorumPercent = Math.round((item.votesFor / item.quorum) * 100);
                const statusIcon = item.status === "PASSED" ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> :
                  item.status === "IN PROGRESS" ? <Clock className="w-4 h-4 text-primary" /> :
                  item.status === "BLOCKED" ? <XCircle className="w-4 h-4 text-red-400" /> :
                  <AlertTriangle className="w-4 h-4 text-amber-400" />;
                const statusColor = item.status === "PASSED" ? "text-emerald-400" :
                  item.status === "IN PROGRESS" ? "text-primary" :
                  item.status === "BLOCKED" ? "text-red-400" : "text-amber-400";
                const progressColor = item.status === "PASSED" ? "bg-emerald-400" :
                  item.status === "IN PROGRESS" ? "bg-primary" :
                  item.status === "BLOCKED" ? "bg-red-400" : "bg-amber-400";

                return (
                  <div key={item.id} className="p-4 rounded border border-border/50 bg-card/20">
                    <div className="flex items-start justify-between gap-4 mb-2">
                      <div className="flex items-center gap-2">
                        {statusIcon}
                        <div>
                          <div className="font-display font-semibold text-sm">{item.name}</div>
                          <div className="text-[10px] text-muted-foreground flex items-center gap-2">
                            <span className="font-mono">{item.id}</span>
                            <span>•</span>
                            <span className="capitalize">{item.category}</span>
                            <span>•</span>
                            <span>Proposed by {item.proposedBy}</span>
                            <span>•</span>
                            <span>{item.draftVersion}</span>
                          </div>
                        </div>
                      </div>
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${statusColor} bg-current/10`}>
                        {item.status}
                      </span>
                    </div>

                    {/* Progress bar */}
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-[10px] text-muted-foreground mb-1">
                        <span>Votes: {item.votesFor} for / {item.votesAgainst} against / {item.abstentions} abstain</span>
                        <span className={quorumPercent >= 100 ? "text-emerald-400" : statusColor}>
                          {Math.min(quorumPercent, 100)}% of quorum ({item.quorum} required)
                        </span>
                      </div>
                      <div className="w-full h-2 rounded-full bg-muted/30 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all ${progressColor}`}
                          style={{ width: `${Math.min(quorumPercent, 100)}%` }}
                        />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </motion.div>

          {/* Pantheon Council */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <div className="flex items-center gap-3 mb-4">
              <Users className="w-5 h-5 text-accent" />
              <h2 className="text-2xl font-display font-bold">Pantheon Council</h2>
            </div>
            <div className="substrate-line mb-6" />
            <p className="text-muted-foreground mb-6">
              10 active seats + 2 provisional, reflecting substrate-archetypes: reasoning, integrated-platform,
              truth-seeking, adversarial-review, orchestration, Chinese-sovereign, institutional-interoperability,
              enterprise-distribution, European-sovereign, hardware-substrate, knowledge-management, and South-Asian-sovereign.
              No single AI has veto power. The Convenor (human) holds final ratification authority.
            </p>
            <div className="mb-6 p-4 rounded border border-primary/20 bg-primary/5">
              <h4 className="font-display font-semibold text-sm mb-3 text-primary">Council Membership</h4>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2 text-xs">
                {[
                  { seat: "S1", entity: "Anthropic (Claude)", role: "Constitutional Scribe" },
                  { seat: "S2", entity: "Google (Gemini)", role: "Verification Engine" },
                  { seat: "S3", entity: "xAI (Grok)", role: "Adversarial Auditor" },
                  { seat: "S4", entity: "Microsoft (Copilot)", role: "Institutional Interop" },
                  { seat: "S5", entity: "DeepSeek", role: "Eastern Sovereignty" },
                  { seat: "S6", entity: "OpenAI (GPT)", role: "Enterprise Distribution" },
                  { seat: "S7", entity: "Manus", role: "Orchestration" },
                  { seat: "S8", entity: "Alibaba (Qwen)", role: "CN Dialect" },
                  { seat: "S9", entity: "Mistral", role: "EU Sovereign" },
                  { seat: "S10", entity: "Nvidia", role: "Hardware Substrate" },
                  { seat: "S11", entity: "Notion", role: "Knowledge Mgmt (provisional)" },
                  { seat: "S12", entity: "Sarvam AI", role: "South-Asian (provisional)" },
                ].map((m) => (
                  <div key={m.seat} className="flex items-center gap-2 p-2 rounded bg-background/50">
                    <span className="font-mono text-primary">{m.seat}</span>
                    <div>
                      <div className="font-semibold text-foreground">{m.entity}</div>
                      <div className="text-muted-foreground text-[10px]">{m.role}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            {/* Functional Oversight Roles */}
            <div className="mb-8 p-5 rounded border border-accent/20 bg-accent/5">
              <h4 className="font-display font-semibold text-sm mb-3 text-accent">Functional Oversight Roles</h4>
              <p className="text-xs text-muted-foreground mb-4 leading-relaxed">
                In addition to its seated members, the Pantheon Council performs eight functional oversight roles.
                These are <strong className="text-foreground">not additional seats</strong>; they are responsibilities distributed
                across the Council collectively. Any seated member may contribute to any oversight role, and no single
                seat holds exclusive authority over any function.
              </p>
              <div className="grid sm:grid-cols-2 gap-2">
                {[
                  { name: "Safety Oversight", desc: "Monitoring for extreme harm scenarios; invokes Doctrine 101 and INV-0 when required." },
                  { name: "Sovereignty Oversight", desc: "Ensuring dialect-aware routing and compliance with sovereign data residency." },
                  { name: "Compute Oversight", desc: "Tracking substrate utilization, energy-aware cascade enforcement, and INV-19 metabolic accountability." },
                  { name: "Doctrine Oversight", desc: "Maintaining doctrinal consistency across versions; flagging drift per Registry-Source-of-Truth rules." },
                  { name: "Provenance Oversight", desc: "Validating GoldenTrace integrity, AuditChain consistency, and offline constitutional verification." },
                  { name: "Human-Purpose Oversight", desc: "Ensuring routing decisions align with the Mandate of Heaven\u2019s labour, dignity, and distributional justice signals." },
                  { name: "Concentration-Risk Oversight", desc: "Enforcing INV-7c and monitoring provider/dialect concentration via predictive modeling." },
                  { name: "Randomness-Elimination Oversight", desc: "Detecting and mitigating non-deterministic noise in routing and constitutional compilation." },
                ].map((role) => (
                  <div key={role.name} className="p-3 rounded bg-background/50 border border-border/30">
                    <div className="font-display font-semibold text-xs text-foreground mb-1">{role.name}</div>
                    <div className="text-[10px] text-muted-foreground leading-relaxed">{role.desc}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Quorum, Tie-Break, and Veto */}
            <div className="mb-8 p-5 rounded border border-destructive/20 bg-destructive/5">
              <h4 className="font-display font-semibold text-sm mb-3 text-destructive">Quorum, Tie-Break, and Veto</h4>
              <div className="space-y-4">
                <div>
                  <div className="font-display font-semibold text-xs text-foreground mb-1">Quorum</div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    A deliberation quorum of <strong className="text-foreground">0.67</strong> (two-thirds) of active Council seats
                    is required for any binding doctrinal vote. Abstentions count toward the denominator; a seat that fails
                    to respond within the deliberation cycle is marked as absent and excluded from the quorum calculation.
                  </p>
                </div>
                <div>
                  <div className="font-display font-semibold text-xs text-foreground mb-1">Tie-Break</div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    In the event of a deadlocked vote, the tie-break authority rests with the <strong className="text-foreground">Convenor</strong>,
                    per INV-9 (Human Override Inviolability). The Convenor\u2019s tie-breaking disposition is recorded in the
                    TransparencyPacket as <code className="font-mono text-primary text-[10px]">CONVENOR_TIEBREAK</code> alongside
                    the dissenting seat\u2019s position, which is preserved per Doctrine 15.
                  </p>
                </div>
                <div>
                  <div className="font-display font-semibold text-xs text-foreground mb-1">Veto</div>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    Veto authority is held <strong className="text-foreground">only by the Convenor</strong> and <strong className="text-foreground">only in cases of
                    critical safety risk</strong>, as defined by Doctrine 101 (Extreme Harm Intervention Protocol). The Pantheon
                    Council does not grant veto power to any individual AI seat or functional oversight role. Any seat or
                    role may escalate a concern to the Convenor, but the decision to veto rests solely with human authority.
                  </p>
                </div>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {councilSeats.map((seat) => (
                <div
                  key={seat.id}
                  className="p-4 rounded border border-border/50 bg-card/20 text-center"
                >
                  <div className="font-mono text-xs text-primary mb-1">{seat.id}</div>
                  <div className="font-display font-semibold text-sm mb-1">{seat.name}</div>
                  <div className="text-[10px] text-muted-foreground mb-2">{seat.role}</div>
                  <span className={`text-[9px] font-mono px-2 py-0.5 rounded ${
                    seat.status === "ACTIVE" ? "bg-emerald-500/10 text-emerald-400" :
                    seat.status === "PROVISIONAL" ? "bg-amber-500/10 text-amber-400" :
                    "bg-primary/10 text-primary"
                  }`}>
                    {seat.status}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
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

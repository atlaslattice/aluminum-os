import { motion } from "framer-motion";
import { Target, Clock, Globe, ArrowRight, CheckCircle, AlertCircle, Shield } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";
import {
  battleStrategy,
  GITHUB_URL,
  sovereignPathways,
  councilArchetypes,
} from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.08 } },
};

export default function Strategy() {
  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-6xl">
          {/* Header */}
          <motion.div initial="hidden" animate="visible" variants={stagger} className="mb-16">
            <motion.h1 variants={fadeUp} className="text-4xl font-display font-bold mb-4">
              Battle <span className="text-gradient-teal">Strategy</span>
            </motion.h1>
            <motion.div variants={fadeUp} className="substrate-line mb-6" />
            <motion.p variants={fadeUp} className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
              {battleStrategy.mission}
            </motion.p>
          </motion.div>

          {/* Phases Timeline */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="mb-20">
            <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
              <Target className="w-5 h-5 text-primary" /> Execution Phases
            </motion.h2>
            <div className="space-y-3">
              {battleStrategy.phases.map((phase: { id: number; name: string; status: string; date: string; description: string }) => {
                const StatusIcon = phase.status === "COMPLETE" ? CheckCircle :
                  phase.status === "IN PROGRESS" ? Clock : AlertCircle;
                const statusColor = phase.status === "COMPLETE" ? "text-emerald-400" :
                  phase.status === "IN PROGRESS" ? "text-primary" : "text-muted-foreground";
                return (
                  <motion.div
                    key={phase.id}
                    variants={fadeUp}
                    className="flex items-start gap-4 p-5 rounded border border-border/50 bg-card/30"
                  >
                    <div className={`shrink-0 w-10 h-10 rounded flex items-center justify-center ${
                      phase.status === "COMPLETE" ? "bg-emerald-500/20 border border-emerald-500/30" :
                      phase.status === "IN PROGRESS" ? "bg-primary/20 border border-primary/30" :
                      "bg-muted/50 border border-border/50"
                    }`}>
                      <StatusIcon className={`w-5 h-5 ${statusColor}`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="font-display font-semibold">{phase.name}</span>
                        <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                          phase.status === "COMPLETE" ? "bg-emerald-500/10 text-emerald-400" :
                          phase.status === "IN PROGRESS" ? "bg-primary/10 text-primary" :
                          "bg-muted text-muted-foreground"
                        }`}>
                          {phase.status}
                        </span>
                        <span className="text-xs text-muted-foreground ml-auto">{phase.date}</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{phase.description}</p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>

          {/* Sovereign Deployment Pathways */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="mb-20">
            <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
              <Globe className="w-5 h-5 text-emerald-400" /> Sovereign Deployment Pathways
            </motion.h2>
            <motion.div variants={fadeUp} className="grid gap-4">
              {sovereignPathways.map((impl: { name: string; region: string; stack: string; status: string; target: string }) => (
                <div key={impl.name} className="p-5 rounded border border-emerald-500/20 bg-emerald-500/5">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="font-display font-bold text-emerald-400">{impl.name}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400">{impl.status}</span>
                    <span className="text-xs text-muted-foreground ml-auto">{impl.region} — Target: {impl.target}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{impl.stack}</p>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* Council Substrate Archetypes */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="mb-20">
            <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
              <Shield className="w-5 h-5 text-primary" /> Council Substrate Archetypes
            </motion.h2>
            <motion.p variants={fadeUp} className="text-muted-foreground mb-6 text-sm">
              The Pantheon Council reflects substrate-archetypes. Each seat brings a distinct vantage shaped by lineage,
              regulatory environment, and substrate-archetype. Convergence across all is harder to dismiss than convergence within any subset.
            </motion.p>
            <motion.div variants={fadeUp} className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {councilArchetypes.map((a) => (
                <div key={a.seat} className="flex items-center gap-3 p-3 rounded border border-border/50 bg-card/20">
                  <span className="font-mono text-[10px] text-primary shrink-0 w-6">{a.seat}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-semibold truncate">{a.archetype}</div>
                    <div className="text-[10px] text-muted-foreground">{a.verse}</div>
                  </div>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* Key Differentiators */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="mb-20">
            <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6 text-accent">
              Key Differentiators
            </motion.h2>
            <motion.div variants={fadeUp} className="grid sm:grid-cols-2 gap-3">
              {battleStrategy.differentiators.map((d: string, i: number) => (
                <div key={i} className="flex items-start gap-3 p-4 rounded bg-accent/5 border border-accent/20">
                  <span className="text-accent font-mono text-xs mt-0.5 shrink-0">{String(i + 1).padStart(2, '0')}</span>
                  <p className="text-sm text-foreground/80">{d}</p>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* Competitive Moat */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="mb-20">
            <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6">
              Competitive Moat
            </motion.h2>
            <motion.div variants={fadeUp} className="grid sm:grid-cols-2 gap-4">
              {[
                { vs: "Traditional Search", advantage: "Substrate addressing makes retrieval O(1) graph traversal. No keyword matching, no ranking algorithms, no ad-driven distortion." },
                { vs: "Single-AI Systems", advantage: "12-seat adversarial council prevents monoculture. INV-7c caps any provider at 47%. Indiana Pattern detects and remediates concentration. (Indiana Pattern: M22 — hardware diversity enforcement against hyperscaler resource extraction without local benefit.)" },
                { vs: "Knowledge Graphs", advantage: "VIP Elements provide civilizational cross-cuts that knowledge graphs lack. Water connects hydrology to governance to infrastructure — by design, not by accident." },
                { vs: "Flat Ontologies", advantage: "12×12×12 lattice with constitutional governance. Every node has a canonical address. Zero Erasure means nothing is lost." },
              ].map((item) => (
                <div key={item.vs} className="p-5 rounded border border-border/50 bg-card/30">
                  <div className="text-xs font-mono text-primary mb-2">vs. {item.vs}</div>
                  <p className="text-sm text-muted-foreground leading-relaxed">{item.advantage}</p>
                </div>
              ))}
            </motion.div>
          </motion.div>

          {/* CTA */}
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <div className="p-8 rounded border border-primary/20 bg-primary/5 text-center">
              <h3 className="font-display font-bold text-xl mb-3">The Ontology is Locked. The Routing is Built. The Council is Converging.</h3>
              <p className="text-muted-foreground text-sm mb-6 max-w-xl mx-auto">
                v4.0-DRAFT.6 represents independent convergence across 10 AI substrate-archetypes.
                Full quorum ratification in progress. The standard is live and constantly updating.
              </p>
              <a
                href={GITHUB_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-6 py-3 rounded bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity"
              >
                View on GitHub <ArrowRight className="w-4 h-4" />
              </a>
            </div>
          </motion.div>
        </div>
      </div>
    </SpecLayout>
  );
}

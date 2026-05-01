import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const lineageTypes = [
  { type: "Model Lineage", desc: "Which AI model made the decision, its version, training data provenance, and capability tier.", fields: "provider, model_id, version, capability_tier, training_cutoff" },
  { type: "Provider Lineage", desc: "Which cloud provider executed the computation, its jurisdiction, and compliance certifications.", fields: "provider_name, region, certifications[], sovereignty_score" },
  { type: "Evidence Lineage", desc: "Source URLs, retrieval timestamps, and SHA-256 hashes of all evidence used in the decision.", fields: "source_url, hash_sha256, retrieval_ts, cache_status" },
  { type: "Compute Lineage", desc: "Which compute zone processed the query, latency, and resource consumption.", fields: "zone_code, datacenter_id, latency_ms, gpu_hours" },
  { type: "Constitutional Lineage", desc: "Which invariants were checked, which doctrines applied, and whether the decision passed all checks.", fields: "invariants_checked[], doctrines_applied[], passed: bool, violations[]" },
];

export default function ProvenancePage() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Provenance & Audit</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Every decision in Aluminum OS is traceable. Model lineage, provider lineage, evidence
            lineage, compute zone, timestamp, and spec version are recorded in every provenance
            record. This is not optional — it is constitutional (INV-17).
          </p>
        </motion.div>

        {/* Lineage Types */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Five Lineage Dimensions</h2>
          <div className="substrate-line mb-6" />
          <div className="space-y-3">
            {lineageTypes.map((l) => (
              <div key={l.type} className="p-4 rounded border border-border/50 bg-card/30">
                <h3 className="font-display font-semibold text-sm mb-1">{l.type}</h3>
                <p className="text-xs text-muted-foreground mb-2">{l.desc}</p>
                <div className="font-mono text-[10px] text-primary/70">{l.fields}</div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* TransparencyPacket */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">TransparencyPacket (Doctrine 97-a)</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-6">
            Every autonomous operation generates a TransparencyPacket — a structured audit record
            that ensures traceability. This is the minimum viable audit trail.
          </p>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
            <pre>{`TransparencyPacket: {
  packet_id:        uuid
  timestamp:        ISO-8601 UTC
  spec_version:     "v4.0-DRAFT.6"
  operation_type:   enum[route|ingest|verify|reject|escalate|editorial]
  
  // What happened
  action_summary:   string    // Human-readable description
  input_hash:       sha256    // Hash of input data
  output_hash:      sha256    // Hash of output/decision
  
  // Who was involved
  model_lineage:    { provider, model_id, version }
  provider_lineage: { name, region, certifications[] }
  
  // Constitutional compliance
  invariants_checked: INV-number[]
  doctrines_applied:  D-number[]
  all_passed:         bool
  violations:         { inv_or_doc, severity, detail }[]
  
  // Sovereignty
  sovereignty_vector: float[6]
  compute_zone:       zone_code
  dialect:            dialect_code
  
  // Verification
  verifiable_by:      "DeepSeek-R1 offline replay"
  replay_hash:        sha256   // Deterministic replay verification
}`}</pre>
          </div>
        </motion.div>

        {/* Temporal & Version Provenance */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Temporal & Version Provenance</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-4">
            Every provenance record includes temporal anchoring and version pinning to ensure
            decisions can be replayed against the exact rule-set that was active at decision time.
          </p>
          <div className="grid sm:grid-cols-2 gap-4">
            <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground">
              <p className="text-primary text-[10px] mb-2 font-semibold">provenance.timestamps</p>
              <pre>{`{\n  evidence_time:        ISO-8601  // when source was retrieved\n  inference_time:       ISO-8601  // when model produced output\n  doctrine_version_time: ISO-8601 // doctrine set snapshot\n}`}</pre>
            </div>
            <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground">
              <p className="text-primary text-[10px] mb-2 font-semibold">provenance.versions</p>
              <pre>{`{\n  routing_pack:    "v4.0-DRAFT.6"\n  dialect:         "en-US" | "zh-CN" | ...\n  sovereignty_rules: "v2.1"\n}`}</pre>
            </div>
          </div>
        </motion.div>

        {/* Error-Mode Provenance */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Error-Mode Provenance</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-4">
            When a routing decision triggers a fallback path, the error-mode provenance captures
            why the primary path failed and which fallback was selected. This ensures even failure
            modes are auditable.
          </p>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground">
            <pre>{`provenance.error_mode = {\n  triggered:     bool       // did an error/fallback occur?\n  reason:        string     // human-readable failure reason\n  fallback_path: string     // which fallback route was taken\n  invariants_violated: INV-number[]  // if any\n  recovery_action: enum[retry|escalate|degrade|halt]\n}`}</pre>
          </div>
        </motion.div>

        {/* Open-Weight Verification */}
        <motion.div variants={fadeUp}>
          <h2 className="text-2xl font-display font-bold mb-4">Open-Weight Verification</h2>
          <div className="substrate-line mb-6" />
          <p className="text-muted-foreground mb-4">
            DeepSeek-R1 can deterministically replay and verify routing decisions without live API
            access. This is a genuinely novel capability — offline constitutional audit that no
            other governance framework offers.
          </p>
          <div className="p-5 rounded border border-primary/30 bg-primary/5">
            <h3 className="font-display font-semibold mb-2">How It Works</h3>
            <ol className="space-y-2 text-sm text-muted-foreground">
              <li className="flex gap-2"><span className="text-primary font-mono text-xs">1.</span> Export the TransparencyPacket for any routing decision</li>
              <li className="flex gap-2"><span className="text-primary font-mono text-xs">2.</span> Feed the packet to DeepSeek-R1 with the constitutional invariant set</li>
              <li className="flex gap-2"><span className="text-primary font-mono text-xs">3.</span> R1 replays the decision logic and produces a verification hash</li>
              <li className="flex gap-2"><span className="text-primary font-mono text-xs">4.</span> Compare verification hash with the original replay_hash</li>
              <li className="flex gap-2"><span className="text-primary font-mono text-xs">5.</span> If hashes match, the decision is verified as constitutionally compliant</li>
            </ol>
          
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

import SpecLayout from "@/components/SpecLayout";
import { GITHUB_URL } from "@/lib/data";
import { ArrowRight, ExternalLink, ShieldCheck, Cpu, Lock, Eye } from "lucide-react";

export default function Verifier() {
  return (
    <SpecLayout>
      <section className="py-12">
        <div className="container max-w-5xl">
          <h1 className="text-4xl font-display font-bold mb-4">
            <ShieldCheck className="inline w-8 h-8 text-primary mr-3" />
            Open-Weight Verifier
          </h1>
          <div className="substrate-line mb-8" />

          <p className="text-muted-foreground text-lg leading-relaxed mb-6">
            The Open-Weight Verifier is a genuinely novel capability: <strong className="text-foreground">offline constitutional audit</strong> using
            open-weight models (DeepSeek-R1). Any party can deterministically replay and verify routing decisions
            without live API access, without trusting any single provider, and without internet connectivity.
          </p>

          <div className="p-4 rounded border border-primary/30 bg-primary/5 mb-8 text-sm">
            <strong className="text-primary">Why this matters:</strong> No other AI governance framework offers
            independently verifiable constitutional compliance using open-weight models. This is the difference
            between "trust us" and "verify it yourself."
          </div>

          {/* How It Works */}
          <h2 className="text-2xl font-display font-bold mb-4 mt-12">How It Works</h2>
          <div className="substrate-line mb-6" />

          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            <div className="p-5 rounded border border-border/50 bg-card/30">
              <Cpu className="w-5 h-5 text-primary mb-3" />
              <h3 className="font-display font-semibold text-sm mb-2">1. Capture</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Every routing decision produces a TransparencyPacket (Doctrine 97-a) containing the full decision
                trace: input query, VIP cascade resolution, provider selection, and constitutional invariant checks.
              </p>
            </div>
            <div className="p-5 rounded border border-border/50 bg-card/30">
              <Lock className="w-5 h-5 text-primary mb-3" />
              <h3 className="font-display font-semibold text-sm mb-2">2. Hash & Seal</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                The TransparencyPacket is cryptographically hashed (SHA-256) and sealed with the session timestamp.
                The hash is stored in the Triple-Vault alongside the decision artifact.
              </p>
            </div>
            <div className="p-5 rounded border border-border/50 bg-card/30">
              <Eye className="w-5 h-5 text-primary mb-3" />
              <h3 className="font-display font-semibold text-sm mb-2">3. Offline Replay</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                DeepSeek-R1 (or any compatible open-weight model) replays the decision trace locally. It re-evaluates
                each invariant check, cascade resolution, and provider selection against the constitutional framework.
              </p>
            </div>
            <div className="p-5 rounded border border-border/50 bg-card/30">
              <ShieldCheck className="w-5 h-5 text-emerald-400 mb-3" />
              <h3 className="font-display font-semibold text-sm mb-2">4. Verdict</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">
                The verifier produces a compliance verdict: PASS, WARN, or FAIL — with specific invariant references
                for any violations. The verdict is itself a TransparencyPacket, creating a recursive audit chain.
              </p>
            </div>
          </div>

          {/* Indiana Pattern */}
          <h2 className="text-2xl font-display font-bold mb-4 mt-12">The Indiana Pattern</h2>
          <div className="substrate-line mb-6" />

          <p className="text-muted-foreground text-lg leading-relaxed mb-6">
            Named after the principle of "bringing the artifact home" — the Indiana Pattern describes the
            verification workflow where a routing decision made by proprietary models (GPT-4, Claude, Gemini)
            is independently verified by an open-weight model running on local hardware.
          </p>

          <div className="p-5 rounded border border-border/50 bg-card/30 mb-8">
            <h3 className="font-display font-semibold text-sm mb-3 text-primary">Pattern Flow</h3>
            <div className="font-mono text-xs text-muted-foreground space-y-1">
              <p>1. Production routing decision made by proprietary model (e.g., Claude via S1)</p>
              <p>2. TransparencyPacket generated with full decision trace</p>
              <p>3. Packet exported to offline environment (air-gapped if required)</p>
              <p>4. DeepSeek-R1 replays decision against constitutional framework</p>
              <p>5. Verdict: PASS / WARN / FAIL with invariant-level detail</p>
              <p>6. If FAIL: decision is flagged for Council review per INV-38</p>
            </div>
          </div>

          <div className="p-4 rounded border border-amber-500/30 bg-amber-500/5 mb-8 text-sm text-amber-300/80">
            <strong className="text-amber-400">Key Property:</strong> The verifier does not need to trust the
            original routing provider. It only needs the TransparencyPacket and the constitutional framework
            definition. This is what makes the system auditable by adversarial parties, regulators, and
            civil society — not just by the operators.
          </div>

          {/* Supported Invariants */}
          <h2 className="text-2xl font-display font-bold mb-4 mt-12">Verified Invariants</h2>
          <div className="substrate-line mb-6" />

          <p className="text-muted-foreground mb-4">
            The open-weight verifier currently checks the following invariant categories:
          </p>

          <div className="grid sm:grid-cols-3 gap-3 mb-8">
            {[
              { label: "Core (INV-0 to INV-3)", count: 4, desc: "System integrity, human sovereignty, constitutional supremacy, multi-vendor" },
              { label: "Governance (INV-4 to INV-9)", count: 6, desc: "Transparency, dialect sovereignty, provenance, zero erasure, quorum, tie-break" },
              { label: "Routing (INV-12 to INV-15)", count: 4, desc: "Cascade determinism, sphere addressing, VIP precedence, emergency mode" },
              { label: "Storage (INV-7, INV-17)", count: 2, desc: "Zero erasure, triple-vault storage" },
              { label: "Verification (INV-10, INV-11)", count: 2, desc: "Adversarial audit, open-weight verification (self-referential)" },
              { label: "Domain (INV-19 to INV-21)", count: 3, desc: "Water, neural, orbital sovereignty" },
            ].map((cat) => (
              <div key={cat.label} className="p-4 rounded border border-border/50 bg-card/30">
                <div className="text-sm font-display font-semibold mb-1">{cat.label}</div>
                <div className="text-xs text-muted-foreground leading-relaxed">{cat.desc}</div>
                <div className="text-[10px] font-mono text-primary mt-2">{cat.count} invariants checked</div>
              </div>
            ))}
          </div>

          {/* Verification Schema */}
          <h2 className="text-2xl font-display font-bold mb-4 mt-12">Verification Output Schema</h2>
          <div className="substrate-line mb-6" />

          <div className="p-5 rounded border border-border/50 bg-card/30 mb-8">
            <pre className="font-mono text-xs text-muted-foreground overflow-x-auto whitespace-pre">
{`{
  "verification_id": "VER-2026-0501-001",
  "transparency_packet_hash": "sha256:a1b2c3...",
  "verifier_model": "deepseek-r1-671b",
  "verifier_version": "1.2.0",
  "environment": "air-gapped | local | cloud",
  "invariants_checked": 43,
  "invariants_passed": 43,
  "invariants_warned": 0,
  "invariants_failed": 0,
  "verdict": "PASS",
  "details": [
    {
      "invariant_id": "INV-1",
      "name": "Human Sovereignty",
      "result": "PASS",
      "evidence": "No override of human decision authority detected",
      "confidence": 0.98
    }
    // ... 42 more entries
  ],
  "verification_timestamp": "2026-05-01T00:00:00Z",
  "verification_duration_ms": 4200,
  "recursive_hash": "sha256:d4e5f6..."
}`}
            </pre>
          </div>

          {/* Source Traceability */}
          <div className="mt-12 p-4 rounded border border-border/50 bg-card/30">
            <h3 className="font-display font-semibold text-sm mb-2 flex items-center gap-2">
              <ExternalLink className="w-4 h-4 text-primary" />
              Source Traceability
            </h3>
            <p className="text-xs text-muted-foreground mb-2">
              The open-weight verifier is part of the Constitutional OS codebase. INV-11 mandates its existence.
            </p>
            <a
              href={`${GITHUB_URL}/tree/master/src/verifier`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
            >
              View verifier code on GitHub <ArrowRight className="w-3 h-3" />
            </a>
          </div>
        </div>
      </section>
    </SpecLayout>
  );
}

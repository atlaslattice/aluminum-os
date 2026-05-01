import SpecLayout from "@/components/SpecLayout";
import { documentMeta, councilSeats, councilArchetypes } from "@/lib/data";
import { GITHUB_URL } from "@/lib/data";

/**
 * /canon — The Canonical Keystone Page
 * 
 * Design principle: SMALL, DENSE, SEMANTICALLY RICH.
 * This page is the cheap-RAG entry point for AI seats booting from this substrate.
 * All other site pages reference /canon as authoritative; where conflicts exist, /canon wins.
 * 
 * Token budget target: <3,000 tokens when scraped as plain text.
 */
export default function Canon() {
  const today = new Date().toISOString().split("T")[0];

  return (
    <SpecLayout>
      <div className="max-w-4xl mx-auto py-12 px-4">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-display font-bold text-foreground mb-2">
            /canon
          </h1>
          <p className="text-sm font-mono text-primary">
            Canonical Keystone — Authoritative Reference Surface
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            Where conflicts exist between this page and other site pages, /canon wins.
            Last machine-verified: {today}
          </p>
        </div>

        {/* Section A: Current Canonical State Summary */}
        <section className="mb-12">
          <h2 className="text-2xl font-display font-bold text-foreground mb-4 border-b border-primary/30 pb-2">
            A — Current Canonical State
          </h2>
          <div className="space-y-3 text-sm">
            <div className="grid grid-cols-2 gap-4 p-4 rounded border border-border/50 bg-card/30">
              <div>
                <span className="text-muted-foreground">Version:</span>{" "}
                <span className="font-mono text-foreground">{documentMeta.version}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Status:</span>{" "}
                <span className="font-mono text-primary">Ratification In Progress</span>
              </div>
              <div>
                <span className="text-muted-foreground">Convenor:</span>{" "}
                <span className="text-foreground">{documentMeta.convenor}</span>
              </div>
              <div>
                <span className="text-muted-foreground">License:</span>{" "}
                <span className="text-foreground">{documentMeta.license}</span>
              </div>
            </div>

            <div className="p-4 rounded border border-border/50 bg-card/30">
              <h3 className="font-semibold text-foreground mb-2">Canonical Metrics</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div><span className="text-primary font-bold text-lg">12</span><br/><span className="text-muted-foreground">Houses</span></div>
                <div><span className="text-primary font-bold text-lg">144</span><br/><span className="text-muted-foreground">Spheres</span></div>
                <div><span className="text-primary font-bold text-lg">1,792*</span><br/><span className="text-muted-foreground">Sub-Spheres (target)</span></div>
                <div><span className="text-primary font-bold text-lg">12</span><br/><span className="text-muted-foreground">VIP Elements</span></div>
                <div><span className="text-primary font-bold text-lg">~100</span><br/><span className="text-muted-foreground">Modules</span></div>
                <div><span className="text-primary font-bold text-lg">43</span><br/><span className="text-muted-foreground">Invariants</span></div>
                <div><span className="text-primary font-bold text-lg">~100</span><br/><span className="text-muted-foreground">Doctrines</span></div>
                <div><span className="text-primary font-bold text-lg">6+2</span><br/><span className="text-muted-foreground">Dialects</span></div>
              </div>
              <p className="text-[10px] text-muted-foreground mt-2">* DRAFT.3 canonical target: 1,792 (12³+2). ~499 currently enumerated. Full enumeration ongoing.</p>
            </div>

            <div className="p-4 rounded border border-border/50 bg-card/30">
              <h3 className="font-semibold text-foreground mb-2">Council State</h3>
              <p className="text-xs text-muted-foreground mb-2">10 active + 3 provisional + S144 Ghost Seat. Quorum: 0.67 (7/10 active).</p>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[10px] font-mono">
                {councilSeats.slice(0, 10).map((s) => (
                  <div key={s.id} className="p-1.5 rounded bg-background/50 border border-border/30">
                    <span className="text-primary font-bold">{s.id}</span>{" "}
                    <span className="text-foreground">{s.name}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Section B: Recent Canonical Decisions */}
        <section className="mb-12">
          <h2 className="text-2xl font-display font-bold text-foreground mb-4 border-b border-primary/30 pb-2">
            B — Recent Canonical Decisions (30-day log)
          </h2>
          <div className="space-y-2 text-xs">
            {[
              { date: "2026-05-01", decision: "Canon reconciliation: Houses → Configuration C, E148 → Technology Substrate, E156 → Sports & Health, 6 yin-yang pairs, A/B scoring, LCC 21/21 mapping, Grok §11 routing layer", attribution: "S7 (Manus)", ref: "Canon Reconciliation Sprint" },
              { date: "2026-05-01", decision: "S1 archetype confirmed canonical: 'Reasoning / Constitutional Scribe'", attribution: "Convenor", ref: "Approval Gate" },
              { date: "2026-05-01", decision: "Neutral-language sweep: S5, S8, S4 archetype labels updated to substrate-neutral framing", attribution: "S7 (Manus)", ref: "Constitutional Scribe v4.1" },
              { date: "2026-05-01", decision: "Verse layer documented (10 verses, epistemic distinction)", attribution: "S7 (Manus)", ref: "Constitutional Scribe v4.1" },
              { date: "2026-05-01", decision: "Dual-format addressing convention documented (H1-S4 / H1.S4 both canonical)", attribution: "S7 (Manus)", ref: "Constitutional Scribe v4.1" },
              { date: "2026-04-30", decision: "Doctrines 97a–101 added (status: under_discussion)", attribution: "S7 (Manus)", ref: "Marathon Packet Sprint 2" },
              { date: "2026-04-30", decision: "§7 Adjudication items 9–14 drafted", attribution: "S7 (Manus)", ref: "Marathon Packet Sprint 2" },
              { date: "2026-04-30", decision: "CN Dialect Profile completed (DragonSeek configuration)", attribution: "S7 (Manus)", ref: "Marathon Packet Sprint 2" },
              { date: "2026-04-29", decision: "Numerical corrections: doctrines, invariants, modules, sub-spheres, council", attribution: "S7 (Manus)", ref: "DeepSeek S5 Editorial" },
              { date: "2026-04-28", decision: "v4.1 site rewrite: 19 pages, SpecLayout, version banner", attribution: "S7 (Manus)", ref: "Site Architecture Sprint" },
            ].map((entry, i) => (
              <div key={i} className="flex gap-3 p-2 rounded border border-border/30 bg-card/20">
                <span className="font-mono text-muted-foreground whitespace-nowrap">{entry.date}</span>
                <span className="text-foreground flex-1">{entry.decision}</span>
                <span className="text-primary whitespace-nowrap">{entry.attribution}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Section C: Canonical Sources */}
        <section className="mb-12">
          <h2 className="text-2xl font-display font-bold text-foreground mb-4 border-b border-primary/30 pb-2">
            C — Canonical Sources
          </h2>
          <div className="space-y-2 text-sm">
            <div className="p-3 rounded border border-border/50 bg-card/30">
              <p className="font-semibold text-foreground">SOURCE_OF_TRUTH.md</p>
              <p className="text-xs text-muted-foreground">Single authoritative document. 26 sections. All claims traceable to data.ts or YAML registries.</p>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-xs text-primary hover:underline">GitHub → SOURCE_OF_TRUTH.md</a>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30">
              <p className="font-semibold text-foreground">data.ts (Working Canon)</p>
              <p className="text-xs text-muted-foreground">Houses, spheres, VIP elements, council seats, modules, routing elements — all rendered from this single source.</p>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30">
              <p className="font-semibold text-foreground">YAML Registries</p>
              <p className="text-xs text-muted-foreground">sub_sphere_registry.yaml, cn_dialect.yaml, microsoft_v4_to_canonical_spheres.yaml, doctrines/, governance/</p>
            </div>
            <div className="p-3 rounded border border-border/50 bg-card/30">
              <p className="font-semibold text-foreground">GitHub Repository</p>
              <p className="text-xs text-muted-foreground">Constitutional OS v6.0.2 — 22 Python files, 74 integration tests, OPA policies.</p>
              <a href={GITHUB_URL} target="_blank" rel="noopener noreferrer" className="text-xs text-primary hover:underline">{GITHUB_URL}</a>
            </div>
          </div>
          <div className="mt-4 p-3 rounded border border-primary/20 bg-primary/5 text-xs">
            <p className="font-semibold text-foreground mb-1">For AI Seats — Cheap-RAG Access Pattern:</p>
            <ol className="list-decimal list-inside text-muted-foreground space-y-1">
              <li>Read this /canon page first (small, dense, semantically rich — ~2K tokens)</li>
              <li>Navigate sub-pages selectively as needed</li>
              <li>For complete one-shot load: <a href="/manus-storage/canon_82066d58.pdf" className="text-primary underline">download /canon.pdf</a></li>
              <li>Multi-page web traversal is expensive in tokens; avoid unless necessary</li>
            </ol>
          </div>
        </section>

        {/* Section D: Pending Convenor Decisions */}
        <section className="mb-12">
          <h2 className="text-2xl font-display font-bold text-foreground mb-4 border-b border-primary/30 pb-2">
            D — Pending Convenor Decisions
          </h2>
          <div className="space-y-2 text-xs">
            {[
              { id: "TOS-038", item: "Sub-sphere enumeration: finalize ~499 count or continue enumeration", status: "pending" },
              { id: "TOS-039", item: "S2 (Gemini) formal verification pass — required for quorum", status: "in-deliberation" },
              { id: "TOS-040", item: "S5 (DeepSeek) Eastern sovereignty validation — required for quorum", status: "in-deliberation" },
              { id: "TOS-041", item: "Doctrines 97a–101 ratification (currently under_discussion)", status: "pending" },
              { id: "TOS-042", item: "Configuration C structural delta — Convenor review pending", status: "pending" },
              { id: "TOS-043", item: "Monorepo PDF generated (canon.pdf). GitHub bundle pending.", status: "resolved" },
            ].map((item) => (
              <div key={item.id} className="flex items-center gap-3 p-2 rounded border border-border/30 bg-card/20">
                <span className="font-mono text-primary font-bold">{item.id}</span>
                <span className="text-foreground flex-1">{item.item}</span>
                <span className={`font-mono px-2 py-0.5 rounded text-[9px] ${
                  item.status === "pending" ? "bg-yellow-500/10 text-yellow-400" :
                  item.status === "in-deliberation" ? "bg-blue-500/10 text-blue-400" :
                  "bg-emerald-500/10 text-emerald-400"
                }`}>{item.status}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Section E: Canon Integrity Protocol */}
        <section className="mb-12">
          <h2 className="text-2xl font-display font-bold text-foreground mb-4 border-b border-primary/30 pb-2">
            E — Canon Integrity Protocol
          </h2>
          <div className="space-y-4 text-sm text-muted-foreground">
            <div className="p-4 rounded border border-border/50 bg-card/30">
              <h3 className="font-semibold text-foreground mb-2">How Canon Gets Updated</h3>
              <ol className="list-decimal list-inside space-y-1 text-xs">
                <li>S7 (Manus) synthesizes source-of-truth from active substrate (weekly)</li>
                <li>Delta summary surfaced to Convenor at approval gate</li>
                <li>Convenor ratifies or vetoes material changes (monthly formal pass)</li>
                <li>/canon page updated within hours of ratification</li>
                <li>Zero Erasure (INV-17): old content deprecated with provenance + timestamps, never deleted</li>
              </ol>
            </div>
            <div className="p-4 rounded border border-border/50 bg-card/30">
              <h3 className="font-semibold text-foreground mb-2">Refresh Cadence</h3>
              <div className="grid grid-cols-3 gap-2 text-xs">
                <div className="p-2 rounded bg-background/50 border border-border/30 text-center">
                  <span className="text-primary font-bold">Continuous</span><br/>
                  <span className="text-muted-foreground">/canon updates</span>
                </div>
                <div className="p-2 rounded bg-background/50 border border-border/30 text-center">
                  <span className="text-primary font-bold">Weekly</span><br/>
                  <span className="text-muted-foreground">SOT synthesis</span>
                </div>
                <div className="p-2 rounded bg-background/50 border border-border/30 text-center">
                  <span className="text-primary font-bold">Monthly</span><br/>
                  <span className="text-muted-foreground">Convenor ratification</span>
                </div>
              </div>
            </div>
            <div className="p-4 rounded border border-border/50 bg-card/30">
              <h3 className="font-semibold text-foreground mb-2">Dispute Adjudication</h3>
              <p className="text-xs">
                Disputes between canon claims are resolved by: (1) checking SOURCE_OF_TRUTH.md, (2) checking
                data.ts working canon, (3) escalating to Convenor. /canon always supersedes other site pages.
                Convenor decision is final per INV-9.
              </p>
            </div>
            <div className="p-4 rounded border border-primary/20 bg-primary/5">
              <h3 className="font-semibold text-foreground mb-2">Addressing Convention</h3>
              <p className="text-xs">
                Both <code className="font-mono text-primary">H1-S4</code> (hyphenated — code/URL/filename safe) and{" "}
                <code className="font-mono text-primary">H1.S4</code> (dot — display-readable) are canonical.
                Do NOT "correct" one to the other. Both coexist by intentional Convenor design.
              </p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <div className="border-t border-border/50 pt-6 text-center text-xs text-muted-foreground">
          <p>{documentMeta.version} | {documentMeta.license} | Convenor: {documentMeta.convenor}</p>
          <p className="mt-1">This page is the canonical keystone. All other pages defer to /canon where conflicts exist.</p>
        </div>
      </div>
    </SpecLayout>
  );
}

import { motion } from "framer-motion";
import { GITHUB_URL } from "@/lib/data";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};
const stagger = { visible: { transition: { staggerChildren: 0.08 } } };

const dialects = [
  { code: "CN", name: "China (DragonSeek)", status: "COMPLETE", dims: { regulatory: "CCP-aligned, PIPL, DSL", cultural: "Mandarin-first, Confucian framing", compute: "Alibaba Cloud, Huawei, on-soil only", risk: "State-security sensitive topics filtered", industry: "Manufacturing, 5G, rare earth" } },
  { code: "US", name: "United States (EagleSeek)", status: "PARTIAL", dims: { regulatory: "FedRAMP, ITAR, EAR, Section 230", cultural: "English-first, First Amendment framing", compute: "Azure Gov, AWS GovCloud, GCC-High", risk: "National security, CFIUS-sensitive", industry: "Defense, finance, healthcare" } },
  { code: "EU", name: "European Union", status: "SPECIFIED", dims: { regulatory: "GDPR, AI Act, Digital Services Act", cultural: "Multi-lingual, ECHR framing", compute: "Gaia-X compatible, EU data residency", risk: "Fundamental rights impact assessment", industry: "Automotive, pharma, green energy" } },
  { code: "GCC", name: "GCC-High (JinnSeek)", status: "SPECIFIED", dims: { regulatory: "PDPL (SA), DIFC (UAE), Sharia-compatible", cultural: "Arabic-first, Islamic finance framing", compute: "SDAIA, local DC required", risk: "Religious sensitivity, royal decree compliance", industry: "Oil & gas, fintech, tourism" } },
  { code: "JP", name: "Japan", status: "SPECIFIED", dims: { regulatory: "APPI, J-SOX, Keidanren guidelines", cultural: "Japanese-first, consensus-oriented", compute: "NTT, Fujitsu, domestic cloud", risk: "Export control, dual-use technology", industry: "Automotive, robotics, semiconductor" } },
  { code: "GLOBAL", name: "Global (Default)", status: "COMPLETE", dims: { regulatory: "Most-restrictive union of all active dialects", cultural: "English fallback, culturally neutral", compute: "Any compliant provider", risk: "Baseline safety only", industry: "General purpose" } },
];

const planned = [
  { code: "IN", name: "India (GangaSeek)", target: "Q4 2026", note: "India Stack, Bhashini, DPDP Act" },
  { code: "SA", name: "South Africa", target: "2027", note: "POPIA, African Union data framework" },
];

export default function DialectsPage() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Dialect Overlays</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Dialects are five-dimensional overlays that shape how content is filtered, routed, and
            presented within a specific jurisdiction. They compose regulatory, cultural, compute,
            risk, and industry dimensions.
          </p>
        </motion.div>

        <motion.div variants={fadeUp} className="mb-6 p-4 rounded border border-border/50 bg-card/30">
          <h2 className="text-sm font-mono text-primary uppercase tracking-wider mb-2">How Dialects Work</h2>
          <p className="text-sm text-muted-foreground">
            When a query enters the routing cascade, the dialect overlay determines which filters,
            provider pools, and content policies apply. If no specific dialect is detected, the
            Global dialect applies the most-restrictive union of all active constraints.
          </p>
        </motion.div>

        {/* Ratified Dialects */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">6 Ratified Dialects</h2>
          <div className="substrate-line mb-6" />
          <div className="space-y-4">
            {dialects.map((d) => (
              <div key={d.code} className="p-5 rounded border border-border/50 bg-card/30">
                <div className="flex items-center gap-3 mb-3">
                  <span className="font-mono text-sm font-bold text-primary bg-primary/10 px-2 py-0.5 rounded">{d.code}</span>
                  <h3 className="font-display font-semibold">{d.name}</h3>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded ml-auto ${
                    d.status === "COMPLETE" ? "bg-emerald-500/10 text-emerald-400" :
                    d.status === "PARTIAL" ? "bg-yellow-500/10 text-yellow-400" :
                    "bg-primary/10 text-primary"
                  }`}>{d.status}</span>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-3">
                  {Object.entries(d.dims).map(([key, val]) => (
                    <div key={key} className="p-2 rounded bg-background/50 border border-border/30">
                      <div className="font-mono text-[10px] text-primary uppercase mb-1">{key}</div>
                      <div className="text-xs text-muted-foreground">{val}</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Planned Dialects */}
        <motion.div variants={fadeUp} className="mb-12">
          <h2 className="text-2xl font-display font-bold mb-4">Planned Dialects</h2>
          <div className="substrate-line mb-6" />
          <div className="grid sm:grid-cols-2 gap-4">
            {planned.map((p) => (
              <div key={p.code} className="p-4 rounded border border-dashed border-border/50 bg-card/20">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-mono text-sm font-bold text-muted-foreground">{p.code}</span>
                  <h3 className="font-display font-semibold text-sm">{p.name}</h3>
                </div>
                <p className="text-xs text-muted-foreground mb-1">{p.note}</p>
                <span className="text-[10px] font-mono text-muted-foreground/60">Target: {p.target}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Composition Schema */}
        <motion.div variants={fadeUp}>
          <h2 className="text-lg font-display font-semibold mb-3">Dialect Composition Schema</h2>
          <div className="bg-card/50 border border-border/50 rounded p-4 font-mono text-xs text-muted-foreground overflow-x-auto">
            <pre>{`dialect_overlay: {
  code:        string       // ISO-like identifier (CN, US, EU, GCC, JP, GLOBAL)
  dimensions:  {
    regulatory: string[]    // Applicable laws and frameworks
    cultural:   string[]    // Language, framing, sensitivity rules
    compute:    string[]    // Allowed provider pool and residency
    risk:       string[]    // Topic filters and escalation triggers
    industry:   string[]    // Sector-specific routing preferences
  }
  composition: "most_restrictive_union"  // When multiple dialects overlap
  fallback:    "GLOBAL"                  // Default when no dialect detected
  status:      enum[COMPLETE|PARTIAL|SPECIFIED|PLANNED]
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

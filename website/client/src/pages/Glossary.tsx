import { motion } from "framer-motion";
import SpecLayout from "@/components/SpecLayout";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.05 } },
};

interface GlossaryEntry {
  term: string;
  definition: string;
  context?: string;
  see?: string;
}

const glossary: GlossaryEntry[] = [
  {
    term: "Activation Lifecycle",
    definition: "The progression a specification component follows before becoming canonical: draft → simulated → shadow → limited activation → ratified.",
    context: "No component reaches production without passing through all five stages. Shadow mode runs alongside live traffic without affecting outputs.",
    see: "/simulation",
  },
  {
    term: "Cascade",
    definition: "A priority-ordered routing mechanism that resolves conflicts when a query touches multiple substrates, dialects, or sovereignty vectors simultaneously.",
    context: "The VIP Cascade determines which Element takes precedence. The 5-tier priority is: Safety → Sovereignty → Governance → Provenance → Performance.",
    see: "/elements",
  },
  {
    term: "Compute Zone",
    definition: "A geographic or jurisdictional boundary within which specific routing rules, provider pools, and sovereignty constraints apply.",
    context: "Three special zones exist: Mixed-Compliance (overlapping jurisdictions), Contested (disputed sovereignty), and Low-Power/Emergency (degraded capacity).",
    see: "/compute-zones",
  },
  {
    term: "Council (Pantheon Council)",
    definition: "The 10+3+1 governance body responsible for ratifying doctrines, invariants, and spec changes. 10 active seats (S1–S10), 3 provisional, 1 Ghost Seat (S144).",
    context: "Quorum requires 0.67 of active seats. Convenor (human) holds tie-break (INV-9) and veto (Doctrine 101). No AI entity holds unilateral authority.",
    see: "/governance",
  },
  {
    term: "Dialect",
    definition: "A five-dimensional overlay (regulatory, cultural, compute, risk, industry) that shapes how content is filtered, routed, and presented within a specific jurisdiction or context.",
    context: "6 ratified: US, EU, CN, GCC-High, JP, Global. 2 planned: IN, SA. The CN dialect is fully specified; US is partial.",
    see: "/dialects",
  },
  {
    term: "Doctrine",
    definition: "A governance rule ratified by the Council that constrains system behavior. ~101 doctrines exist (D-1 through D-95 ratified + D-96 through D-101 under discussion).",
    context: "Doctrines can be amended by Council vote. Invariants cannot. Doctrines are the 'laws'; invariants are the 'constitution'.",
    see: "/doctrines",
  },
  {
    term: "Element (VIP Element)",
    definition: "One of 12 civilizational substrates (E145–E156) that cross-cut all 12 Houses. Not knowledge categories, but the physical and institutional infrastructure that makes knowledge production possible.",
    context: "Water, Energy, AI, Governance, Security, Economics, Compute, Provenance, Education, Health, Climate, and the Meta-Orchestrator.",
    see: "/elements",
  },
  {
    term: "Indiana Pattern",
    definition: "The failure mode where data center hyperscaler operations extract local water, energy, and community resources without local benefit. Named for siting concerns at Project Rainier (Indiana).",
    context: "The Indiana Pattern is the canonical example of why VIP Element E145 (Water) exists as a cross-cutting substrate. When compute infrastructure consumes local resources at scale, the sovereignty gradient must account for community impact — not just jurisdictional compliance.",
    see: "/sovereignty",
  },
  {
    term: "House",
    definition: "One of 12 top-level knowledge domains in the ontology. Each House contains exactly 12 Spheres, for 144 total.",
    context: "Houses represent broad disciplinary categories. The 12×12 structure ensures every knowledge domain has a canonical address.",
    see: "/lattice",
  },
  {
    term: "Invariant",
    definition: "A constitutional constraint that cannot be overridden by any Council vote, doctrine, or system update. 43 total: 40 base (INV-0 through INV-39) + 3 domain-specific.",
    context: "INV-1 (Human Sovereignty) is absolute. INV-7c caps any single provider at 47%/60%. INV-9 grants Convenor tie-break authority.",
    see: "/governance",
  },
  {
    term: "Shadow Mode",
    definition: "An activation stage where a new component runs alongside live traffic, receiving real inputs and producing outputs, but those outputs are logged rather than served to users.",
    context: "Shadow mode allows verification of correctness and performance without risk. A component must pass shadow mode before limited activation.",
    see: "/simulation",
  },
  {
    term: "Sovereignty Vector",
    definition: "A six-dimensional assessment (legal, data, compute, economic, provenance, operational) that scores every routing decision's sovereignty implications.",
    context: "Enables sovereign deployment pathways. Each dimension is independently scored, allowing fine-grained sovereignty compliance.",
    see: "/sovereignty",
  },
  {
    term: "Sphere",
    definition: "A second-level knowledge domain within a House. Each House contains exactly 12 Spheres. Sub-spheres (tier-2) provide further granularity (~499 enumerated to date).",
    context: "Spheres have canonical addresses (e.g., H3.S7 = House 3, Sphere 7). Sub-sphere enumeration is ongoing.",
    see: "/lattice",
  },
  {
    term: "TransparencyPacket",
    definition: "A structured audit record generated by every autonomous operation (ingestion, routing, editorial pass). Contains timestamp, source, action taken, constitutional compliance status, and provenance hash.",
    context: "Required by Doctrine 97-a. Ensures every autonomous action is traceable and auditable. Implements INV-7c compliance logging.",
    see: "/provenance",
  },
  {
    term: "VIP Substrate",
    definition: "See 'Element (VIP Element)'. The term 'VIP' refers to the priority status of these substrates in the routing cascade — they take precedence over domain-specific routing.",
    context: "VIP stands for the cascade priority, not 'Very Important Person'. These are the civilizational substrates that make all other knowledge production possible.",
    see: "/elements",
  },
];

export default function Glossary() {
  return (
    <SpecLayout>
      <motion.div initial="hidden" animate="visible" variants={stagger}>
        <motion.div variants={fadeUp} className="mb-8">
          <h1 className="text-4xl font-display font-bold mb-2">
            <span className="text-gradient-teal">Glossary</span>
          </h1>
          <p className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
            Canonical definitions for all terms used in the Aluminum OS specification.
            This glossary is machine-readable and LLM-parsable.
          </p>
        </motion.div>

        <motion.div variants={fadeUp} className="mb-8 p-4 rounded border border-border/50 bg-card/30">
          <h2 className="text-sm font-mono text-primary uppercase tracking-wider mb-2">How to Read This Spec</h2>
          <ul className="text-sm text-muted-foreground space-y-1.5">
            <li>• <strong className="text-foreground/80">Invariants</strong> are constitutional — they cannot be changed by any vote.</li>
            <li>• <strong className="text-foreground/80">Doctrines</strong> are governance rules — they can be amended by Council supermajority.</li>
            <li>• <strong className="text-foreground/80">Modules</strong> are implementation units — they carry M-numbers (e.g., M3, M111).</li>
            <li>• <strong className="text-foreground/80">Elements</strong> are VIP substrates — they carry E-numbers (E145–E156).</li>
            <li>• <strong className="text-foreground/80">Seats</strong> are Council positions — they carry S-numbers (S1–S10, S11–S13, S144).</li>
            <li>• <strong className="text-foreground/80">Houses</strong> are knowledge domains — they carry H-numbers (H1–H12).</li>
          </ul>
        </motion.div>

        <motion.div variants={fadeUp} className="space-y-4">
          {glossary.map((entry) => (
            <motion.div
              key={entry.term}
              variants={fadeUp}
              className="p-4 rounded border border-border/50 bg-card/30 hover:border-primary/30 transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="font-display font-semibold text-foreground mb-1">{entry.term}</h3>
                  <p className="text-sm text-muted-foreground mb-2">{entry.definition}</p>
                  {entry.context && (
                    <p className="text-xs text-muted-foreground/70 italic">{entry.context}</p>
                  )}
                </div>
                {entry.see && (
                  <a
                    href={entry.see}
                    className="shrink-0 text-[10px] font-mono text-primary hover:underline"
                  >
                    See →
                  </a>
                )}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </SpecLayout>
  );
}

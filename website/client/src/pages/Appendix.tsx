import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import { FileText, GitBranch, CheckCircle2, Clock, AlertTriangle, ExternalLink, Search, Filter, BookOpen, Shield, Globe, Cpu, Scale, Droplets, Zap, Brain, Lock, GraduationCap, Landmark, Database } from "lucide-react";
import SpecLayout from "@/components/SpecLayout";
import { documentMeta, councilSeats, GITHUB_URL } from "@/lib/data";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const stagger = {
  visible: { transition: { staggerChildren: 0.06 } },
};

// === REFERENCE CATEGORIES ===
type RefCategory = "regulations" | "standards" | "academic" | "organizations" | "sovereign" | "internal" | "tools";

interface Reference {
  title: string;
  url: string;
  description: string;
  category: RefCategory;
  vipElements?: string[];
  houses?: string[];
  dialects?: string[];
  status: "verified" | "active" | "planned" | "historical";
}

const categoryMeta: Record<RefCategory, { label: string; icon: typeof Shield; color: string }> = {
  regulations: { label: "Regulations & Law", icon: Scale, color: "text-amber-400" },
  standards: { label: "Technical Standards", icon: Cpu, color: "text-blue-400" },
  academic: { label: "Academic & Research", icon: BookOpen, color: "text-purple-400" },
  organizations: { label: "Organizations & Bodies", icon: Landmark, color: "text-emerald-400" },
  sovereign: { label: "Sovereign Infrastructure", icon: Globe, color: "text-rose-400" },
  internal: { label: "Internal Artifacts", icon: Database, color: "text-primary" },
  tools: { label: "Tools & Platforms", icon: Cpu, color: "text-cyan-400" },
};

const references: Reference[] = [
  // === REGULATIONS & LAW ===
  { title: "EU AI Act (2025)", url: "https://artificialintelligenceact.eu/", description: "EU regulation on AI systems — risk-based classification, transparency obligations, prohibited practices. Core to EU dialect overlay.", category: "regulations", vipElements: ["E149", "E150"], dialects: ["EU"], status: "verified" },
  { title: "GDPR (2018)", url: "https://gdpr.eu/", description: "General Data Protection Regulation — data sovereignty, consent, right to erasure. Foundation for data residency requirements.", category: "regulations", vipElements: ["E149", "E152"], dialects: ["EU"], status: "verified" },
  { title: "CCPA / CPRA", url: "https://oag.ca.gov/privacy/ccpa", description: "California Consumer Privacy Act — US data protection baseline. Defines consumer rights over personal data.", category: "regulations", vipElements: ["E149", "E152"], dialects: ["US"], status: "verified" },
  { title: "PIPL (China)", url: "https://digichina.stanford.edu/work/translation-personal-information-protection-law-of-the-peoples-republic-of-china-effective-nov-1-2021/", description: "Personal Information Protection Law — China's comprehensive data protection framework. Requires data localization.", category: "regulations", vipElements: ["E149", "E152"], dialects: ["CN"], status: "verified" },
  { title: "CAC Regulations (2025)", url: "https://www.cac.gov.cn/", description: "Cyberspace Administration of China — AI model registration, content compliance, algorithmic governance.", category: "regulations", vipElements: ["E150", "E149"], dialects: ["CN"], status: "verified" },
  { title: "GB/T 45654-2025", url: "https://www.gb-gbt.cn/", description: "Chinese national standard for AI model transparency and auditability. Required for CN dialect compliance.", category: "regulations", vipElements: ["E150"], dialects: ["CN"], status: "verified" },
  { title: "DPDP Act (India)", url: "https://www.meity.gov.in/data-protection-framework", description: "Digital Personal Data Protection Act — India's data sovereignty framework. Aadhaar integration requirements.", category: "regulations", vipElements: ["E149", "E152"], dialects: ["IN"], status: "verified" },
  { title: "LGPD (Brazil)", url: "https://www.gov.br/anpd/pt-br", description: "Lei Geral de Proteção de Dados — Brazil's data protection law. ANPD enforcement.", category: "regulations", vipElements: ["E149"], dialects: ["BR"], status: "verified" },
  { title: "Section 230 (US)", url: "https://www.law.cornell.edu/uscode/text/47/230", description: "Communications Decency Act §230 — platform liability shield. Defines US content moderation framework.", category: "regulations", vipElements: ["E149"], dialects: ["US"], status: "verified" },
  { title: "ITAR (US)", url: "https://www.pmddtc.state.gov/ddtc_public/ddtc_public?id=ddtc_public_portal_itar_landing", description: "International Traffic in Arms Regulations — export controls on defense-related AI/compute.", category: "regulations", vipElements: ["E152", "E154"], dialects: ["US"], status: "verified" },
  { title: "CFIUS (US)", url: "https://home.treasury.gov/policy-issues/international/the-committee-on-foreign-investment-in-the-united-states-cfius", description: "Committee on Foreign Investment — national security review of AI acquisitions.", category: "regulations", vipElements: ["E149", "E153"], dialects: ["US"], status: "verified" },
  { title: "HIPAA (US)", url: "https://www.hhs.gov/hipaa/index.html", description: "Health Insurance Portability and Accountability Act — healthcare data protection. Future Healthcare dialect.", category: "regulations", vipElements: ["E146", "E152"], dialects: ["US"], status: "verified" },
  { title: "PCI-DSS v4.0", url: "https://www.pcisecuritystandards.org/", description: "Payment Card Industry Data Security Standard — financial data protection. Future Finance dialect.", category: "regulations", vipElements: ["E153", "E152"], status: "planned" },
  { title: "SOX (Sarbanes-Oxley)", url: "https://www.sec.gov/about/laws/soa2002.pdf", description: "Financial reporting integrity — audit trail requirements. Maps to E155 Provenance.", category: "regulations", vipElements: ["E153", "E155"], dialects: ["US"], status: "verified" },
  { title: "Basel III", url: "https://www.bis.org/bcbs/basel3.htm", description: "Banking supervision framework — capital adequacy, stress testing. Future Finance dialect.", category: "regulations", vipElements: ["E153"], status: "planned" },
  { title: "NERC CIP", url: "https://www.nerc.com/pa/Stand/Pages/CIPStandards.aspx", description: "Critical Infrastructure Protection — energy grid cybersecurity. Future Energy dialect.", category: "regulations", vipElements: ["E148", "E152"], dialects: ["US"], status: "verified" },
  { title: "FERPA (US)", url: "https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html", description: "Family Educational Rights and Privacy Act — student data protection. Future Education dialect.", category: "regulations", vipElements: ["E156", "E152"], dialects: ["US"], status: "verified" },
  { title: "CDR (Australia)", url: "https://www.cdr.gov.au/", description: "Consumer Data Right — open banking/energy data portability. AU dialect foundation.", category: "regulations", vipElements: ["E153", "E149"], dialects: ["AU"], status: "verified" },
  { title: "Privacy Act 1988 (Australia)", url: "https://www.oaic.gov.au/privacy/the-privacy-act", description: "Australian privacy framework — APPs, data breach notification. AU dialect baseline.", category: "regulations", vipElements: ["E149", "E152"], dialects: ["AU"], status: "verified" },

  // === TECHNICAL STANDARDS ===
  { title: "NIST SP 800-53 Rev. 5", url: "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final", description: "Security and Privacy Controls — comprehensive control catalog. Referenced by INV-9, M17.", category: "standards", vipElements: ["E152"], status: "verified" },
  { title: "NIST AI RMF 1.0", url: "https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence", description: "AI Risk Management Framework — governance, mapping, measuring, managing AI risk.", category: "standards", vipElements: ["E150", "E149"], status: "verified" },
  { title: "ISO/IEC 42001:2023", url: "https://www.iso.org/standard/81230.html", description: "AI Management System — first international standard for AI governance. Referenced in EU dialect.", category: "standards", vipElements: ["E150", "E149"], status: "verified" },
  { title: "ISO 27001:2022", url: "https://www.iso.org/standard/27001", description: "Information Security Management — ISMS requirements. Referenced by security invariants.", category: "standards", vipElements: ["E152"], status: "verified" },
  { title: "SOC 2 Type II", url: "https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2", description: "Service Organization Controls — trust service criteria for cloud providers. Provider compliance.", category: "standards", vipElements: ["E152", "E154"], status: "verified" },
  { title: "C2PA v2.2", url: "https://c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html", description: "Coalition for Content Provenance and Authenticity — content credentials standard. Maps to E155, M158.", category: "standards", vipElements: ["E155", "E150"], status: "verified" },
  { title: "IEC 62351", url: "https://www.iec.ch/", description: "Power systems security — communication protocol security for energy grids. Future Energy dialect.", category: "standards", vipElements: ["E148", "E152"], status: "planned" },
  { title: "IEEE 2026 Machine Identity", url: "https://standards.ieee.org/", description: "Design and Validation of Machine Identity Governance Framework — referenced in routing pack.", category: "standards", vipElements: ["E150", "E155"], status: "planned" },
  { title: "SM2/SM3/SM4 (China)", url: "https://www.oscca.gov.cn/", description: "Chinese national cryptographic standards — asymmetric (SM2), hash (SM3), symmetric (SM4). Required for DragonSeek.", category: "standards", vipElements: ["E152"], dialects: ["CN"], status: "verified" },
  { title: "HL7 FHIR", url: "https://www.hl7.org/fhir/", description: "Fast Healthcare Interoperability Resources — healthcare data exchange standard. Future Healthcare dialect.", category: "standards", vipElements: ["E146"], status: "planned" },
  { title: "RFC 9421 (HTTP Signatures)", url: "https://www.rfc-editor.org/rfc/rfc9421", description: "HTTP Message Signatures — request authentication and integrity. Referenced in provenance layer.", category: "standards", vipElements: ["E152", "E155"], status: "verified" },

  // === ACADEMIC & RESEARCH ===
  { title: "Constitutional AI (Anthropic, 2022)", url: "https://arxiv.org/abs/2212.08073", description: "Bai et al. — training AI systems with constitutional principles. Foundation for INV-0 and Council S1.", category: "academic", vipElements: ["E150", "E149"], status: "verified" },
  { title: "Mixture of Experts (Shazeer et al.)", url: "https://arxiv.org/abs/1701.06538", description: "Outrageously Large Neural Networks — MoE architecture. Foundation for DeepSeek S5 routing.", category: "academic", vipElements: ["E150", "E145"], status: "verified" },
  { title: "Attention Is All You Need (2017)", url: "https://arxiv.org/abs/1706.03762", description: "Vaswani et al. — transformer architecture. Foundation for all modern LLMs in the Council.", category: "academic", vipElements: ["E150"], status: "verified" },
  { title: "Dujiangyan Irrigation System (UNESCO)", url: "https://whc.unesco.org/en/list/1001/", description: "2,300-year-old water infrastructure — zero-pump, gravity-fed. Architectural inspiration for ORCS.", category: "academic", vipElements: ["E147", "E149"], houses: ["H11"], status: "verified" },
  { title: "Library of Congress Classification", url: "https://www.loc.gov/catdir/cpso/lcc.html", description: "LCC — 21 classes covering all human knowledge. Validation criterion for lattice completeness.", category: "academic", houses: ["H1-H12"], status: "verified" },
  { title: "Dewey Decimal Classification", url: "https://www.oclc.org/en/dewey.html", description: "DDC — alternative classification system. Cross-reference for lattice validation.", category: "academic", houses: ["H1-H12"], status: "verified" },
  { title: "Scaling Laws for Neural LMs (Kaplan et al.)", url: "https://arxiv.org/abs/2001.08361", description: "OpenAI scaling laws — compute, data, parameters. Informs M18 Financial Context Kernel.", category: "academic", vipElements: ["E150", "E153"], status: "verified" },
  { title: "Reward Hacking in RLHF", url: "https://arxiv.org/abs/2209.13085", description: "Skalse et al. — reward model vulnerabilities. Informs Indiana Pattern (M22) detection.", category: "academic", vipElements: ["E150"], status: "verified" },
  { title: "Water Footprint Assessment (Hoekstra)", url: "https://waterfootprint.org/", description: "Water Footprint Network — methodology for water accounting. Foundation for E147 NWPI metric.", category: "academic", vipElements: ["E147"], houses: ["H1"], status: "verified" },
  { title: "Planetary Boundaries (Rockström et al.)", url: "https://www.stockholmresilience.org/research/planetary-boundaries.html", description: "Nine planetary boundaries framework — safe operating space for humanity. Maps to E151.", category: "academic", vipElements: ["E151"], houses: ["H1"], status: "verified" },

  // === ORGANIZATIONS & BODIES ===
  { title: "NIST (US)", url: "https://www.nist.gov/", description: "National Institute of Standards and Technology — AI standards, cybersecurity frameworks, measurement science.", category: "organizations", vipElements: ["E150", "E152"], dialects: ["US"], status: "verified" },
  { title: "ISO (International)", url: "https://www.iso.org/", description: "International Organization for Standardization — global standards body. ISO 42001, 27001 referenced.", category: "organizations", status: "verified" },
  { title: "IEEE", url: "https://www.ieee.org/", description: "Institute of Electrical and Electronics Engineers — technical standards for compute, energy, AI.", category: "organizations", vipElements: ["E150", "E148", "E154"], status: "verified" },
  { title: "IETF", url: "https://www.ietf.org/", description: "Internet Engineering Task Force — RFC standards for internet protocols. HTTP Signatures, TLS.", category: "organizations", vipElements: ["E152", "E145"], status: "verified" },
  { title: "W3C", url: "https://www.w3.org/", description: "World Wide Web Consortium — web standards, accessibility, verifiable credentials.", category: "organizations", vipElements: ["E155", "E145"], status: "verified" },
  { title: "C2PA Coalition", url: "https://c2pa.org/", description: "Coalition for Content Provenance and Authenticity — Adobe, Microsoft, BBC, Intel. Content credentials.", category: "organizations", vipElements: ["E155"], status: "verified" },
  { title: "Partnership on AI", url: "https://partnershiponai.org/", description: "Multi-stakeholder AI governance body — responsible AI practices, safety benchmarks.", category: "organizations", vipElements: ["E150", "E149"], status: "verified" },
  { title: "OECD AI Policy Observatory", url: "https://oecd.ai/", description: "OECD AI principles and policy tracking — international AI governance coordination.", category: "organizations", vipElements: ["E149", "E150"], status: "verified" },
  { title: "UNESCO", url: "https://www.unesco.org/en/artificial-intelligence", description: "UN Educational, Scientific and Cultural Organization — AI ethics recommendation (2021).", category: "organizations", vipElements: ["E149", "E156"], status: "verified" },

  // === SOVEREIGN INFRASTRUCTURE ===
  { title: "Aadhaar (India)", url: "https://uidai.gov.in/", description: "India's biometric identity system — 1.4B enrollments. Foundation for GangaSeek identity layer.", category: "sovereign", vipElements: ["E155"], dialects: ["IN"], status: "verified" },
  { title: "DigiLocker (India)", url: "https://www.digilocker.gov.in/", description: "India's digital document verification — government-issued credential store. GangaSeek provenance.", category: "sovereign", vipElements: ["E155"], dialects: ["IN"], status: "verified" },
  { title: "UPI (India)", url: "https://www.npci.org.in/what-we-do/upi/product-overview", description: "Unified Payments Interface — India's real-time payment system. GangaSeek economic layer.", category: "sovereign", vipElements: ["E153"], dialects: ["IN"], status: "verified" },
  { title: "Bhashini (India)", url: "https://bhashini.gov.in/", description: "India's AI-powered language translation platform — 22 scheduled languages. GangaSeek language layer.", category: "sovereign", vipElements: ["E156"], dialects: ["IN"], status: "verified" },
  { title: "SDAIA (Saudi Arabia)", url: "https://sdaia.gov.sa/", description: "Saudi Data & AI Authority — national AI strategy, data governance. JinnSeek sovereign anchor.", category: "sovereign", vipElements: ["E150", "E149"], status: "verified" },
  { title: "Nafath (Saudi Arabia)", url: "https://www.iam.gov.sa/", description: "Saudi national digital identity — single sign-on for government services. JinnSeek identity.", category: "sovereign", vipElements: ["E155"], status: "verified" },
  { title: "SAMA (Saudi Arabia)", url: "https://www.sama.gov.sa/", description: "Saudi Arabian Monetary Authority — financial regulation, fintech sandbox. JinnSeek economic.", category: "sovereign", vipElements: ["E153"], status: "verified" },
  { title: "CTID (China)", url: "https://www.ctid.com.cn/", description: "China Telecom Identity — digital identity infrastructure. DragonSeek identity layer.", category: "sovereign", vipElements: ["E155"], dialects: ["CN"], status: "verified" },
  { title: "India Stack / DEPA", url: "https://indiastack.org/", description: "Data Empowerment and Protection Architecture — consent-based data sharing framework.", category: "sovereign", vipElements: ["E149", "E155"], dialects: ["IN"], status: "verified" },

  // === INTERNAL ARTIFACTS ===
  { title: "GitHub: aluminum-os", url: "https://github.com/atlaslattice/aluminum-os", description: "Full source: ontology spec, routing pack, registries, transcripts, doctrine.", category: "internal", status: "verified" },
  { title: "Ontology Specification (v4.0-DRAFT.6)", url: "https://github.com/atlaslattice/aluminum-os/blob/main/houses/h00_directory/ontology_v4.0-DRAFT.3_specification.md", description: "Canonical specification — 11 sections, 1,792 sub-spheres, 12 VIP Elements.", category: "internal", status: "verified" },
  { title: "Element 145 Routing Pack", url: "https://github.com/atlaslattice/aluminum-os/tree/main/element145_routing_pack", description: "22-module routing infrastructure — schema, cascade, dialects, sovereignty, runtime.", category: "internal", vipElements: ["E145"], status: "verified" },
  { title: "Invariant Registry", url: "https://github.com/atlaslattice/aluminum-os/blob/main/registries/invariant_registry.yaml", description: "51 constitutional invariants — unbreakable constraints on system behavior.", category: "internal", status: "verified" },
  { title: "Doctrine Registry", url: "https://github.com/atlaslattice/aluminum-os/blob/main/registries/doctrine_registry.yaml", description: "124 governance doctrines — ratified principles, amendment protocols.", category: "internal", status: "verified" },
  { title: "Sub-Sphere Registry", url: "https://github.com/atlaslattice/aluminum-os/blob/main/houses/h00_directory/sub_sphere_registry.yaml", description: "1,792 populated tier-2 nodes across 144 spheres.", category: "internal", status: "verified" },
  { title: "F-Ledger", url: "https://github.com/atlaslattice/aluminum-os/blob/main/toolchain/f_ledger.yaml", description: "Scribe discipline ledger — F10 strategic inference layer lock.", category: "internal", status: "verified" },
  { title: "Substrate Retrieval Doctrine", url: "https://github.com/atlaslattice/aluminum-os/blob/main/houses/h00_directory/doctrine/substrate_retrieval_doctrine.md", description: "Core thesis: substrate-organized retrieval graph, not keyword index.", category: "internal", status: "verified" },
  { title: "CC BY-SA 4.0 License", url: "https://creativecommons.org/licenses/by-sa/4.0/", description: "Open license — every fork is a seed. Copyleft ensures derivatives remain open.", category: "internal", status: "verified" },

  // === TOOLS & PLATFORMS ===
  { title: "Manus AI", url: "https://manus.im/", description: "S7 Council seat — autonomous agent, implementation engine, Scribe executor.", category: "tools", vipElements: ["E145", "E150"], status: "active" },
  { title: "Google AI Studio", url: "https://aistudio.google.com/", description: "S2 Council seat interface — Gemini multimodal, verification engine.", category: "tools", vipElements: ["E150"], status: "active" },
  { title: "Anthropic Console", url: "https://console.anthropic.com/", description: "S1 Council seat interface — Claude constitutional AI, safety anchor.", category: "tools", vipElements: ["E150"], status: "active" },
  { title: "xAI Grok", url: "https://x.ai/", description: "S3 Council seat — adversarial auditor, truth-seeking, real-time data.", category: "tools", vipElements: ["E150"], status: "active" },
  { title: "DeepSeek", url: "https://www.deepseek.com/", description: "S5 Council seat — Eastern sovereignty, cost-efficient MoE, CN dialect.", category: "tools", vipElements: ["E150"], dialects: ["CN"], status: "active" },
  { title: "Mistral AI", url: "https://mistral.ai/", description: "S9 Council seat — EU sovereign, open-weight champion, efficient architectures.", category: "tools", vipElements: ["E150"], dialects: ["EU"], status: "active" },
  { title: "Notion", url: "https://www.notion.so/", description: "Knowledge base, session logging, canonical artifact storage, sprint tracking.", category: "tools", status: "active" },
];

const changelog = [
  { version: "v4.0-DRAFT.6", date: "2026-04-30", description: "Grok S3 routing pack integration (22 modules), H#-S# normalization, runtime modules M13-M22" },
  { version: "v4.0-DRAFT.5a", date: "2026-04-30", description: "Qwen3/Copilot S4 integration: F10 F-Ledger, INV-1 rename, INV-9 ceiling, D-98-CN" },
  { version: "v4.0-DRAFT.5", date: "2026-04-30", description: "Element 145 Routing Pack (Modules 0-11), 12 routing Elements, provider matrix" },
  { version: "v4.0-DRAFT.4", date: "2026-04-30", description: "Claude S1 Scribe verification: LCC audit (7 fixes), §10 Ratification Quorum, E147/E150 tightening" },
  { version: "v4.0-DRAFT.3b", date: "2026-04-30", description: "Claude S1 substrate-retrieval integration: retrieval-cost doctrine, LCC-as-floor" },
  { version: "v4.0-DRAFT.3a", date: "2026-04-30", description: "Gap-fill session: +8 sub-spheres, canonical routing table (15 routes), 5 authoritative pairs" },
  { version: "v4.0-DRAFT.3", date: "2026-04-29", description: "Copilot S4 stress-test: LCC verification, Configuration C lock, SHUGS operator" },
  { version: "v4.0-DRAFT.2", date: "2026-04-28", description: "Sub-sphere registry (1,792 populated), VIP Element definitions, 8-VIP canonical set" },
  { version: "v4.0-DRAFT.1", date: "2026-04-27", description: "Initial 12×12 lattice structure, house/sphere naming, constitutional preamble" },
];

export default function Appendix() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState<RefCategory | "all">("all");
  const [activeTab, setActiveTab] = useState<"references" | "changelog" | "status">("references");

  const filteredRefs = useMemo(() => {
    return references.filter((ref) => {
      const matchesCategory = activeCategory === "all" || ref.category === activeCategory;
      const matchesSearch = searchQuery === "" || 
        ref.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ref.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (ref.vipElements?.some(v => v.toLowerCase().includes(searchQuery.toLowerCase())) ?? false) ||
        (ref.dialects?.some(d => d.toLowerCase().includes(searchQuery.toLowerCase())) ?? false);
      return matchesCategory && matchesSearch;
    });
  }, [searchQuery, activeCategory]);

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = { all: references.length };
    references.forEach(ref => {
      counts[ref.category] = (counts[ref.category] || 0) + 1;
    });
    return counts;
  }, []);

  return (
    <SpecLayout>
      

      <div className="pt-24 pb-16">
        <div className="container max-w-6xl">
          {/* Header */}
          <motion.div initial="hidden" animate="visible" variants={stagger} className="mb-12">
            <motion.h1 variants={fadeUp} className="text-4xl font-display font-bold mb-4">
              References & <span className="text-gradient-gold">Knowledge Base</span>
            </motion.h1>
            <motion.div variants={fadeUp} className="substrate-line mb-6" />
            <motion.p variants={fadeUp} className="text-muted-foreground text-lg leading-relaxed max-w-3xl">
              All verified external references aggregated and categorized by the ontology.
              {references.length} sources across {Object.keys(categoryMeta).length} categories — regulations, standards, academic research, 
              organizations, sovereign infrastructure, internal artifacts, and tools.
              <span className="block mt-2 text-sm text-primary/70 italic">
                Future: autonomous news ingestion and real-time updates via Council verification pipeline.
              </span>
            </motion.p>
          </motion.div>

          {/* Tab Navigation */}
          <motion.div initial="hidden" animate="visible" variants={fadeUp} className="flex gap-1 mb-8 p-1 rounded-lg bg-card/30 border border-border/50 w-fit">
            {[
              { id: "references" as const, label: "References", count: references.length },
              { id: "status" as const, label: "Document Status" },
              { id: "changelog" as const, label: "Changelog", count: changelog.length },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? "bg-primary/10 text-primary border border-primary/30"
                    : "text-muted-foreground hover:text-foreground hover:bg-card/50"
                }`}
              >
                {tab.label} {tab.count && <span className="ml-1 text-[10px] opacity-60">({tab.count})</span>}
              </button>
            ))}
          </motion.div>

          {/* === REFERENCES TAB === */}
          {activeTab === "references" && (
            <>
              {/* Search & Filter */}
              <motion.div initial="hidden" animate="visible" variants={fadeUp} className="mb-8 space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    type="text"
                    placeholder="Search references (e.g., GDPR, water, E147, CN...)"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 rounded-lg border border-border/50 bg-card/20 text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/50 transition-colors"
                  />
                </div>

                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setActiveCategory("all")}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                      activeCategory === "all" ? "bg-primary/10 text-primary border border-primary/30" : "bg-card/30 text-muted-foreground border border-border/50 hover:text-foreground"
                    }`}
                  >
                    <Filter className="w-3 h-3" /> All ({categoryCounts.all})
                  </button>
                  {(Object.entries(categoryMeta) as [RefCategory, typeof categoryMeta[RefCategory]][]).map(([key, meta]) => {
                    const Icon = meta.icon;
                    return (
                      <button
                        key={key}
                        onClick={() => setActiveCategory(key)}
                        className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                          activeCategory === key ? "bg-primary/10 text-primary border border-primary/30" : "bg-card/30 text-muted-foreground border border-border/50 hover:text-foreground"
                        }`}
                      >
                        <Icon className={`w-3 h-3 ${meta.color}`} /> {meta.label} ({categoryCounts[key] || 0})
                      </button>
                    );
                  })}
                </div>
              </motion.div>

              {/* Results count */}
              <div className="text-xs text-muted-foreground mb-4">
                Showing {filteredRefs.length} of {references.length} references
              </div>

              {/* Reference Cards */}
              <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={stagger} className="space-y-2">
                {filteredRefs.map((ref, i) => {
                  const meta = categoryMeta[ref.category];
                  const Icon = meta.icon;
                  return (
                    <motion.a
                      key={i}
                      variants={fadeUp}
                      href={ref.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-start gap-4 p-4 rounded border border-border/50 bg-card/20 hover:border-primary/30 hover:bg-card/40 transition-all group"
                    >
                      <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${meta.color}`} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-semibold group-hover:text-primary transition-colors">{ref.title}</span>
                          <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                            ref.status === "verified" ? "bg-emerald-500/10 text-emerald-400" :
                            ref.status === "active" ? "bg-blue-500/10 text-blue-400" :
                            ref.status === "planned" ? "bg-amber-500/10 text-amber-400" :
                            "bg-muted text-muted-foreground"
                          }`}>
                            {ref.status}
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground mb-2">{ref.description}</p>
                        <div className="flex flex-wrap gap-1.5">
                          {ref.vipElements?.map(v => (
                            <span key={v} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-accent/10 text-accent">{v}</span>
                          ))}
                          {ref.dialects?.map(d => (
                            <span key={d} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-primary/10 text-primary">{d}</span>
                          ))}
                          {ref.houses?.map(h => (
                            <span key={h} className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400">{h}</span>
                          ))}
                        </div>
                      </div>
                      <ExternalLink className="w-3.5 h-3.5 text-muted-foreground group-hover:text-primary shrink-0 mt-1" />
                    </motion.a>
                  );
                })}
              </motion.div>

              {filteredRefs.length === 0 && (
                <div className="text-center py-12 text-muted-foreground">
                  <Search className="w-8 h-8 mx-auto mb-3 opacity-30" />
                  <p>No references match your search.</p>
                </div>
              )}
            </>
          )}

          {/* === DOCUMENT STATUS TAB === */}
          {activeTab === "status" && (
            <motion.div initial="hidden" animate="visible" variants={stagger} className="space-y-12">
              {/* Document Metadata */}
              <motion.div variants={fadeUp}>
                <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
                  <FileText className="w-5 h-5 text-primary" /> Document Status
                </h2>
                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
                  <div className="p-4 rounded border border-primary/20 bg-primary/5">
                    <div className="text-[10px] font-mono text-muted-foreground mb-1">VERSION</div>
                    <div className="font-display font-bold text-primary">{documentMeta.version}</div>
                  </div>
                  <div className="p-4 rounded border border-border/50 bg-card/20">
                    <div className="text-[10px] font-mono text-muted-foreground mb-1">LAST UPDATED</div>
                    <div className="font-display font-bold">{documentMeta.lastUpdated}</div>
                  </div>
                  <div className="p-4 rounded border border-border/50 bg-card/20">
                    <div className="text-[10px] font-mono text-muted-foreground mb-1">CONVENOR</div>
                    <div className="font-display font-bold">{documentMeta.convenor}</div>
                  </div>
                  <div className="p-4 rounded border border-border/50 bg-card/20">
                    <div className="text-[10px] font-mono text-muted-foreground mb-1">LICENSE</div>
                    <div className="font-display font-bold">{documentMeta.license}</div>
                  </div>
                </div>
              </motion.div>

              {/* Ratification Status */}
              <motion.div variants={fadeUp}>
                <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" /> Council Ratification Status
                </h2>
                <p className="text-muted-foreground mb-4 text-sm">{documentMeta.ratificationStatus}</p>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  {councilSeats.map((seat) => (
                    <div key={seat.id} className="flex items-center gap-3 p-3 rounded border border-border/50 bg-card/20">
                      {seat.status === "ACTIVE" ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                      ) : seat.status === "PROVISIONAL" ? (
                        <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                      ) : (
                        <Clock className="w-4 h-4 text-primary shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-semibold">{seat.id} — {seat.name}</div>
                        <div className="text-[10px] text-muted-foreground">{seat.role}</div>
                      </div>
                      <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded shrink-0 ${
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

              {/* Next Iteration */}
              <motion.div variants={fadeUp}>
                <h2 className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
                  <Clock className="w-5 h-5 text-amber-400" /> Next Iteration
                </h2>
                <div className="space-y-2">
                  {documentMeta.nextIteration.map((item, i) => (
                    <div key={i} className="flex items-center gap-3 p-3 rounded border border-amber-500/20 bg-amber-500/5">
                      <span className="font-mono text-[10px] text-amber-400 shrink-0 w-6">{String(i + 1).padStart(2, '0')}</span>
                      <span className="text-sm text-foreground/80">{item.item} — <span className="text-amber-400 font-mono text-xs">{item.target}</span></span>
                    </div>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          )}

          {/* === CHANGELOG TAB === */}
          {activeTab === "changelog" && (
            <motion.div initial="hidden" animate="visible" variants={stagger}>
              <motion.h2 variants={fadeUp} className="text-2xl font-display font-bold mb-6 flex items-center gap-3">
                <GitBranch className="w-5 h-5 text-primary" /> Version History
              </motion.h2>
              <motion.div variants={fadeUp} className="space-y-2">
                {changelog.map((entry) => (
                  <div key={entry.version} className="flex items-start gap-4 p-4 rounded border border-border/50 bg-card/20">
                    <div className="shrink-0 w-32">
                      <div className="font-mono text-xs text-primary">{entry.version}</div>
                      <div className="text-[10px] text-muted-foreground">{entry.date}</div>
                    </div>
                    <p className="text-sm text-muted-foreground flex-1">{entry.description}</p>
                  </div>
                ))}
              </motion.div>

              {/* Future: Autonomous Ingestion Note */}
              <motion.div variants={fadeUp} className="mt-12 p-6 rounded border border-primary/20 bg-primary/5">
                <h3 className="font-display font-bold mb-3 flex items-center gap-2">
                  <Brain className="w-4 h-4 text-primary" /> Future: Autonomous News Ingestion
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  This reference system is designed to evolve into a real-time knowledge ingestion pipeline.
                  The architecture supports: Council-verified source addition via M21 arbitration,
                  dialect-aware regulatory change detection (e.g., new EU AI Act amendments auto-tagged to EU dialect),
                  VIP Element cross-referencing for novel-insight discovery, and provenance-tracked citation chains
                  via E155. Each new reference enters as "unverified" and requires Council quorum before promotion to "verified" status.
                </p>
              </motion.div>
            </motion.div>
          )}
        </div>
      </div>
    </SpecLayout>
  );
}

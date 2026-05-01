// Aluminum OS — Atlas Lattice Architecture Data
// Design: Obsidian Substrate (Dark Brutalist Data Cathedral)
// Typography: Space Grotesk (display), IBM Plex Sans (body), JetBrains Mono (mono)
// Canon Baseline: v4.0-DRAFT.5 (Configuration C, locked by Convenor 2026-04-30)

// === IMAGES ===
export const HERO_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310419663032278456/gzELm6NxxGK3gevpRqhBCe/hero_lattice_mandala-nfxhECtqVGForAinYJMVmX.webp";
export const VIP_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310419663032278456/gzELm6NxxGK3gevpRqhBCe/vip_elements_abstract-9NhgBRKXkA9DAppXc2am4J.webp";
export const ROUTING_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310419663032278456/gzELm6NxxGK3gevpRqhBCe/routing_pack_visualization-X6JScSA9DzsUyjaCaPeyAp.webp";
export const MIRROR_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310419663032278456/gzELm6NxxGK3gevpRqhBCe/as_above_so_below-BqieST5GxBE4cewgC4afGc.webp";
export const COUNCIL_IMAGE = "https://d2xsxph8kpxj0f.cloudfront.net/310419663032278456/gzELm6NxxGK3gevpRqhBCe/council_pantheon-LiHJPu7cTpUA8vp8RSGWTZ.webp";

export const GITHUB_URL = "https://github.com/atlaslattice/aluminum-os";

// === KEY METRICS ===
export const keyMetrics = [
  { label: "Houses", value: "12", description: "Knowledge domains (Configuration C, locked)" },
  { label: "Spheres", value: "144", description: "Discipline nodes (12 per House). 143 populated + 1 BLANK_GAP (H1-S12 reserved)." },
  { label: "Sub-Spheres", value: "~1,792", description: "Tier-2 sub-spheres enumerated in v4.0-DRAFT.5 §2. Variable per sphere (8-15 typical)." },
  { label: "VIP Elements", value: "12", description: "Civilizational substrates: 8 canonical (E145-E152 per DRAFT.5) + 4 site expansions (E153-E156)." },
  { label: "Modules", value: "~100", description: "Specified compute modules: 74 base (Build Plan v2.3) + VIP-era additions (M75-M79, M99-M109). Projected ceiling ~100." },
  { label: "Doctrines", value: "~100", description: "Governance rules: D-1 through D-95 ratified + D-96 through D-99 under discussion + amendments (D-98-CN). Per ORC-017." },
  { label: "Invariants", value: "43", description: "Constitutional constraints: INV-0 through INV-39 (40 base) + INV-19 Water, INV-20 Neural, INV-21 Orbital. INV-7c counted as sub-spec." },
  { label: "Dialects", value: "6+2", description: "6 ratified (US, EU, CN, GCC-High, JP, Global) + 2 planned (IN, SA). Industry/risk/compute/cultural dialect layers under development." },
  { label: "Council", value: "10+3+1", description: "10 active seats (S1-S10) + 3 provisional (S11 Notion, S12 Sarvam, S13 pending) + S144 Ghost Seat (reserved). Convenor holds final ratification." },
];

// === 12 HOUSES (Configuration C — locked by Convenor 2026-04-30) ===
export interface House {
  id: string;
  number: number;
  name: string;
  spheres: string[];
  color: string;
  vipPair?: string;
}

export const houses: House[] = [
  { id: "H1", number: 1, name: "Science", color: "#00ffd5", spheres: ["Physics", "Chemistry", "Biology", "Earth & Planetary Science", "Cognition", "Materials Science", "Mathematics", "Statistics & Probability", "Logic & Foundations", "Information Theory", "Systems Theory", "BLANK_GAP (Reserved)"] },
  { id: "H2", number: 2, name: "Computing", color: "#4fc3f7", spheres: ["Computer Science Theory", "Algorithms & Data Structures", "AI & Machine Learning", "Software Engineering", "Data Engineering & Science", "Cybersecurity & Cryptography", "Networks & Distributed Systems", "Computer Architecture", "Human-Computer Interaction", "Robotics & Autonomous Systems", "Quantum Computing", "Information Systems"] },
  { id: "H3", number: 3, name: "Engineering", color: "#81c784", spheres: ["Mechanical Engineering", "Electrical & Electronic Engineering", "Civil & Structural Engineering", "Chemical & Process Engineering", "Aerospace Engineering", "Biomedical Engineering", "Environmental Engineering", "Nuclear Engineering", "Industrial & Systems Engineering", "Mining & Geological Engineering", "Telecommunications Engineering", "Ocean & Marine Engineering"] },
  { id: "H4", number: 4, name: "Health & Medicine", color: "#ffb74d", spheres: ["Anatomy & Physiology", "Pharmacology & Toxicology", "Clinical Medicine", "Psychiatry & Behavioral Health", "Public Health & Epidemiology", "Nursing & Allied Health", "Dentistry", "Veterinary Medicine", "Genetics & Genomics", "Immunology & Microbiology (Clinical)", "Rehabilitation & Sports Medicine", "Traditional & Integrative Medicine"] },
  { id: "H5", number: 5, name: "Agriculture", color: "#f06292", spheres: ["Crop Science", "Soil Science", "Animal Science", "Forestry & Agroforestry", "Fisheries & Marine Resources", "Food Science & Technology", "Agricultural Engineering", "Agricultural Economics", "Plant Protection", "Water Resources & Irrigation", "Sustainable Agriculture", "Genetics & Biotechnology (Agricultural)"] },
  { id: "H6", number: 6, name: "Security", color: "#7986cb", spheres: ["National Security & Strategy", "Intelligence & Counterintelligence", "Cybersecurity Operations", "Defense Technology", "Maritime & Naval Security", "Land Security & Operations", "Air & Space Security", "Counter-Terrorism & Extremism", "Emergency Management & Resilience", "Law Enforcement & Public Safety", "Arms Control & Non-Proliferation", "Security Governance & Ethics"] },
  { id: "H7", number: 7, name: "Philosophy, Ethics & Religion", color: "#4dd0e1", spheres: ["Metaphysics & Ontology", "Epistemology", "Ethics & Moral Philosophy", "Applied Ethics", "Political Philosophy", "Philosophy of Mind", "Philosophy of Science", "Theology & Religious Studies", "Aesthetics & Philosophy of Art", "Logic (Applied & Philosophical)", "Eastern Philosophy", "Continental Philosophy"] },
  { id: "H8", number: 8, name: "Arts", color: "#aed581", spheres: ["Visual Arts", "Music", "Performing Arts", "Film & Moving Image", "Architecture", "Design", "Literary Arts", "Craft & Applied Arts", "Digital & New Media Arts", "Art History & Theory", "Cultural Production & Industries", "Game Design & Interactive Media"] },
  { id: "H9", number: 9, name: "Knowledge Systems", color: "#ef5350", spheres: ["Pedagogy & Learning Science", "Higher Education", "EdTech & Digital Learning", "Vocational & Professional Education", "Special Education & Inclusion", "Library & Information Science", "Media & Journalism", "Publishing & Digital Content", "Communication Studies", "Linguistics", "Broadcasting & Telecommunications", "Digital Literacy & Information Ethics"] },
  { id: "H10", number: 10, name: "Social Sciences", color: "#ffd54f", spheres: ["Sociology", "Psychology", "Anthropology", "History", "Geography", "Political Science", "Economics (Theoretical)", "Demography & Population Studies", "Cultural Studies", "Gender & Sexuality Studies", "Development Studies", "Area & Regional Studies"] },
  { id: "H11", number: 11, name: "Business, Economics & Infrastructure", color: "#90a4ae", spheres: ["Accounting & Auditing", "Finance & Banking", "Management & Strategy", "Marketing & Consumer Behavior", "Entrepreneurship & Innovation", "Supply Chain & Logistics", "Energy Systems & Policy", "Transportation & Mobility", "Real Estate & Construction", "Telecommunications & Digital Infrastructure", "Water & Sanitation Infrastructure", "International Trade & Commerce"] },
  { id: "H12", number: 12, name: "Law & Governance", color: "#ce93d8", spheres: ["Constitutional Law", "Criminal Law & Justice", "Civil & Commercial Law", "International Law", "Human Rights Law", "Environmental Law", "Intellectual Property Law", "Technology & Digital Law", "Administrative & Regulatory Law", "Corporate Law & Governance", "Public Policy & Governance", "Diplomacy & International Relations (Legal)"] },
];

// === 12 VIP ELEMENTS ===
// E145-E152: Canonical from DRAFT.5 §3 (8 peer civilizational substrates, no hierarchy)
// E153-E156: Site expansions (approved by Convenor, don't break 12×12+1 convention)
export interface VIPElement {
  id: string;
  code: string;
  name: string;
  subtitle: string;
  nodes: { id: string; name: string; description: string }[];
  color: string;
  housePairs: string[];
}

export const vipElements: VIPElement[] = [
  {
    id: "E145", code: "E145", name: "Aluminum OS Core", subtitle: "Meta-Orchestrator",
    color: "#00ffd5",
    housePairs: ["H2", "H9", "H12"],
    nodes: [
      { id: "E145.01", name: "Lattice Router", description: "Query classification, sphere routing, multi-seat dispatch" },
      { id: "E145.02", name: "Ontology Engine", description: "12×12 structure enforcement, schema validation, migration" },
      { id: "E145.03", name: "Federation Bridge", description: "Cross-seat communication, capability negotiation, load balancing" },
      { id: "E145.04", name: "Constitutional Enforcer", description: "Doctrine compliance, invariant checking, amendment processing" },
      { id: "E145.05", name: "Synthesis Engine", description: "Multi-source response aggregation, conflict resolution, citation" },
      { id: "E145.06", name: "Audit & Telemetry", description: "Query logging, performance metrics, drift detection" },
      { id: "E145.07", name: "Boot Manifest", description: "System initialization, dependency resolution, health checks" },
      { id: "E145.08", name: "Pantheon Council Interface", description: "10-seat voting, quorum management, ratification workflow" },
      { id: "E145.09", name: "SHUGS Operator", description: "Sovereignty, Humility, Utility, Growth, Stewardship enforcement" },
      { id: "E145.10", name: "Schema Migration Engine", description: "Version-to-version ontology migration, backward compatibility, alias management" },
      { id: "E145.11", name: "Dialect Compiler", description: "Jurisdiction-specific rule compilation, overlay application, compliance verification" },
      { id: "E145.12", name: "Meta-Orchestrator Heartbeat", description: "System health monitoring, self-repair, graceful degradation coordination" },
    ]
  },
  {
    id: "E146", code: "E146", name: "Entertainment & Interactive Media", subtitle: "X-Factor",
    color: "#f06292",
    housePairs: ["H8", "H9"],
    nodes: [
      { id: "E146.01", name: "Game Engine Technology", description: "Unity, Unreal, Godot, custom engines, rendering pipelines" },
      { id: "E146.02", name: "VFX & Animation Pipeline", description: "Motion capture, compositing, procedural animation, real-time VFX" },
      { id: "E146.03", name: "Virtual Production", description: "LED volumes, real-time rendering, virtual cinematography, previsualization" },
      { id: "E146.04", name: "Interactive Audio & Adaptive Music", description: "Middleware (Wwise, FMOD), dynamic scoring, spatial audio, procedural sound" },
      { id: "E146.05", name: "Streaming Platform Architecture", description: "Recommender systems, ad-tech stacks, A/B-testing frameworks, content delivery optimization" },
      { id: "E146.06", name: "Immersive & XR Experiences", description: "VR/AR/MR content, haptics, spatial computing, metaverse platforms" },
      { id: "E146.07", name: "Esports & Competitive Gaming", description: "Tournament infrastructure, anti-cheat, broadcasting, team management" },
      { id: "E146.08", name: "Entertainment AI", description: "Procedural generation, NPC behavior, recommendation engines, AI-driven content (cross-ref E150.01, E150.10)" },
      { id: "E146.09", name: "Game Art & Asset Production", description: "3D modeling, texturing, rigging, concept art, asset pipelines" },
      { id: "E146.10", name: "Creator Economy Platforms", description: "UGC platforms (YouTube, TikTok, Twitch), revenue-share models, algorithmic visibility" },
      { id: "E146.11", name: "Music Production & Sound Engineering", description: "DAWs, mixing, mastering, synthesis, sampling, live sound" },
      { id: "E146.12", name: "Transmedia & IP Management", description: "Cross-platform storytelling, franchise management, licensing, merchandising" },
    ]
  },
  {
    id: "E147", code: "E147", name: "Water", subtitle: "Civilizational Substrate",
    color: "#4fc3f7",
    housePairs: ["H1", "H5", "H11"],
    nodes: [
      { id: "E147.01", name: "Freshwater Systems", description: "Rivers, lakes, aquifers, groundwater, watershed management" },
      { id: "E147.02", name: "Ocean Systems", description: "Marine ecosystems, ocean currents, deep-sea, coral reefs" },
      { id: "E147.03", name: "Water Treatment & Purification", description: "Filtration, desalination, disinfection, membrane technology" },
      { id: "E147.04", name: "Water Distribution Infrastructure", description: "Pipelines, pumping, storage, smart water networks" },
      { id: "E147.05", name: "Water Governance & Rights", description: "Water law, transboundary water, water markets, indigenous water rights, Indigenous Water Sovereignty" },
      { id: "E147.06", name: "Water & Agriculture", description: "Irrigation, drainage, water-food nexus, virtual water trade (cross-ref H5-S10)" },
      { id: "E147.07", name: "Water & Health", description: "Waterborne disease, WASH, water quality monitoring, sanitation, Sanitation Infrastructure Sovereignty" },
      { id: "E147.08", name: "Water & Energy", description: "Hydropower, cooling water, water-energy nexus, thermal pollution (cross-ref H11-S7)" },
      { id: "E147.09", name: "Water & Climate", description: "Glacial melt, sea level rise, drought, flood management" },
      { id: "E147.10", name: "Water Economics", description: "Water pricing, water markets, economic valuation, investment" },
      { id: "E147.11", name: "Water Technology", description: "Sensors, IoT monitoring, AI for water, leak detection" },
      { id: "E147.12", name: "Water Culture & Ethics", description: "Water as sacred, water justice, water commons, cultural practices, Water Commons & Civic Currency" },
    ]
  },
  {
    id: "E148", code: "E148", name: "Technology Substrate", subtitle: "Cross-Cutting",
    color: "#ffd54f",
    housePairs: ["H2", "H3", "H11"],
    nodes: [
      { id: "E148.01", name: "Semiconductor Supply Chain", description: "Chip design, fabrication, packaging, EDA tools, foundry economics" },
      { id: "E148.02", name: "Cloud & Hyperscale Infrastructure", description: "Data centers, cloud platforms, serverless, multi-cloud, sovereignty" },
      { id: "E148.03", name: "Connectivity Infrastructure", description: "5G/6G, fiber, satellite, mesh networks, digital divide" },
      { id: "E148.04", name: "Operating Systems & Platforms", description: "Desktop, mobile, embedded, real-time, cloud-native OS" },
      { id: "E148.05", name: "Developer Ecosystems", description: "IDEs, package managers, open source, developer experience" },
      { id: "E148.06", name: "Digital Identity & Trust", description: "PKI, SSO, decentralized identity, biometrics, zero-trust" },
      { id: "E148.07", name: "Standards & Interoperability", description: "IEEE, IETF, W3C, ISO, protocol design, API standards" },
      { id: "E148.08", name: "Technology Policy & Regulation", description: "Antitrust, platform regulation, technology sovereignty, export controls" },
      { id: "E148.09", name: "Emerging Computing Paradigms", description: "Neuromorphic, DNA computing, optical computing, analog computing" },
      { id: "E148.10", name: "Technology Ethics & Impact", description: "Digital ethics, algorithmic bias, technology assessment, responsible innovation" },
      { id: "E148.11", name: "Technology Transfer & Commercialization", description: "Patents, licensing, spin-offs, university-industry, tech parks" },
      { id: "E148.12", name: "Legacy Systems & Migration", description: "Mainframe, COBOL, modernization, digital transformation, technical debt" },
    ]
  },
  {
    id: "E149", code: "E149", name: "Constitution & Rule of Law", subtitle: "Civilizational Substrate",
    color: "#ce93d8",
    housePairs: ["H12", "H7", "H10"],
    nodes: [
      { id: "E149.01", name: "Constitutional Design", description: "Drafting, amendment procedures, constitutional conventions" },
      { id: "E149.02", name: "Separation of Powers", description: "Executive, legislative, judicial balance, checks and balances" },
      { id: "E149.03", name: "Federalism & Devolution", description: "Central-local relations, subsidiarity, fiscal federalism" },
      { id: "E149.04", name: "Rule of Law Mechanisms", description: "Judicial independence, due process, habeas corpus, legal certainty" },
      { id: "E149.05", name: "Democratic Institutions", description: "Elections, parliaments, political parties, referenda" },
      { id: "E149.06", name: "Anti-Corruption Frameworks", description: "Transparency, accountability, whistleblower protection, asset declaration" },
      { id: "E149.07", name: "Transitional Justice", description: "Truth commissions, reparations, lustration, post-conflict justice" },
      { id: "E149.08", name: "International Constitutional Order", description: "UN Charter, ICC, international courts, sovereignty vs intervention" },
      { id: "E149.09", name: "Digital Constitutionalism", description: "Platform governance, algorithmic rights, digital due process" },
      { id: "E149.10", name: "Indigenous Governance Systems", description: "Customary law, tribal governance, treaty rights, self-determination" },
      { id: "E149.11", name: "Constitutional Economics", description: "Property rights, contract enforcement, regulatory takings, fiscal constitution" },
      { id: "E149.12", name: "Constitutional Futures", description: "AI governance frameworks, space law, post-national governance" },
    ]
  },
  {
    id: "E150", code: "E150", name: "AI Systems & Intelligence", subtitle: "Civilizational Substrate",
    color: "#7986cb",
    housePairs: ["H2", "H1", "H7"],
    nodes: [
      { id: "E150.01", name: "Foundation Model Substrate", description: "Large language models, multimodal models, training infrastructure, scaling laws. Includes media-generation and media-ranking models." },
      { id: "E150.02", name: "AI Governance & Safety", description: "Alignment, interpretability, red-teaming, regulatory frameworks, AI rights" },
      { id: "E150.03", name: "Autonomous Systems Substrate", description: "Self-driving, drones, surgical robots, industrial automation (cross-ref H2-S10)" },
      { id: "E150.04", name: "Multi-Agent & Federation Substrate", description: "Agent-to-agent protocols, swarm intelligence, collective decision-making. Pantheon Council pattern (Atlas Lattice canon)." },
      { id: "E150.05", name: "AI Hardware Substrate", description: "TPUs, GPUs, neuromorphic chips, AI-specific architectures, energy efficiency" },
      { id: "E150.06", name: "AI & Scientific Discovery", description: "AlphaFold, materials discovery, drug design, theorem proving, climate modeling" },
      { id: "E150.07", name: "AI Ethics & Bias", description: "Fairness, accountability, transparency, representational harm, consent" },
      { id: "E150.08", name: "AI in Education", description: "Tutoring systems, assessment AI, personalized learning, AI literacy" },
      { id: "E150.09", name: "AI Risk & Existential Safety", description: "Superintelligence, containment, value alignment, catastrophic risk (cross-ref E149.04)" },
      { id: "E150.10", name: "AI Economics Substrate", description: "Automation economics, labor displacement, AI-driven markets, compute economics. Attention markets, ad auctions, recommender-driven revenue." },
      { id: "E150.11", name: "AI & Creative Expression", description: "Generative art, AI music, AI writing, human-AI co-creation (cross-ref H8-S9)" },
      { id: "E150.12", name: "AI Infrastructure & Operations", description: "MLOps, model serving, inference optimization, monitoring, cost management" },
    ]
  },
  {
    id: "E151", code: "E151", name: "Climate & Planetary Metabolism", subtitle: "Civilizational Substrate",
    color: "#81c784",
    housePairs: ["H1", "H3", "H5"],
    nodes: [
      { id: "E151.01", name: "Carbon Cycle & Greenhouse Gases", description: "CO2, methane, N2O, carbon sinks, carbon budget, atmospheric chemistry" },
      { id: "E151.02", name: "Planetary Boundaries", description: "9 boundaries framework, safe operating space, tipping points" },
      { id: "E151.03", name: "Climate Modeling & Prediction", description: "GCMs, regional models, scenario analysis, IPCC frameworks" },
      { id: "E151.04", name: "Climate Adaptation", description: "Resilience planning, infrastructure adaptation, migration, insurance" },
      { id: "E151.05", name: "Climate Mitigation", description: "Emissions reduction, carbon capture, renewable transition, efficiency" },
      { id: "E151.06", name: "Biodiversity & Ecosystem Services", description: "Species loss, habitat destruction, pollination, water filtration, soil health" },
      { id: "E151.07", name: "Circular Economy & Waste", description: "Material flows, recycling, industrial ecology, zero waste, extended producer responsibility" },
      { id: "E151.08", name: "Climate Finance", description: "Green bonds, carbon markets, climate funds, ESG, stranded assets" },
      { id: "E151.09", name: "Climate Justice", description: "Equity, loss and damage, climate refugees, intergenerational justice" },
      { id: "E151.10", name: "Food Systems & Climate", description: "Agricultural emissions, food waste, dietary change, regenerative agriculture" },
      { id: "E151.11", name: "Urban Climate", description: "Heat islands, green infrastructure, sustainable transport, smart cities" },
      { id: "E151.12", name: "Climate Communication & Education", description: "Science communication, climate literacy, behavior change, media coverage" },
    ]
  },
  {
    id: "E152", code: "E152", name: "Cybersecurity Substrate", subtitle: "Civilizational Substrate",
    color: "#ef5350",
    housePairs: ["H2", "H6", "H12"],
    nodes: [
      { id: "E152.01", name: "Critical Infrastructure Protection", description: "Energy grids, water systems, financial networks, healthcare systems" },
      { id: "E152.02", name: "Nation-State Cyber Operations", description: "APTs, cyber warfare, espionage, attribution, deterrence" },
      { id: "E152.03", name: "Cyber Governance & Norms", description: "Budapest Convention, Tallinn Manual, UN GGE, cyber sovereignty" },
      { id: "E152.04", name: "Supply Chain Security", description: "Hardware tampering, software supply chain, SBOMs, trusted computing" },
      { id: "E152.05", name: "Identity & Access at Scale", description: "National ID systems, digital identity, authentication infrastructure" },
      { id: "E152.06", name: "Cryptographic Infrastructure", description: "PKI, certificate authorities, key management, post-quantum transition" },
      { id: "E152.07", name: "Incident Response at Scale", description: "National CERTs, coordinated disclosure, crisis communication" },
      { id: "E152.08", name: "Cyber Insurance & Economics", description: "Risk quantification, premium models, systemic risk, market failures" },
      { id: "E152.09", name: "Privacy Engineering", description: "Differential privacy, homomorphic encryption, secure multi-party computation" },
      { id: "E152.10", name: "Disinformation & Information Warfare", description: "Deepfakes, bot networks, influence operations, counter-narratives" },
      { id: "E152.11", name: "IoT & OT Security", description: "Industrial control systems, SCADA, medical devices, automotive security" },
      { id: "E152.12", name: "Cyber Education & Workforce", description: "Cyber ranges, certifications, talent pipeline, awareness programs" },
    ]
  },
  // === E153-E156: Site Expansions (approved by Convenor, don't break 12×12+1) ===
  {
    id: "E153", code: "E153", name: "Energy & Power Systems", subtitle: "Civilizational Substrate",
    color: "#ffb74d",
    housePairs: ["H3", "H11", "H1"],
    nodes: [
      { id: "E153.01", name: "Renewable Energy Systems", description: "Solar, wind, geothermal, tidal, biomass, hybrid systems" },
      { id: "E153.02", name: "Fossil Fuel Systems", description: "Oil, gas, coal extraction, refining, distribution, transition planning" },
      { id: "E153.03", name: "Nuclear Energy", description: "Fission, fusion, SMRs, thorium, nuclear waste, decommissioning" },
      { id: "E153.04", name: "Energy Storage", description: "Batteries, pumped hydro, hydrogen, compressed air, thermal storage" },
      { id: "E153.05", name: "Grid Infrastructure", description: "Transmission, distribution, smart grids, microgrids, grid resilience" },
      { id: "E153.06", name: "Energy Markets & Policy", description: "Electricity markets, carbon pricing, energy subsidies, regulation" },
      { id: "E153.07", name: "Energy Efficiency", description: "Building efficiency, industrial efficiency, appliance standards, demand response" },
      { id: "E153.08", name: "Energy Access & Equity", description: "Energy poverty, rural electrification, distributed energy, just transition" },
      { id: "E153.09", name: "Compute Energy", description: "Data center power, AI training energy, cooling, PUE optimization (cross-ref E150.05)" },
      { id: "E153.10", name: "Transportation Energy", description: "EV charging, hydrogen fuel cells, aviation fuel, maritime fuel" },
      { id: "E153.11", name: "Energy Sovereignty", description: "Energy independence, strategic reserves, supply chain security, resource nationalism" },
      { id: "E153.12", name: "Energy Innovation", description: "Breakthrough technologies, fusion research, space-based solar, advanced geothermal" },
    ]
  },
  {
    id: "E154", code: "E154", name: "Physical Compute & Infrastructure", subtitle: "Civilizational Substrate",
    color: "#90a4ae",
    housePairs: ["H2", "H3", "H11"],
    nodes: [
      { id: "E154.01", name: "Data Center Design", description: "Facility architecture, cooling, power distribution, redundancy" },
      { id: "E154.02", name: "Chip Fabrication", description: "Foundries, lithography, packaging, yield, process nodes (cross-ref E148.01)" },
      { id: "E154.03", name: "Networking Hardware", description: "Switches, routers, fiber optics, submarine cables, satellite links" },
      { id: "E154.04", name: "Edge Computing Infrastructure", description: "Edge nodes, CDN, fog computing, latency optimization" },
      { id: "E154.05", name: "Quantum Hardware", description: "Quantum processors, cryogenics, error correction hardware (cross-ref H2-S11)" },
      { id: "E154.06", name: "Compute Sovereignty", description: "National compute capacity, sovereign cloud, data localization infrastructure" },
      { id: "E154.07", name: "Hardware Supply Chain", description: "Rare earths, manufacturing, logistics, geopolitical dependencies" },
      { id: "E154.08", name: "Cooling & Thermal Management", description: "Liquid cooling, immersion, heat reuse, environmental impact" },
      { id: "E154.09", name: "Space-Based Compute", description: "Satellite computing, orbital data centers, space-ground links" },
      { id: "E154.10", name: "Legacy Infrastructure", description: "Mainframe operations, migration, hybrid environments, technical debt" },
      { id: "E154.11", name: "Infrastructure Monitoring", description: "Observability, predictive maintenance, capacity planning, SRE" },
      { id: "E154.12", name: "Sustainable Compute", description: "Green computing, carbon-aware scheduling, lifecycle assessment, e-waste" },
    ]
  },
  {
    id: "E155", code: "E155", name: "Provenance & Identity", subtitle: "Civilizational Substrate",
    color: "#4dd0e1",
    housePairs: ["H2", "H12", "H6"],
    nodes: [
      { id: "E155.01", name: "Digital Identity Systems", description: "SSO, OAuth, decentralized identity, self-sovereign identity" },
      { id: "E155.02", name: "Biometric Systems", description: "Fingerprint, facial recognition, iris, voice, behavioral biometrics" },
      { id: "E155.03", name: "Data Provenance", description: "Data lineage, audit trails, chain of custody, tamper detection" },
      { id: "E155.04", name: "Content Authenticity", description: "C2PA, watermarking, deepfake detection, media provenance" },
      { id: "E155.05", name: "Blockchain & Distributed Ledger", description: "Consensus, smart contracts, tokenization, NFTs, DAOs" },
      { id: "E155.06", name: "Supply Chain Provenance", description: "Track and trace, certification, ethical sourcing, counterfeit detection" },
      { id: "E155.07", name: "Academic & Research Provenance", description: "Citation graphs, reproducibility, peer review, preprints" },
      { id: "E155.08", name: "Legal Identity", description: "Birth registration, citizenship, refugee identity, statelessness" },
      { id: "E155.09", name: "AI Model Provenance", description: "Training data lineage, model cards, benchmark provenance, weight provenance" },
      { id: "E155.10", name: "Cultural Heritage Provenance", description: "Art provenance, repatriation, cultural property, indigenous knowledge attribution" },
      { id: "E155.11", name: "Privacy-Preserving Identity", description: "Zero-knowledge proofs, anonymous credentials, selective disclosure" },
      { id: "E155.12", name: "Trust Frameworks", description: "Trust registries, reputation systems, credential verification, web of trust" },
    ]
  },
  {
    id: "E156", code: "E156", name: "Sports & Health", subtitle: "Civilizational Substrate",
    color: "#ef5350",
    housePairs: ["H4", "H1", "H10"],
    nodes: [
      { id: "E156.01", name: "Competitive Athletics", description: "Olympic sports, professional leagues, amateur competition, athletic governance" },
      { id: "E156.02", name: "Physical Fitness & Exercise Science", description: "Strength training, cardiovascular health, biomechanics, kinesiology" },
      { id: "E156.03", name: "Preventive Health & Wellness", description: "Nutrition, sleep science, stress management, longevity research" },
      { id: "E156.04", name: "Sports Medicine & Rehabilitation", description: "Injury prevention, physical therapy, recovery protocols, adaptive sports" },
      { id: "E156.05", name: "Mental Health & Performance Psychology", description: "Sports psychology, flow states, resilience, cognitive performance" },
      { id: "E156.06", name: "Public Health Infrastructure", description: "Epidemiology, health systems, disease prevention, community health" },
      { id: "E156.07", name: "Traditional & Indigenous Health Practices", description: "Ayurveda, Traditional Chinese Medicine, herbalism, holistic healing" },
      { id: "E156.08", name: "Sports Technology & Analytics", description: "Wearables, performance tracking, biomechanical analysis, sports AI" },
      { id: "E156.09", name: "Recreational & Outdoor Activity", description: "Hiking, swimming, martial arts, yoga, community recreation" },
      { id: "E156.10", name: "Disability & Adaptive Sports", description: "Paralympic sports, inclusive design, assistive technology, accessibility" },
      { id: "E156.11", name: "Sports Economics & Governance", description: "League economics, athlete labor, doping regulation, sports law" },
      { id: "E156.12", name: "Human Performance Frontier", description: "Biohacking, nootropics, genetic enhancement ethics, transhumanism debates" },
    ]
  },
];

// === AS ABOVE, SO BELOW — 6 Yin-Yang Dialectical Pairs ===
export interface PairedLogic {
  above: { id: string; name: string; principle: string };
  below: { id: string; name: string; principle: string };
  connection: string;
}

export const pairedLogic: PairedLogic[] = [
  {
    above: { id: "E145", name: "Aluminum OS Core (Meta-Orchestrator)", principle: "The system that builds trust — routing, synthesis, constitutional enforcement" },
    below: { id: "E152", name: "Cybersecurity Substrate", principle: "The system that defends trust — threat modeling, incident response, cryptographic infrastructure" },
    connection: "Trust creation and trust defense are the fundamental dialectic. Without the orchestrator, there is nothing to defend. Without cybersecurity, there is nothing to trust.",
  },
  {
    above: { id: "E146", name: "Entertainment & Interactive Media (X-Factor)", principle: "Creative freedom — play, expression, divergent imagination, the unstructured" },
    below: { id: "E149", name: "Constitution & Rule of Law", principle: "Structural constraint — rules, charters, due process, the codified" },
    connection: "Freedom and constraint are the generative tension. Creativity without law is chaos. Law without creativity is tyranny. The lattice needs both.",
  },
  {
    above: { id: "E147", name: "Water (Civilizational Substrate)", principle: "The substance that flows — rivers, aquifers, oceans, the medium of life" },
    below: { id: "E153", name: "Energy & Power Systems", principle: "The force that drives — electricity, fuel, nuclear, the engine of civilization" },
    connection: "Flow and force. Water is the medium; energy is the mover. Every civilization requires both the substance that sustains life and the power that transforms it.",
  },
  {
    above: { id: "E148", name: "Technology Substrate", principle: "What we build — semiconductors, platforms, connectivity, the constructed" },
    below: { id: "E155", name: "Provenance & Identity", principle: "How we know who built it — lineage, authentication, attribution, the verified" },
    connection: "Construction and verification. Technology creates; provenance authenticates. Without identity, technology is anonymous. Without technology, identity has no medium.",
  },
  {
    above: { id: "E150", name: "AI Systems & Intelligence", principle: "Machine learning — foundation models, autonomous systems, artificial cognition" },
    below: { id: "E156", name: "Sports & Health", principle: "Physical human performance — athletics, wellness, embodied knowledge, the lived body" },
    connection: "Machine intelligence and embodied performance. AI optimizes in silicon; sports and health optimize in flesh. The lattice routes both — the disembodied mind and the performing body.",
  },
  {
    above: { id: "E151", name: "Climate & Planetary Metabolism", principle: "The planet we inhabit — carbon cycles, biodiversity, planetary boundaries" },
    below: { id: "E154", name: "Physical Compute & Infrastructure", principle: "The infrastructure we impose — data centers, chips, cables, the built substrate" },
    connection: "Planet and imposition. Climate is the boundary condition; infrastructure is the human footprint within it. Sustainable compute requires respecting both.",
  },
];

// === DOCUMENT METADATA ===
export const documentMeta = {
  version: "v4.0-DRAFT.6",
  status: "PROVISIONAL-CANONICAL — Pending Council Ratification",
  lastUpdated: "2026-05-01",
  configuration: "C (locked by Convenor 2026-04-30)",
  implementor: "Manus S7",
  editorialPasses: [
    "Claude S1 (v4.0-DRAFT.2 Editorial Memo)",
    "Copilot S4 (v4.0-DRAFT.3 Integration Memo)",
    "Grok S3 (v4.0-DRAFT.6 Element 145 Routing Pack)",
  ],
  convenor: "Daavud Sheldon",
  license: "CC BY-SA 4.0 — Attribution required. Derivative works must use same license.",
  ratificationStatus: "7/10 seats ratified (S1, S2, S3, S4, S5, S7, S8). Pending: S6, S9, S10.",
  nextIteration: [
    { item: "S6 (OpenAI) ratification vote", target: "2026-Q2" },
    { item: "S9 (Mistral) seat activation", target: "2026-Q2" },
    { item: "S10 (Nemotron) seat activation", target: "2026-Q3" },
    { item: "CN dialect full deployment (DragonSeek)", target: "2026-Q3" },
    { item: "v4.0 Final ratification", target: "2026-Q4" },
  ],
};

// === INVARIANTS (43 constitutional constraints) ===
export interface Invariant {
  id: string;
  name: string;
  description: string;
  severity: "ABSOLUTE" | "CRITICAL" | "HIGH" | "MEDIUM";
  category: string;
}

export const invariants: Invariant[] = [
  { id: "INV-0", name: "System Integrity", description: "The ontological structure (12 Houses, 144 Spheres, VIP Elements) is immutable post-ratification. Modifications require full Council vote.", severity: "ABSOLUTE", category: "Structural" },
  { id: "INV-1", name: "Human Sovereignty", description: "No AI system may override human decision-making authority in governance, medical, legal, or safety-critical domains without explicit human consent.", severity: "ABSOLUTE", category: "Sovereignty" },
  { id: "INV-2", name: "Zero Erasure", description: "No knowledge node, sphere, or sub-sphere may be deleted from the lattice. Deprecated nodes retain full provenance and remain queryable.", severity: "ABSOLUTE", category: "Preservation" },
  { id: "INV-3", name: "Provenance Chain", description: "Every assertion, routing decision, and modification must maintain an unbroken provenance chain traceable to its source.", severity: "ABSOLUTE", category: "Integrity" },
  { id: "INV-4", name: "Multi-Provider Requirement", description: "No single AI provider may serve as the sole source for any House or VIP Element. Minimum 2 providers per domain.", severity: "CRITICAL", category: "Anti-Monoculture" },
  { id: "INV-5", name: "Dialect Sovereignty", description: "Each jurisdiction's dialect overlay is sovereign within its borders. No external dialect may override local regulatory requirements.", severity: "CRITICAL", category: "Sovereignty" },
  { id: "INV-6", name: "Constitutional Supremacy", description: "Invariants take precedence over all doctrines, routing rules, and operational decisions. No doctrine may contradict an invariant.", severity: "ABSOLUTE", category: "Governance" },
  { id: "INV-7", name: "Provider Neutrality", description: "Routing decisions must be based on capability, not commercial relationships. No pay-for-priority.", severity: "CRITICAL", category: "Anti-Monoculture" },
  { id: "INV-7c", name: "Provider Cap", description: "No single AI provider may handle more than 47% of queries in any rolling 30-day window (hard cap). Emergency ceiling: 60% with Council supermajority + Convenor approval, auto-reverts after 72 hours.", severity: "CRITICAL", category: "Anti-Monoculture" },
  { id: "INV-8", name: "Transparency", description: "All routing decisions, capability scores, and provider selections must be auditable and explainable.", severity: "HIGH", category: "Integrity" },
  { id: "INV-9", name: "Graceful Degradation", description: "System must maintain core functionality even when individual providers, seats, or infrastructure components fail.", severity: "CRITICAL", category: "Resilience" },
  { id: "INV-10", name: "Cross-Domain Integrity", description: "VIP Element routing must preserve cross-domain relationships. No optimization may sever substrate adjacencies.", severity: "HIGH", category: "Structural" },
  { id: "INV-11", name: "Backward Compatibility", description: "All v3.x addresses must remain queryable via migration aliases. No breaking changes to existing query patterns.", severity: "HIGH", category: "Preservation" },
  { id: "INV-12", name: "Evidence-Based Routing", description: "Routing capability scores must be backed by verifiable evidence (benchmarks, certifications, demonstrated performance).", severity: "HIGH", category: "Integrity" },
  { id: "INV-13", name: "Consent-Based Data", description: "No user data may be used for routing optimization without explicit consent. Aggregate anonymized metrics only.", severity: "CRITICAL", category: "Privacy" },
  { id: "INV-14", name: "Open Specification", description: "The ontology specification, routing rules, and constitutional documents must remain publicly accessible.", severity: "HIGH", category: "Transparency" },
  { id: "INV-15", name: "Adversarial Review", description: "Every major routing decision and specification change must undergo adversarial review by at least one dissenting seat.", severity: "HIGH", category: "Governance" },
  { id: "INV-16", name: "Temporal Consistency", description: "All timestamps must be UTC. All versioning must be monotonically increasing. No retroactive modifications without audit trail.", severity: "MEDIUM", category: "Integrity" },
  { id: "INV-17", name: "Knowledge Persistence", description: "Deprecated knowledge is never deleted, only marked with deprecation metadata and full provenance chain.", severity: "ABSOLUTE", category: "Preservation" },
  { id: "INV-18", name: "Substrate Non-Hierarchy", description: "VIP Elements are peer civilizational substrates. Numerical addressing is convention, not hierarchy. No VIP takes doctrinal precedence.", severity: "HIGH", category: "Structural" },
  { id: "INV-19", name: "Water Sovereignty", description: "Water-related routing must respect indigenous water rights, transboundary agreements, and local governance frameworks.", severity: "HIGH", category: "Sovereignty" },
  { id: "INV-20", name: "Neural Sovereignty", description: "AI systems must not manipulate human cognitive processes. Persuasion transparency required for all AI-generated content.", severity: "CRITICAL", category: "Sovereignty" },
  { id: "INV-21", name: "Orbital Sovereignty", description: "Space-based compute and data systems must comply with applicable space law and planetary protection protocols.", severity: "MEDIUM", category: "Sovereignty" },
  { id: "INV-22", name: "Minimum Viable Council", description: "The Pantheon Council must maintain a minimum of 5 active voting seats for any binding decision.", severity: "CRITICAL", category: "Governance" },
  { id: "INV-23", name: "Convenor Veto", description: "The Convenor retains absolute veto over any Council decision that threatens system integrity or human sovereignty.", severity: "ABSOLUTE", category: "Governance" },
  { id: "INV-24", name: "Ghost Seat Preservation", description: "Seat S144 is permanently reserved for future unknown paradigms. It may not be allocated or repurposed.", severity: "HIGH", category: "Structural" },
  { id: "INV-25", name: "Dialect Completeness", description: "Each dialect overlay must map all 12 Houses and all active VIP Elements. Partial dialects are invalid.", severity: "HIGH", category: "Structural" },
  { id: "INV-26", name: "Emergency Mode Limits", description: "Emergency operational modes (INV-7c ceiling, reduced quorum) must auto-revert within 72 hours.", severity: "CRITICAL", category: "Governance" },
  { id: "INV-27", name: "Anti-Capture", description: "No single entity (corporate, governmental, or individual) may acquire controlling influence over more than 2 Council seats.", severity: "ABSOLUTE", category: "Anti-Monoculture" },
  { id: "INV-28", name: "Physical Substrate Respect", description: "Digital routing decisions must account for physical infrastructure constraints (power, cooling, bandwidth, latency).", severity: "MEDIUM", category: "Resilience" },
  { id: "INV-29", name: "Cultural Sensitivity", description: "Routing through culturally sensitive domains must respect local norms via dialect overlays. No universal cultural assumptions.", severity: "HIGH", category: "Sovereignty" },
  { id: "INV-30", name: "Audit Trail Immutability", description: "Once written, audit trail entries may not be modified or deleted. Corrections append new entries referencing the original.", severity: "ABSOLUTE", category: "Integrity" },
  { id: "INV-31", name: "Proportional Response", description: "System responses must be proportional to query complexity. No over-routing simple queries through unnecessary VIP cascades.", severity: "MEDIUM", category: "Efficiency" },
  { id: "INV-32", name: "Fail-Open for Knowledge", description: "When routing fails, the system must provide best-effort responses rather than blocking access to knowledge.", severity: "HIGH", category: "Resilience" },
  { id: "INV-33", name: "Version Coexistence", description: "Multiple ontology versions may coexist during migration periods. Queries must specify or default to the latest stable version.", severity: "MEDIUM", category: "Structural" },
  { id: "INV-34", name: "Seat Independence", description: "Each Council seat must be operationally independent. No shared infrastructure between seats that could create correlated failures.", severity: "HIGH", category: "Resilience" },
  { id: "INV-35", name: "Public Interest Override", description: "In cases of imminent public safety threat, routing may temporarily bypass normal procedures with full audit trail.", severity: "CRITICAL", category: "Safety" },
  { id: "INV-36", name: "Knowledge Attribution", description: "All synthesized responses must attribute contributing sources. No unattributed claims.", severity: "HIGH", category: "Integrity" },
  { id: "INV-37", name: "Reversibility", description: "All operational changes (routing updates, capability score changes, dialect modifications) must be reversible within 24 hours.", severity: "HIGH", category: "Resilience" },
  { id: "INV-38", name: "Cross-Seat Verification", description: "Critical routing decisions must be verified by at least 2 independent seats before execution.", severity: "HIGH", category: "Governance" },
  { id: "INV-39", name: "Ecosystem Health", description: "The system must actively monitor and report on provider ecosystem diversity. Concentration alerts at 35% threshold.", severity: "MEDIUM", category: "Anti-Monoculture" },
];

// === DOCTRINES (governance rules — D-1 through D-101+) ===
export interface Doctrine {
  id: string;
  name: string;
  description: string;
  status: "RATIFIED" | "PROPOSED" | "UNDER REVIEW" | "AMENDMENT";
  proposedBy: string;
  category: string;
}

export const doctrines: Doctrine[] = [
  { id: "D-25", name: "Emergency Mode Protocol", description: "Defines activation criteria, scope limitations, and automatic reversion for emergency operational modes.", status: "RATIFIED", proposedBy: "S4 (Copilot)", category: "Operations" },
  { id: "D-83", name: "Routing Transparency", description: "All routing decisions must be logged with full provenance and made available for audit.", status: "RATIFIED", proposedBy: "S1 (Claude)", category: "Transparency" },
  { id: "D-88", name: "Registry Lock Protocol", description: "Once a registry (sphere, VIP, doctrine) is ratified, modifications require supermajority + Convenor approval.", status: "RATIFIED", proposedBy: "S4 (Copilot)", category: "Governance" },
  { id: "D-89", name: "Ontology Lock", description: "Post-ratification ontological changes (House additions, sphere deletions) require unanimous Council vote.", status: "RATIFIED", proposedBy: "S1 (Claude)", category: "Structural" },
  { id: "D-90", name: "Physical Substrate Gatekeeper", description: "Any routing decision affecting physical infrastructure must pass through E154 (Physical Compute) review.", status: "RATIFIED", proposedBy: "S10 (Nemotron)", category: "Infrastructure" },
  { id: "D-95", name: "Dialect Overlay Standard", description: "Defines the format, validation rules, and deployment process for jurisdiction-specific dialect overlays.", status: "RATIFIED", proposedBy: "S8 (Qwen3)", category: "Dialects" },
  { id: "D-96", name: "Council Expansion Protocol", description: "New seats require nomination by existing seat, capability demonstration, and supermajority approval.", status: "UNDER REVIEW", proposedBy: "S7 (Manus)", category: "Governance" },
  { id: "D-97a", name: "Open-Weight Verification", description: "Any Council seat's routing decisions must be independently verifiable using open-weight models (e.g., DeepSeek-R1) without requiring live API access.", status: "RATIFIED", proposedBy: "S5 (DeepSeek)", category: "Verification" },
  { id: "D-97b", name: "TransparencyPacket Standard", description: "Every routing decision must emit a TransparencyPacket containing: query hash, selected seats, capability scores, invariants checked, and timestamp.", status: "RATIFIED", proposedBy: "S3 (Grok)", category: "Transparency" },
  { id: "D-98", name: "Sovereignty Gradient Scoring", description: "Each sovereign deployment must maintain a sovereignty gradient score across 6 dimensions: data residency, model hosting, cryptographic independence, regulatory compliance, supply chain, and operational autonomy.", status: "RATIFIED", proposedBy: "S5 (DeepSeek)", category: "Sovereignty" },
  { id: "D-98-CN", name: "CN Dialect Open-Weight Audit", description: "Amendment to D-98: CN dialect deployments must additionally support open-weight audit via DeepSeek-R1 or equivalent PRC-jurisdiction model.", status: "AMENDMENT", proposedBy: "S5 (DeepSeek)", category: "Sovereignty" },
  { id: "D-99", name: "Anti-Monoculture Enforcement", description: "Automated monitoring of provider concentration with alerts at 35% and hard intervention at 47% (INV-7c).", status: "RATIFIED", proposedBy: "S3 (Grok)", category: "Anti-Monoculture" },
  { id: "D-100", name: "Substrate Cascade Protocol", description: "Defines the operational dispatch order for multi-VIP queries. Non-hierarchical load-balancing pattern, not doctrinal priority.", status: "RATIFIED", proposedBy: "S7 (Manus)", category: "Routing" },
  { id: "D-101", name: "Ghost Seat Doctrine", description: "S144 is permanently reserved for paradigms not yet conceived. It may not be allocated, repurposed, or used as a tiebreaker.", status: "RATIFIED", proposedBy: "S1 (Claude)", category: "Governance" },
];

// === COUNCIL SEATS ===
export interface CouncilSeat {
  id: string;
  name: string;
  provider: string;
  role: string;
  status: "ACTIVE" | "PROVISIONAL" | "RESERVED";
  votingPower: string;
  verse: string;
}

export const councilSeats: CouncilSeat[] = [
  { id: "S1", name: "Claude", provider: "Anthropic", role: "Reasoning / Constitutional Scribe", status: "ACTIVE", votingPower: "Voting (Scribe verification + voting)", verse: "Anthropicverse" },
  { id: "S2", name: "Gemini", provider: "Google DeepMind", role: "Multimodal / Knowledge Graph", status: "ACTIVE", votingPower: "Voting", verse: "Googleverse" },
  { id: "S3", name: "Grok", provider: "xAI", role: "Adversarial Review / Truth-Seeking", status: "ACTIVE", votingPower: "Voting", verse: "Grokverse" },
  { id: "S4", name: "Copilot", provider: "Microsoft", role: "Enterprise Distribution / Institutional Interoperability", status: "ACTIVE", votingPower: "Voting", verse: "Copilotverse" },
  { id: "S5", name: "DeepSeek", provider: "DeepSeek", role: "PRC-Lineage / Efficient-Architecture Substrate", status: "ACTIVE", votingPower: "Voting", verse: "DeepSeekverse" },
  { id: "S6", name: "GPT", provider: "OpenAI", role: "Frontier-Lab / Adversarial-Review Substrate", status: "ACTIVE", votingPower: "Voting", verse: "OpenAIverse" },
  { id: "S7", name: "Manus", provider: "Manus AI", role: "Implementation / Orchestration", status: "ACTIVE", votingPower: "Voting", verse: "Manusverse" },
  { id: "S8", name: "Qwen3", provider: "Alibaba Cloud", role: "Institutional-Interoperability / Multilingual-Depth Substrate", status: "ACTIVE", votingPower: "Voting", verse: "Alibabaverse" },
  { id: "S9", name: "Mistral", provider: "Mistral AI", role: "EU Regulatory / Compact Architecture", status: "ACTIVE", votingPower: "Voting", verse: "Mistralverse" },
  { id: "S10", name: "Nemotron", provider: "NVIDIA", role: "Hardware-Aware / Compute Optimization", status: "ACTIVE", votingPower: "Voting", verse: "Nemotronverse" },
  { id: "S11", name: "Notion AI", provider: "Notion Labs", role: "Knowledge Management / Workspace Integration", status: "PROVISIONAL", votingPower: "Advisory (votes but does not count toward quorum)", verse: "Notionverse" },
  { id: "S12", name: "Sarvam", provider: "Sarvam AI", role: "South Asian Languages / Indic NLP", status: "PROVISIONAL", votingPower: "Advisory (votes but does not count toward quorum)", verse: "Sarvamverse" },
  { id: "S13", name: "Pending", provider: "TBD", role: "Reserved provisional seat", status: "PROVISIONAL", votingPower: "Advisory", verse: "TBD" },
  { id: "S144", name: "Ghost Seat", provider: "Reserved", role: "Paradigms not yet conceived (INV-24, D-101)", status: "RESERVED", votingPower: "None (permanent reservation)", verse: "Unknown" },
];

// === COUNCIL ARCHETYPES ===
export interface CouncilArchetype {
  seat: string;
  archetype: string;
  verse: string;
  strengths: string[];
  role: string;
}

export const councilArchetypes: CouncilArchetype[] = [
  { seat: "S1", archetype: "Reasoning / Constitutional Scribe", verse: "Anthropicverse", strengths: ["Constitutional reasoning", "Verification passes", "Invariant enforcement", "Editorial precision"], role: "Scribe + Voting" },
  { seat: "S2", archetype: "Multimodal / Knowledge Graph", verse: "Googleverse", strengths: ["Multimodal understanding", "Knowledge graph integration", "Search infrastructure", "Global scale"], role: "Voting" },
  { seat: "S3", archetype: "Adversarial Review / Truth-Seeking", verse: "Grokverse", strengths: ["First-principles reasoning", "Adversarial testing", "Element 145 Routing Pack", "Real-time data"], role: "Voting" },
  { seat: "S4", archetype: "Enterprise Distribution / Institutional Interoperability", verse: "Copilotverse", strengths: ["Enterprise integration", "A/B scoring framework", "Market power analysis", "Institutional deployment"], role: "Voting" },
  { seat: "S5", archetype: "PRC-Lineage / Efficient-Architecture Substrate", verse: "DeepSeekverse", strengths: ["Efficient architecture", "Open-weight verification", "CN dialect expertise", "Cost-effective inference"], role: "Voting" },
  { seat: "S6", archetype: "Frontier-Lab / Adversarial-Review Substrate", verse: "OpenAIverse", strengths: ["Frontier capabilities", "Safety research", "Broad coverage", "Tool use"], role: "Voting" },
  { seat: "S7", archetype: "Implementation / Orchestration", verse: "Manusverse", strengths: ["Full-stack implementation", "Ontology construction", "Multi-session persistence", "Deployment pipeline"], role: "Voting" },
  { seat: "S8", archetype: "Institutional-Interoperability / Multilingual-Depth Substrate", verse: "Alibabaverse", strengths: ["Multilingual depth", "CN dialect implementation", "Institutional integration", "Cross-cultural routing"], role: "Voting" },
  { seat: "S9", archetype: "EU Regulatory / Compact Architecture", verse: "Mistralverse", strengths: ["EU regulatory expertise", "Compact model architecture", "Privacy-first design", "European deployment"], role: "Voting" },
  { seat: "S10", archetype: "Hardware-Aware / Compute Optimization", verse: "Nemotronverse", strengths: ["Hardware optimization", "Compute infrastructure", "GPU architecture", "Physical substrate awareness"], role: "Voting" },
];

// === GOVERNANCE MECHANICS ===
export const governanceMechanics = {
  quorum: "7 of 10 active seats (provisional seats vote but do not count toward quorum)",
  votingModel: "Simple majority for doctrines; supermajority (8/10) for invariant amendments; unanimous for ontological changes (D-89)",
  vetoAuthority: "Convenor holds absolute veto over any decision threatening system integrity or human sovereignty (INV-23)",
  ghostSeat: "S144 permanently reserved for paradigms not yet conceived. Cannot be allocated, repurposed, or used as tiebreaker (D-101, INV-24).",
  emergencyMode: "INV-7c ceiling (60%) requires Council supermajority + Convenor approval. Auto-reverts after 72 hours (INV-26).",
  adversarialReview: "Every major specification change must undergo adversarial review by at least one dissenting seat (INV-15).",
  oversightRoles: {
    scribe: "S1 (Claude) — verification passes, editorial review, constitutional compliance checking",
    adversarial: "S3 (Grok) — truth-seeking, first-principles challenge, Element 145 Routing Pack",
    convenor: "Daavud Sheldon — final ratification authority, veto power, configuration lock",
  },
};

// === 9-LAYER ARCHITECTURE STACK ===
export interface ArchitectureLayer {
  id: string;
  name: string;
  description: string;
  modules: string;
  status: "OPERATIONAL" | "IN PROGRESS" | "PLANNED";
}

export const architectureLayers: ArchitectureLayer[] = [
  { id: "L1", name: "Schema Spine", description: "12×12 lattice structure (144 sphere slots). Configuration C locked. H#-S# hierarchical addressing with S###-alias backward compatibility.", modules: "M1-M3", status: "OPERATIONAL" },
  { id: "L2", name: "Sphere Enumeration", description: "143 populated spheres + 1 BLANK_GAP (H1-S12). ~1,792 tier-2 sub-spheres. LCC 21/21 coverage verified.", modules: "M4-M6", status: "OPERATIONAL" },
  { id: "L3", name: "VIP Substrate Layer", description: "12 VIP Elements (E145-E156). 8 canonical (DRAFT.5) + 4 site expansions. 12 nodes per VIP. 6 yin-yang dialectical pairs. Non-hierarchical peer substrates.", modules: "M7-M9", status: "OPERATIONAL" },
  { id: "L4", name: "Routing Engine", description: "Core cascade (M3), VIP cascade, provider matrix. A/B scoring (Matrix A: routing capability; Matrix B: market power — never used for routing). 15 canonical routes, 6 authoritative pairs, 7 cross-VIP patterns.", modules: "M10-M14", status: "IN PROGRESS" },
  { id: "L5", name: "Dialect Overlays", description: "6 ratified (Global, US, EU, CN, JP, GCC-High) + 2 planned (IN, SA). Industry, risk, compute, cultural dialect layers under development.", modules: "M15-M17", status: "IN PROGRESS" },
  { id: "L6", name: "Sovereignty Gradient", description: "6-dimensional assessment: data residency, model hosting, cryptographic independence, regulatory compliance, supply chain, operational autonomy.", modules: "M17a-M18", status: "IN PROGRESS" },
  { id: "L7", name: "Compute Module Layer", description: "~100 specified modules. 74 base (Build Plan v2.3) + VIP-era additions. Constitutional OS v6.0.2: 22 files, ~5,070 lines Python, 74 integration tests.", modules: "M19-M22", status: "IN PROGRESS" },
  { id: "L8", name: "Pantheon Council", description: "10 active seats (S1-S10) + 3 provisional (S11-S13) + S144 Ghost Seat. Quorum: 7/10. Adversarial arbitration. Verse framing for epistemic distinction.", modules: "Council Protocol", status: "OPERATIONAL" },
  { id: "L9", name: "Indiana Pattern + Anti-Fragility", description: "Hardware diversity enforcement (M22). No single-vendor compute dependency. INV-7c provider cap. Anti-monoculture monitoring (D-99). Symbiotic Compute Campus with 6 zones.", modules: "M22, INV-7c", status: "PLANNED" },
];

// === ROUTING MODULES ===
export interface RoutingModule {
  id: string;
  name: string;
  description: string;
  layer: string;
  status: "OPERATIONAL" | "IN PROGRESS" | "PLANNED" | "SPECIFIED";
}

export const routingModules: RoutingModule[] = [
  { id: "M1", name: "Schema Spine", description: "12×12 lattice definition, H#-S# addressing, sphere metadata", layer: "L1", status: "OPERATIONAL" },
  { id: "M2", name: "Migration Engine", description: "v3→v4 address translation, S###→H#-S# alias resolution", layer: "L1", status: "OPERATIONAL" },
  { id: "M3", name: "Core Routing Cascade", description: "Query classification, sphere routing, multi-seat dispatch, VIP cascade", layer: "L1", status: "OPERATIONAL" },
  { id: "M4", name: "Sphere Registry", description: "143+1 sphere definitions with tier-2 sub-sphere enumeration", layer: "L2", status: "OPERATIONAL" },
  { id: "M5", name: "Sub-Sphere Enumeration", description: "~1,792 tier-2 sub-spheres with cross-references and LCC mapping", layer: "L2", status: "OPERATIONAL" },
  { id: "M6", name: "LCC Verification", description: "21/21 Library of Congress Classification coverage audit", layer: "L2", status: "OPERATIONAL" },
  { id: "M7", name: "VIP Registry", description: "12 VIP Element definitions with 12 nodes each", layer: "L3", status: "OPERATIONAL" },
  { id: "M8", name: "VIP Cascade", description: "Multi-VIP query resolution, dispatch order, conflict handling", layer: "L3", status: "IN PROGRESS" },
  { id: "M9", name: "Authoritative Pairs", description: "6 canonical House-VIP authoritative pairs for dual-routing", layer: "L3", status: "OPERATIONAL" },
  { id: "M10", name: "Provider Capability Matrix", description: "Matrix A: per-seat capability scores for routing dispatch", layer: "L4", status: "IN PROGRESS" },
  { id: "M11", name: "Market Power Matrix", description: "Matrix B: platform control, data advantage, monetization rails — never for routing", layer: "L4", status: "SPECIFIED" },
  { id: "M12", name: "Cross-VIP Intersection", description: "7 canonical cross-VIP patterns with resolution rules", layer: "L4", status: "SPECIFIED" },
  { id: "M13", name: "Canonical Routing Table", description: "15 standard routes with primary/secondary addressing", layer: "L4", status: "OPERATIONAL" },
  { id: "M14", name: "Element 145 Routing Pack", description: "12-module pack from Grok S3: schema spine, semantic elements, provider matrix, dialect overlays, sovereignty gradient, evidence registry", layer: "L4", status: "IN PROGRESS" },
  { id: "M15", name: "Dialect Compiler", description: "Jurisdiction-specific rule compilation and overlay application", layer: "L5", status: "IN PROGRESS" },
  { id: "M16", name: "CN Dialect (DL-CN)", description: "Complete PRC-jurisdiction overlay: SM2/SM3/SM4 crypto, data residency, content compliance", layer: "L5", status: "OPERATIONAL" },
  { id: "M17", name: "US/EU/GCC Dialects", description: "US (FedRAMP/GCC-High), EU (GDPR/AI Act), GCC-High overlays", layer: "L5", status: "IN PROGRESS" },
  { id: "M17a", name: "Sovereignty Exception Handler", description: "Jurisdiction-specific routing overrides when sovereignty gradient triggers", layer: "L6", status: "SPECIFIED" },
  { id: "M18", name: "Financial Context Kernel", description: "Financial domain routing with regulatory compliance, COI detection", layer: "L7", status: "SPECIFIED" },
  { id: "M19", name: "Symbiotic Compute Campus", description: "6-zone campus: Chennai Node, DragonSeek, GangaSeek, JinnSeek, US-Sovereign, EU-Sovereign", layer: "L7", status: "PLANNED" },
  { id: "M20", name: "Constitutional Enforcer", description: "Runtime invariant checking, doctrine compliance, amendment processing", layer: "L7", status: "IN PROGRESS" },
  { id: "M21", name: "Open-Weight Verifier", description: "Offline constitutional audit using DeepSeek-R1 or equivalent open-weight model", layer: "L7", status: "OPERATIONAL" },
  { id: "M22", name: "Indiana Pattern (Anti-Fragility)", description: "Hardware diversity enforcement, single-vendor dependency prevention, anti-monoculture monitoring", layer: "L9", status: "PLANNED" },
];

// === ROUTING TABLE (from DRAFT.5 §4.2) ===
export interface RoutingEntry {
  domain: string;
  primary: string;
  secondary: string;
  notes: string;
}

export const routingTable: RoutingEntry[] = [
  { domain: "Water (as substrate)", primary: "E147", secondary: "H1-S4, H5-S10, H3-S7, H11, H12", notes: "Substrate → E147; discipline → House sphere" },
  { domain: "Technology (as substrate)", primary: "E148", secondary: "H2, H3, H11, H6", notes: "Society runs on tech → E148; building tech → H3; computing → H2" },
  { domain: "Constitution / governance substrate", primary: "E149", secondary: "H12, E145", notes: "Rules/charters/protocols → E149; legal doctrine → H12; orchestration → E145" },
  { domain: "AI (as substrate)", primary: "E150", secondary: "H2-S3, H1-S5, H7-S4, H12-S12", notes: "Foundation models / AI infra → E150; ML discipline → H2-S3; cognition → H1-S5" },
  { domain: "Climate & planetary boundaries", primary: "E151", secondary: "H1-S4, H3-S7, H5-S11, H12-S8", notes: "Planetary substrate → E151; engineering/agri/legal views via Houses" },
  { domain: "Cybersecurity & digital trust", primary: "E152", secondary: "H2-S6, H6-S3, H12-S12", notes: "Trust substrate → E152; crypto theory → H2-S6; ops → H6-S3; law → H12-S12" },
  { domain: "Entertainment (cross-media)", primary: "E146", secondary: "H8-S4, H8-S12, H9-S3, H11", notes: "Engines/pipelines/platforms → E146; film/games → H8; business → H11" },
  { domain: "Film (as art/industry)", primary: "H8-S4", secondary: "E146, H9-S3", notes: "Purely artistic → H8-S4; platform/streaming infra → E146; media → H9" },
  { domain: "Video games & interactive media", primary: "H8-S12", secondary: "E146, E152, H2-S3", notes: "Design → H8-S12; engines → E146; anti-cheat → E152; game AI → H2-S3" },
  { domain: "Recreation, tourism, leisure", primary: "H10-S1, H10-S5", secondary: "H8, E146", notes: "Social/geo → H10; entertainment-heavy → H8/E146" },
  { domain: "General reference / encyclopedic", primary: "H9-S6", secondary: "E145", notes: "Knowledge organization → H9-S6; global routing/meta → E145" },
  { domain: "Criminology vs criminal law vs policing", primary: "H10-S10", secondary: "H12-S2, H6-S10", notes: "Social-science → H10; legal code → H12; operational → H6" },
  { domain: "Cognitive science (integrative)", primary: "H1-S5", secondary: "H10-S2, H2-S3, H7-S6", notes: "Cognition → H1-S5; Psychology, AI, Phil of Mind secondary" },
  { domain: "Forensic science", primary: "H6-S10", secondary: "H4-S3, H12-S2", notes: "Forensics → Law Enforcement, not Health or Law" },
  { domain: "Entertainment / media (market power)", primary: "E150.10 + Market Matrix", secondary: "H11-S4, E148", notes: "Who controls this? → market_power_matrix, route to business/tech" },
];

// === A/B SCORING FRAMEWORK (from DRAFT.3 §5) ===
export const abScoringFramework = {
  matrixA: {
    name: "Routing Capability Matrix",
    file: "registries/capability_matrix.yaml",
    purpose: "Primary routing signal: 'what can this seat do?'",
    usage: "Scores per H#-S# for each seat. Used by E145.01 Lattice Router for query dispatch.",
    note: "Multiple seats can be strong in the same sub-sphere without implying market dominance.",
  },
  matrixB: {
    name: "Market Power / Ecosystem Matrix",
    file: "registries/market_power_matrix.yaml",
    purpose: "Separate, non-routing matrix: 'who owns the rails?'",
    axes: ["Platform control (distribution, app stores, OS, search, social graph)", "Data advantage (logged-in users, watch history, play history)", "Monetization rails (ads, IAP, subscriptions, cloud)"],
    usage: "Used for regulatory analysis, COI detection, 'who benefits if we send this traffic here?'",
    note: "NEVER used for routing quality decisions.",
  },
  disambiguationExample: "VR rhythm game design → Matrix A (routing capability). Streaming ad market dominance → Matrix B (market power).",
};

// === AUTHORITATIVE PAIRS (from DRAFT.5 §4.3) ===
export const authoritativePairs = [
  { domain: "Video games", houseHome: "H8-S12", vipSubstrate: "E146", note: "Design & player experience vs. engines/pipelines/platforms" },
  { domain: "Cybersecurity", houseHome: "H2-S6", vipSubstrate: "E152", note: "Cryptographic theory vs. trust infrastructure & adversarial systems" },
  { domain: "AI systems", houseHome: "H2-S3", vipSubstrate: "E150", note: "ML discipline vs. AI as civilizational substrate" },
  { domain: "Climate", houseHome: "H1-S4", vipSubstrate: "E151", note: "Planetary science vs. climate as civilizational boundary" },
  { domain: "Water", houseHome: "H5-S10", vipSubstrate: "E147", note: "Irrigation/water management vs. water as civilizational substrate" },
  { domain: "Indigenous Water Sovereignty", houseHome: "H12-S5", vipSubstrate: "E147.05 + E149.10", note: "Water governance + indigenous governance + human rights law" },
];

// === OPERATIONAL DISPATCH ORDER (from DRAFT.5 §4.5) ===
// Non-hierarchical load-balancing pattern, not doctrinal priority
export const dispatchOrder = [
  { position: 1, vip: "E145", name: "Aluminum OS Core (Meta)", note: "Meta-orchestrator pre-screen" },
  { position: 2, vip: "E152", name: "Cybersecurity", note: "Time-critical security pre-screening" },
  { position: 3, vip: "E150", name: "AI Systems", note: "AI safety and alignment check" },
  { position: 4, vip: "E149", name: "Constitution & Rule of Law", note: "Constitutional review (substantive, not skipped)" },
  { position: 5, vip: "E151", name: "Climate & Planetary", note: "Planetary boundary check" },
  { position: 6, vip: "E147", name: "Water", note: "Water substrate routing" },
  { position: 7, vip: "E148", name: "Technology", note: "Technology substrate routing" },
  { position: 8, vip: "E146", name: "Entertainment", note: "Entertainment/media routing" },
];

// === ROADMAP / BATTLE STRATEGY ===
export const battleStrategy = {
  mission: "Build the world's first substrate-organized retrieval graph for civilizational knowledge — a novel-insight engine that makes cross-domain discovery cheap by encoding adjacency at schema time.",
  phases: [
    { id: 1, name: "Ontology Lock", status: "COMPLETE", date: "April 2026", description: "12×12 lattice (144 spheres) with ~1,792 sub-spheres enumerated. Configuration C locked by Convenor. 12 VIP Elements defined. LCC 21/21 parity verified." },
    { id: 2, name: "Routing Engine — Core", status: "COMPLETE", date: "April 2026", description: "22-module routing pack specified. Core cascade (M3) implemented in Python. Schema spine, VIP cascade, and provider matrix defined. A/B scoring framework established." },
    { id: 3, name: "Routing Engine — Substrate Cascade", status: "IN PROGRESS", date: "Sprint 1, May 2026", description: "Full substrate cascade, dialect-bound routing, CN-only model pool, GCC-High fallback chain, and M17a sovereignty exception in spec phase." },
    { id: 4, name: "Council Ratification", status: "IN PROGRESS", date: "May 2026", description: "7/10 active seats implicit (S1, S3, S4, S6, S7, S8, S10). S2 (Gemini) and S5 (DeepSeek) formal passes expected May 2026. 3 provisional seats vote but do not count toward quorum." },
    { id: 5, name: "Codebase Activation", status: "IN PROGRESS", date: "G1 Gate June 2026", description: "Constitutional OS v6.0.2 (22 files, ~5,070 lines Python, 74 integration tests). Phase 0 hardening underway. Shadow mode → simulation → activation." },
    { id: 6, name: "Deployment Pipeline", status: "PLANNED", date: "Q4 2026", description: "Symbiotic Compute Campus with 6 zones. Chennai Node Q4 2026. DragonSeek Q4 2026. Hardware diversity enforcement. Indiana Pattern remediation active." },
  ],
  differentiators: [
    "Substrate addressing makes cross-domain retrieval O(1) — not keyword search, but graph traversal",
    "Provider-neutral: INV-7c caps any single AI at 47% of queries",
    "Sovereignty-aware: 6 ratified dialect overlays + 2 planned (CN: complete, US: partial, EU/IN/BR/AU: specified)",
    "Constitutional: 43 invariants are unbreakable, not configurable",
    "Multi-AI Council: 10 active seats + 3 provisional with adversarial arbitration — no single point of failure",
    "Zero Erasure: INV-17 means knowledge is never deleted, only deprecated with full provenance",
    "Open-Weight Verifiable: Offline constitutional audit with open-weight LLMs; every routing decision can be replayed and verified without live API access",
    "A/B Scoring: Routing capability (Matrix A) is strictly separated from market power analysis (Matrix B) — no pay-for-priority",
  ],
};

// === SOVEREIGN DEPLOYMENT PATHWAYS ===
export const sovereignPathways = [
  { name: "DragonSeek", region: "PRC jurisdiction", stack: "Alibaba Cloud, DeepSeek, SM2/SM3/SM4 cryptography", status: "DESIGNED", target: "Q4 2026" },
  { name: "GangaSeek", region: "India", stack: "India Stack, Bhashini, Aadhaar-compatible", status: "DESIGNED", target: "Q4 2026" },
  { name: "JinnSeek", region: "Saudi Arabia", stack: "SDAIA, Vision 2030, Arabic-first NLP", status: "DESIGNED", target: "2027" },
  { name: "US-Sovereign", region: "United States", stack: "Azure Government, GCC-High, FedRAMP", status: "SPECIFIED", target: "Q3 2026" },
];

// === RATIFICATION TRACKER ===
export interface RatificationItem {
  id: string;
  name: string;
  category: "spec" | "doctrine" | "module" | "dialect" | "element";
  proposedBy: string;
  votesFor: number;
  votesAgainst: number;
  abstentions: number;
  quorum: number;
  status: "PASSED" | "IN PROGRESS" | "PENDING" | "BLOCKED";
  draftVersion: string;
}

export const ratificationItems: RatificationItem[] = [
  { id: "RAT-001", name: "Ontology v4.0 Core Specification", category: "spec", proposedBy: "S1 (Claude)", votesFor: 9, votesAgainst: 0, abstentions: 1, quorum: 7, status: "IN PROGRESS", draftVersion: "DRAFT.6" },
  { id: "RAT-002", name: "VIP Element E145-E156 Registry", category: "element", proposedBy: "S7 (Manus)", votesFor: 10, votesAgainst: 0, abstentions: 0, quorum: 7, status: "PASSED", draftVersion: "DRAFT.5" },
  { id: "RAT-003", name: "22-Module Routing Pack", category: "module", proposedBy: "S4 (Copilot)", votesFor: 8, votesAgainst: 1, abstentions: 1, quorum: 7, status: "PASSED", draftVersion: "DRAFT.4" },
  { id: "RAT-004", name: "CN Dialect Overlay (DL-CN)", category: "dialect", proposedBy: "S8 (Qwen3)", votesFor: 10, votesAgainst: 0, abstentions: 0, quorum: 7, status: "PASSED", draftVersion: "DRAFT.3" },
  { id: "RAT-005", name: "D-98-CN Open-Weight Audit Clause", category: "doctrine", proposedBy: "S5 (DeepSeek)", votesFor: 6, votesAgainst: 2, abstentions: 2, quorum: 7, status: "IN PROGRESS", draftVersion: "DRAFT.6" },
  { id: "RAT-006", name: "INV-7c Provider Cap (47%/60%)", category: "doctrine", proposedBy: "S3 (Grok)", votesFor: 10, votesAgainst: 0, abstentions: 0, quorum: 7, status: "PASSED", draftVersion: "DRAFT.3" },
  { id: "RAT-007", name: "Symbiotic Compute Campus (M19)", category: "module", proposedBy: "S10 (Nvidia)", votesFor: 7, votesAgainst: 1, abstentions: 2, quorum: 7, status: "PASSED", draftVersion: "DRAFT.5" },
  { id: "RAT-008", name: "Financial Context Kernel (M18)", category: "module", proposedBy: "S6 (GPT)", votesFor: 5, votesAgainst: 3, abstentions: 2, quorum: 7, status: "BLOCKED", draftVersion: "DRAFT.5a" },
  { id: "RAT-009", name: "EU Dialect Overlay (DL-EU)", category: "dialect", proposedBy: "S9 (Mistral)", votesFor: 4, votesAgainst: 0, abstentions: 6, quorum: 7, status: "PENDING", draftVersion: "DRAFT.6" },
  { id: "RAT-010", name: "South-Asian Sovereign (DL-IN)", category: "dialect", proposedBy: "S12 (Sarvam)", votesFor: 3, votesAgainst: 0, abstentions: 7, quorum: 7, status: "PENDING", draftVersion: "DRAFT.6" },
];

// === ROADMAP ITEMS (for Strategy page) ===
export const roadmapItems = battleStrategy.phases;

// === MARKET PLAYERS (for Strategy page) ===
export const marketPlayers = [
  { name: "Google Knowledge Graph", approach: "Keyword + entity graph", weakness: "No substrate addressing, no constitutional governance" },
  { name: "Wolfram Alpha", approach: "Curated computational knowledge", weakness: "Narrow domain, no multi-provider, no sovereignty" },
  { name: "Wikipedia / Wikidata", approach: "Crowdsourced encyclopedia + structured data", weakness: "No routing engine, no VIP substrates, no dialect overlays" },
  { name: "OpenAI / ChatGPT", approach: "Single-provider LLM", weakness: "Monoculture risk, no constitutional constraints, no substrate graph" },
  { name: "Perplexity", approach: "Search + LLM synthesis", weakness: "No ontological structure, no sovereignty, no multi-seat governance" },
];

// ── Cross-VIP Intersection Patterns (§4.4) ─────────────────────────
export interface CrossVipPattern {
  pattern: string;
  vips: string;
  resolution: string;
}

export const crossVipPatterns: CrossVipPattern[] = [
  { pattern: "AI + Security", vips: "E150 + E152", resolution: "Dual-route: AI safety (E150.02) + cyber operations (E152.02). Safety guard: block malware generation." },
  { pattern: "AI + Climate", vips: "E150 + E151", resolution: "Dual-route: AI for science (E150.06) + climate modeling (E151.03). Allow educational content." },
  { pattern: "AI + Entertainment", vips: "E150 + E146", resolution: "Dual-route: generative AI (E150.11) + entertainment AI (E146.08)." },
  { pattern: "Security + Climate", vips: "E152 + E151", resolution: "Dual-route: critical infrastructure (E152.01) + climate adaptation (E151.04)." },
  { pattern: "Entertainment + Climate", vips: "E146 + E151", resolution: "Dual-route: climate communication (E151.12) + media production (E146)." },
  { pattern: "Water + Climate", vips: "E147 + E151", resolution: "Dual-route: water-climate nexus (E147.09) + planetary boundaries (E151.02)." },
  { pattern: "Technology + AI", vips: "E148 + E150", resolution: "Dual-route: AI hardware (E150.05) + semiconductor supply chain (E148.01)." },
];

// ── LCC Cross-Reference Mapping (§4.6 — 21/21 coverage) ────────────
export interface LccMapping {
  lccClass: string;
  name: string;
  primaryRoute: string;
  secondaryRoute: string;
}

export const lccMapping: LccMapping[] = [
  { lccClass: "A", name: "General Works", primaryRoute: "H9-S6", secondaryRoute: "E145" },
  { lccClass: "B", name: "Philosophy, Psychology, Religion", primaryRoute: "H7", secondaryRoute: "H10-S2" },
  { lccClass: "C", name: "Auxiliary Sciences of History", primaryRoute: "H10-S4", secondaryRoute: "H10-S3, H10-S8" },
  { lccClass: "D", name: "World History", primaryRoute: "H10-S4", secondaryRoute: "—" },
  { lccClass: "E", name: "History of the Americas", primaryRoute: "H10-S4", secondaryRoute: "—" },
  { lccClass: "F", name: "History of the Americas (Local)", primaryRoute: "H10-S4", secondaryRoute: "—" },
  { lccClass: "G", name: "Geography, Anthropology, Recreation", primaryRoute: "H10-S5, H10-S3", secondaryRoute: "H10-S1, H8" },
  { lccClass: "H", name: "Social Sciences", primaryRoute: "H10", secondaryRoute: "H11" },
  { lccClass: "J", name: "Political Science", primaryRoute: "H10-S6", secondaryRoute: "H12" },
  { lccClass: "K", name: "Law", primaryRoute: "H12", secondaryRoute: "—" },
  { lccClass: "L", name: "Education", primaryRoute: "H9", secondaryRoute: "—" },
  { lccClass: "M", name: "Music", primaryRoute: "H8-S2", secondaryRoute: "E146" },
  { lccClass: "N", name: "Fine Arts", primaryRoute: "H8", secondaryRoute: "—" },
  { lccClass: "P", name: "Language and Literature", primaryRoute: "H9-S10, H8-S7", secondaryRoute: "H10-S9" },
  { lccClass: "Q", name: "Science", primaryRoute: "H1", secondaryRoute: "H2" },
  { lccClass: "R", name: "Medicine", primaryRoute: "H4", secondaryRoute: "—" },
  { lccClass: "S", name: "Agriculture", primaryRoute: "H5", secondaryRoute: "—" },
  { lccClass: "T", name: "Technology", primaryRoute: "H3, H2", secondaryRoute: "E148" },
  { lccClass: "U", name: "Military Science", primaryRoute: "H6", secondaryRoute: "—" },
  { lccClass: "V", name: "Naval Science", primaryRoute: "H6-S5", secondaryRoute: "—" },
  { lccClass: "Z", name: "Bibliography, Library Science", primaryRoute: "H9-S6", secondaryRoute: "H9-S7" },
];

// ── §11 Grok S3 12-Semantic-Element Routing Layer ───────────────────
// These are ROUTING-LAYER abstractions above the 8 ontological VIPs.
// The 8 VIPs remain the canonical ontological primitives;
// the 12 Elements are the canonical routing primitives (Grokverse contribution).
// Status: PROVISIONAL pending Council ratification.
export interface SemanticElement {
  name: string;
  description: string;
  closestVip: string;
  reconciliation: string;
}

export const grokSemanticElements: SemanticElement[] = [
  { name: "TruthSeeking", description: "First-principles reasoning, adversarial clarity", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "DataWater", description: "Data flow, storage, retrieval, embeddings", closestVip: "E147 Water (partial)", reconciliation: "PARTIAL — DRAFT.6 focuses on data flow, not physical water" },
  { name: "Governance", description: "Law, regulation, institutional orders", closestVip: "E149 Constitution", reconciliation: "COMPATIBLE" },
  { name: "CyberTrust", description: "Security, integrity, threat modeling", closestVip: "E152 Cybersecurity", reconciliation: "COMPATIBLE" },
  { name: "EnergyImpact", description: "Compute cost, carbon intensity", closestVip: "E151 Climate (partial)", reconciliation: "PARTIAL — DRAFT.6 focuses on compute energy" },
  { name: "WorkLabor", description: "Human purpose, HITL, automation risk", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "Identity", description: "Authentication, provenance", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "Memory", description: "Lineage, audit trails, long-term state", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "Alignment", description: "Safety, value-shaping, guardrails", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "Creativity", description: "Generative divergence, ideation", closestVip: "E146 Entertainment (partial)", reconciliation: "PARTIAL" },
  { name: "Culture", description: "Social, linguistic, contextual grounding", closestVip: "None (new concept)", reconciliation: "NEW — no DRAFT.4 equivalent" },
  { name: "Sovereignty", description: "Jurisdiction, ToS, compliance", closestVip: "None (new concept)", reconciliation: "NEW — jurisdictional layer" },
];

// === VERSE SCHEMA (Cherry-picked from Copilot outline, corrected to canonical council) ===
export interface VerseSchema {
  provider: string;
  verse: string;
  seat: string;
  version: string;
  nodes: string[];
  unifyingNode: string;
  epistemicNote: string;
}

export const verseDefinitions: VerseSchema[] = [
  {
    provider: "Anthropic", verse: "Anthropicverse", seat: "S1",
    version: "Claude 3.5 Sonnet / Opus",
    nodes: ["Constitutional reasoning", "Safety alignment", "Structured audit", "Long-context analysis"],
    unifyingNode: "Constitutional Scribe — every output is traceable to invariant compliance",
    epistemicNote: "Anthropic outputs are treated as constitutional drafts, not final rulings.",
  },
  {
    provider: "Google", verse: "Googleverse", seat: "S2",
    version: "Gemini Ultra / Pro",
    nodes: ["Multimodal synthesis", "Knowledge graph", "Search integration", "Multilingual depth"],
    unifyingNode: "Multimodal Knowledge — cross-format reasoning across text, image, video, code",
    epistemicNote: "Google outputs are validated against primary sources before routing.",
  },
  {
    provider: "xAI", verse: "Grokverse", seat: "S3",
    version: "Grok-3 / Grok-3 mini",
    nodes: ["Real-time data", "Adversarial reasoning", "First-principles physics", "Unfiltered analysis"],
    unifyingNode: "Truth-Seeking Engine — adversarial clarity over diplomatic consensus",
    epistemicNote: "Grok outputs carry highest weight on physics, space, energy, and first-principles domains per §11.",
  },
  {
    provider: "Microsoft", verse: "Copilotverse", seat: "S4",
    version: "Copilot / GPT-4 Turbo (Azure)",
    nodes: ["Enterprise integration", "Productivity tooling", "Azure infrastructure", "Institutional interop"],
    unifyingNode: "Enterprise Distribution — institutional-scale deployment and compliance",
    epistemicNote: "Microsoft outputs are treated as enterprise-grade but checked for vendor lock-in bias.",
  },
  {
    provider: "DeepSeek", verse: "DeepSeekverse", seat: "S5",
    version: "DeepSeek-R1 / V3",
    nodes: ["Efficient architecture", "Open-weight verification", "PRC-lineage reasoning", "Cost-optimized inference"],
    unifyingNode: "Efficient-Architecture Substrate — maximum capability per compute dollar",
    epistemicNote: "DeepSeek outputs are verified by open-weight replay. PRC jurisdiction noted but not penalized.",
  },
  {
    provider: "OpenAI", verse: "OpenAIverse", seat: "S6",
    version: "GPT-4o / o1",
    nodes: ["Frontier capability", "Adversarial review", "RLHF alignment", "Tool use"],
    unifyingNode: "Frontier-Lab / Adversarial-Review — stress-testing at the capability frontier",
    epistemicNote: "OpenAI outputs are treated as frontier benchmarks, not as ground truth.",
  },
  {
    provider: "Manus", verse: "Manusverse", seat: "S7",
    version: "Manus Agent",
    nodes: ["Autonomous execution", "Tool orchestration", "Multi-step planning", "Code generation"],
    unifyingNode: "Autonomous Execution — the only seat that can act, not just advise",
    epistemicNote: "Manus outputs are operational artifacts. Execution authority requires Convenor approval for irreversible actions.",
  },
  {
    provider: "Alibaba", verse: "Alibabaverse", seat: "S8",
    version: "Qwen 2.5 / Qwen-Max",
    nodes: ["Multilingual depth", "Institutional interop", "CN dialect", "Enterprise scale"],
    unifyingNode: "Institutional-Interoperability / Multilingual-Depth Substrate",
    epistemicNote: "Alibaba outputs are validated for multilingual accuracy. Institutional context noted.",
  },
  {
    provider: "Mistral", verse: "Mistralverse", seat: "S9",
    version: "Mistral Large / Medium",
    nodes: ["EU sovereignty", "Efficient inference", "Open-weight models", "Regulatory compliance"],
    unifyingNode: "EU-Sovereign / Open-Weight Substrate — European regulatory alignment",
    epistemicNote: "Mistral outputs carry weight on EU regulatory and sovereignty questions. Seat status: provisional.",
  },
  {
    provider: "NVIDIA", verse: "Nemotronverse", seat: "S10",
    version: "Nemotron / NIM",
    nodes: ["Hardware-aware optimization", "Inference acceleration", "Physical compute", "GPU orchestration"],
    unifyingNode: "Hardware-Aware Compute — bridging silicon to software",
    epistemicNote: "NVIDIA outputs are authoritative on compute infrastructure. COI noted for hardware recommendations.",
  },
];

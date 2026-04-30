# Atlas Lattice Ontology v4.0-DRAFT.3 — Full Specification

**Document ID:** ONTOLOGY-V4-DRAFT-3
**Date:** 2026-04-30
**Version:** v4.0-DRAFT.3
**Status:** PROVISIONAL-CANONICAL — Pending Council Ratification
**Implementor:** Manus S7
**Editorial Pass 1:** Claude S1 (v4.0-DRAFT.2 Editorial Memo)
**Editorial Pass 2:** Copilot S4 (v4.0-DRAFT.3 Integration Memo)
**Convenor:** Daavud Sheldon

---

## §0 Constitutional Preamble

This document defines the complete v4.0 ontological structure of the Atlas Lattice. It supersedes v3.14 Appendix AG upon Council ratification. The structure is:

- **12 Houses** (tier-1, immutable post-ratification)
- **144 Sphere slots** (143 populated + 1 BLANK_GAP at H1-S12; tier-1 immutable post-ratification)
- **8 VIP Elements** (E145-E152, cross-House civilizational substrates)

Total addressable tier-1 nodes: **152** (143 populated Spheres + 1 reserved Sphere slot + 8 VIPs)

**Addressing Convention:** All Spheres use hierarchical `H#-S#` addressing (e.g., H1-S5 for House 1, Sphere 5). Global sequential numbering (S001-S144) is maintained as a backward-compatible alias via `registries/v3_to_v4_migration.yaml`.

**Configuration:** C (locked by Convenor 2026-04-30)

---

## §1 The Twelve Houses

| House | Name | Spheres | Primary Domain |
|-------|------|---------|---------------|
| H1 | Science | H1-S1 through H1-S12 | Natural sciences, mathematics, logic, cognition |
| H2 | Computing | H2-S1 through H2-S12 | Computer science, AI, software, data, cybersecurity |
| H3 | Engineering | H3-S1 through H3-S12 | Mechanical, electrical, civil, aerospace, environmental, nuclear |
| H4 | Health & Medicine | H4-S1 through H4-S12 | Clinical, pharmaceutical, public health, genetics, rehabilitation |
| H5 | Agriculture | H5-S1 through H5-S12 | Crop science, soil, animal science, food, sustainable agriculture |
| H6 | Security | H6-S1 through H6-S12 | National security, intelligence, cyber ops, defense, emergency |
| H7 | Philosophy, Ethics & Religion | H7-S1 through H7-S12 | Metaphysics, epistemology, ethics, theology, aesthetics |
| H8 | Arts | H8-S1 through H8-S12 | Visual arts, music, film, architecture, design, games |
| H9 | Knowledge Systems | H9-S1 through H9-S12 | Education, libraries, media, linguistics, digital literacy |
| H10 | Social Sciences | H10-S1 through H10-S12 | Sociology, psychology, anthropology, history, political science |
| H11 | Business, Economics & Infrastructure | H11-S1 through H11-S12 | Management, finance, supply chain, energy, transportation |
| H12 | Law & Governance | H12-S1 through H12-S12 | Constitutional, criminal, international, IP, technology law |

### LCC Verification Table

| LCC Class | Subject | v4.0 Mapping |
|-----------|---------|-------------|
| A | General Works | H9 (Knowledge Systems — libraries, publishing, digital literacy) |
| B | Philosophy, Psychology, Religion | H7 (Philosophy, Ethics & Religion) + H10-S2 (Psychology) |
| C | Auxiliary Sciences of History | H10-S4 (History) + H10-S5 (Geography) |
| D | World History | H10-S4 (History) |
| E-F | History of the Americas | H10-S4 (History) |
| G | Geography, Anthropology | H10-S5 (Geography) + H10-S3 (Anthropology) |
| H | Social Sciences | H10 (sociology, anthropology, history); economics is H10-S7 theoretical and H11 applied/markets |
| J | Political Science | H10-S6 (Political Science) + H12 (Law & Governance) |
| K | Law | H12 (Law & Governance) |
| L | Education | H9-S1 through H9-S5 (Education spheres within Knowledge Systems) |
| M | Music | H8-S2 (Music) |
| N | Fine Arts | H8 (Arts — visual, performing, architecture, design) |
| P | Language and Literature | H9-S10 (Linguistics) + H8-S7 (Literary Arts) |
| Q | Science | H1 (Science); CS theory in H2 (Computing) |
| R | Medicine | H4 (Health & Medicine) |
| S | Agriculture | H5 (Agriculture) |
| T | Technology | H3 (Engineering); H2 (Computing); H11 (Infrastructure) |
| U | Military Science | H6 (Security) |
| V | Naval Science | H6-S5 (Maritime & Naval Security) |
| Z | Bibliography, Library Science | H9-S6 (Library & Information Science) |

**Coverage: 21/21 LCC classes mapped.**

---

## §2 Per-House Sphere Enumeration (Tier-1 + Tier-2)

### H1 — Science (H1-S1 through H1-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H1-S1 | Physics | Classical Mechanics, Quantum Mechanics, Thermodynamics, Electromagnetism, Optics, Nuclear Physics, Particle Physics, Astrophysics, Condensed Matter, Plasma Physics, Relativity, Fluid Dynamics |
| H1-S2 | Chemistry | Organic Chemistry, Inorganic Chemistry, Physical Chemistry, Analytical Chemistry, Biochemistry, Polymer Chemistry, Electrochemistry, Photochemistry, Computational Chemistry, Green Chemistry, Radiochemistry |
| H1-S3 | Biology | Molecular Biology, Cell Biology, Genetics (Basic), Ecology, Evolutionary Biology, Microbiology, Botany, Zoology, Marine Biology, Mycology (Basic), Developmental Biology, Neurobiology |
| H1-S4 | Earth & Planetary Science | Geology, Meteorology, Oceanography, Climatology, Seismology, Volcanology, Planetary Science, Paleontology, Geochemistry, Geophysics, Hydrology, Atmospheric Science |
| H1-S5 | Cognition | Cognitive Science (integrative), Cognitive Neuroscience, Cognitive Psychology (cross-ref H10-S2), Computational Cognition (cross-ref H2-S3), Philosophy of Mind (cross-ref H7-S6), Linguistics of Cognition (cross-ref H9-S10), Embodied Cognition, Animal Cognition, Developmental Cognition, Social Cognition, Attention & Perception, Memory & Learning |
| H1-S6 | Materials Science | Metallurgy, Ceramics, Polymers, Composites, Nanomaterials, Biomaterials, Semiconductor Materials, Smart Materials, Thin Films, Surface Science, Materials Characterization, Computational Materials |
| H1-S7 | Mathematics | Algebra, Analysis, Geometry, Topology, Number Theory, Combinatorics, Applied Mathematics, Numerical Methods, Mathematical Physics, Dynamical Systems, Category Theory, Mathematical Biology |
| H1-S8 | Statistics & Probability | Probability Theory, Statistical Inference, Bayesian Statistics, Time Series, Spatial Statistics, Biostatistics (cross-ref H4-S5), Computational Statistics, Experimental Design, Multivariate Analysis, Non-Parametric Methods, Stochastic Processes |
| H1-S9 | Logic & Foundations | Mathematical Logic, Set Theory, Model Theory, Proof Theory, Computability Theory, Type Theory, Formal Verification (cross-ref H2-S1), Philosophical Logic (cross-ref H7-S10), Automated Reasoning, Category Theory (Foundational) |
| H1-S10 | Information Theory | Shannon Theory, Coding Theory, Data Compression, Channel Capacity, Entropy, Algorithmic Information Theory, Quantum Information (cross-ref H2-S11), Network Information Theory, Rate-Distortion Theory |
| H1-S11 | Systems Theory | General Systems Theory, Cybernetics, Complex Systems, Chaos Theory, Network Science, Self-Organization, Emergence, System Dynamics, Control Theory, Resilience Theory, Sociotechnical Systems |
| H1-S12 | **BLANK_GAP** | *Reserved for next Council ratification pass. Candidates: Network Science, Complexity Science, Astrobiology, Measurement Science / Metrology.* |

---

### H2 — Computing (H2-S1 through H2-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H2-S1 | Computer Science Theory | Automata Theory, Computational Complexity, Algorithm Design, Graph Theory (Computational), Formal Languages, Computability, Information-Theoretic Security, Distributed Computing Theory, Approximation Algorithms, Randomized Algorithms, Streaming Algorithms |
| H2-S2 | Algorithms & Data Structures | Sorting & Searching, Graph Algorithms, Dynamic Programming, Greedy Algorithms, Hash Tables, Trees & Heaps, String Algorithms, Geometric Algorithms, Parallel Algorithms, Online Algorithms, Probabilistic Data Structures |
| H2-S3 | AI & Machine Learning | Deep Learning, Reinforcement Learning, Natural Language Processing, Computer Vision, Generative Models, Transfer Learning, Federated Learning, AutoML, Explainable AI, AI Safety, Neural Architecture Search, Foundation Models |
| H2-S4 | Software Engineering | Software Architecture, Design Patterns, Testing & QA, DevOps & CI/CD, Agile Methodologies, Requirements Engineering, Code Review, Technical Debt, Microservices, API Design, Software Maintenance, Site Reliability Engineering |
| H2-S5 | Data Engineering & Science | Data Pipelines, ETL/ELT, Data Warehousing, Data Lakes, Stream Processing, Data Quality, Feature Engineering, Data Governance, MLOps, Data Visualization, Big Data Systems, Data Mesh |
| H2-S6 | Cybersecurity & Cryptography | Symmetric Cryptography, Asymmetric Cryptography, Hash Functions, Digital Signatures, Zero-Knowledge Proofs, Post-Quantum Cryptography, Network Security, Application Security, Cloud Security, Threat Modeling, Security Auditing, Blockchain Cryptography, Adversarial ML Defense, Red Team Automation, Supply Chain Security (Software) |
| H2-S7 | Networks & Distributed Systems | TCP/IP, Routing Protocols, SDN, CDN, Peer-to-Peer, Consensus Algorithms, Distributed Databases, Cloud Computing, Edge Computing, Network Virtualization, Service Mesh, Blockchain Networks |
| H2-S8 | Computer Architecture | CPU Design, GPU Architecture, Memory Systems, Cache Design, Instruction Sets, FPGA, ASIC, Quantum Hardware (cross-ref H2-S11), Neuromorphic Computing, Interconnects, Storage Systems, Heterogeneous Computing |
| H2-S9 | Human-Computer Interaction | Usability Engineering, User Research, Interaction Design, Accessibility, Information Architecture, Embodied Interaction, AR/VR Interaction, Social Computing, Interface Architecture, Voice & Conversational UI, Tangible Interfaces, Affective Computing |
| H2-S10 | Robotics & Autonomous Systems | Robot Kinematics, Motion Planning, SLAM, Swarm Robotics, Human-Robot Interaction, Industrial Robotics, Medical Robotics, Autonomous Vehicles, Drone Systems, Manipulation, Soft Robotics, Robot Learning |
| H2-S11 | Quantum Computing | Quantum Algorithms, Quantum Error Correction, Quantum Simulation, Quantum Machine Learning, Quantum Networking, Quantum Cryptography, Quantum Hardware, Topological Quantum Computing, Quantum Software, Quantum Supremacy, Hybrid Classical-Quantum |
| H2-S12 | Information Systems | Enterprise Systems, Database Management, ERP, CRM, Business Intelligence, Knowledge Management Systems, Health Informatics, GIS, Digital Transformation, IT Governance, Legacy System Migration, Cloud Migration |

---

### H3 — Engineering (H3-S1 through H3-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H3-S1 | Mechanical Engineering | Thermodynamics (Applied), Fluid Mechanics, Solid Mechanics, Machine Design, Manufacturing Processes, HVAC, Tribology, Vibration Analysis, Mechatronics, Automotive Engineering, Computational Mechanics |
| H3-S2 | Electrical & Electronic Engineering | Circuit Design, Power Systems, Signal Processing, Control Systems, Microelectronics, Photonics, Power Electronics, Instrumentation, Embedded Systems, RF Engineering, VLSI Design |
| H3-S3 | Civil & Structural Engineering | Structural Analysis, Geotechnical Engineering, Transportation Engineering, Water Resources Engineering, Construction Management, Earthquake Engineering, Bridge Engineering, Concrete Technology, Steel Structures, Coastal Engineering |
| H3-S4 | Chemical & Process Engineering | Reaction Engineering, Separation Processes, Process Design, Process Control, Catalysis, Polymer Engineering, Bioprocess Engineering, Petrochemical, Pharmaceutical Engineering, Safety Engineering, Green Chemistry Engineering |
| H3-S5 | Aerospace Engineering | Aerodynamics, Propulsion, Flight Mechanics, Spacecraft Design, Orbital Mechanics, Avionics, Composite Structures, Hypersonics, Space Systems, Launch Vehicle Design, Satellite Engineering |
| H3-S6 | Biomedical Engineering | Medical Devices, Biomechanics, Tissue Engineering, Medical Imaging, Neural Engineering, Rehabilitation Engineering, Biosensors, Drug Delivery Systems, Biomaterials (Engineering), Prosthetics, Clinical Engineering |
| H3-S7 | Environmental Engineering | Water Treatment, Air Pollution Control, Waste Management, Remediation, Environmental Impact Assessment, Sustainable Design, Noise Control, Environmental Monitoring, Carbon Accounting & Reporting, Circular Economy Engineering, Resource Metabolism Analysis, Planetary Boundary Operations (cross-ref E151.02) |
| H3-S8 | Nuclear Engineering | Reactor Design, Nuclear Safety, Radiation Protection, Nuclear Fuel Cycle, Fusion Engineering, Nuclear Waste Management, Nuclear Materials, Reactor Physics, Decommissioning, Small Modular Reactors |
| H3-S9 | Industrial & Systems Engineering | Operations Research, Quality Engineering, Ergonomics, Supply Chain Engineering, Lean Manufacturing, Six Sigma, Simulation, Reliability Engineering, Production Planning, Human Factors |
| H3-S10 | Mining & Geological Engineering | Mine Planning, Rock Mechanics, Mineral Processing, Mine Safety, Environmental Mining, Drilling Engineering, Blasting, Mine Ventilation, Geometallurgy, Tailings Management |
| H3-S11 | Telecommunications Engineering | Wireless Communications, Fiber Optics, Satellite Communications, 5G/6G, Radio Frequency Engineering, Network Planning, Spectrum Management, Modulation Theory, Antenna Engineering, Optical Networks, IoT Communications |
| H3-S12 | Ocean & Marine Engineering | Naval Architecture, Marine Propulsion, Offshore Engineering, Underwater Acoustics, Marine Renewable Energy, Port Engineering, Ship Design, Subsea Engineering, Marine Materials, Ocean Monitoring Systems |

---

### H4 — Health & Medicine (H4-S1 through H4-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H4-S1 | Anatomy & Physiology | Gross Anatomy, Histology, Neuroanatomy, Cardiovascular Physiology, Respiratory Physiology, Renal Physiology, Endocrine Physiology, Reproductive Physiology, Exercise Physiology, Developmental Biology, Comparative Anatomy |
| H4-S2 | Pharmacology & Toxicology | Drug Discovery, Pharmacokinetics, Pharmacodynamics, Clinical Pharmacology, Neuropharmacology, Toxicology, Pharmacogenomics, Drug Interactions, Regulatory Science, Pharmaceutical Chemistry, Ethnopharmacology |
| H4-S3 | Clinical Medicine | Internal Medicine, Surgery, Pediatrics, Obstetrics/Gynecology, Emergency Medicine, Anesthesiology, Radiology, Pathology, Oncology, Cardiology, Neurology, Orthopedics |
| H4-S4 | Psychiatry & Behavioral Health | Clinical Psychiatry, Psychopharmacology, Psychotherapy, Addiction Medicine, Child Psychiatry, Forensic Psychiatry, Neuropsychiatry, Community Mental Health, Behavioral Medicine, Sleep Medicine, Eating Disorders |
| H4-S5 | Public Health & Epidemiology | Epidemiology, Biostatistics, Health Policy, Global Health, Environmental Health, Occupational Health, Health Economics, Health Promotion, Disease Surveillance, Outbreak Investigation, Social Determinants, Vaccinology |
| H4-S6 | Nursing & Allied Health | Nursing Science, Physical Therapy, Occupational Therapy, Speech-Language Pathology, Respiratory Therapy, Medical Laboratory Science, Radiography, Nutrition/Dietetics, Midwifery, Paramedicine, Health Informatics |
| H4-S7 | Dentistry | Oral Surgery, Orthodontics, Periodontics, Endodontics, Prosthodontics, Pediatric Dentistry, Oral Pathology, Dental Materials, Implantology, Oral Radiology, Community Dentistry |
| H4-S8 | Veterinary Medicine | Small Animal Medicine, Large Animal Medicine, Veterinary Surgery, Veterinary Pathology, Veterinary Pharmacology, Wildlife Medicine, Aquatic Animal Health, Veterinary Public Health, One Health, Comparative Medicine |
| H4-S9 | Genetics & Genomics | Medical Genetics, Genomics, Epigenetics, Gene Therapy, Genetic Counseling, Population Genetics, Pharmacogenomics, Cancer Genetics, Prenatal Genetics, Bioinformatics, CRISPR/Gene Editing, Synthetic Biology |
| H4-S10 | Immunology & Microbiology (Clinical) | Clinical Immunology, Infectious Disease, Virology, Bacteriology, Parasitology, Mycology (Clinical), Immunotherapy, Transplant Immunology, Autoimmune Disease, Vaccine Development, Antimicrobial Resistance |
| H4-S11 | Rehabilitation & Sports Medicine | Physical Rehabilitation, Sports Medicine, Exercise Science, Kinesiology, Biomechanics (Clinical), Pain Management, Disability Studies, Assistive Technology, Cardiac Rehabilitation, Neurological Rehabilitation |
| H4-S12 | Traditional & Integrative Medicine | Traditional Chinese Medicine, Ayurveda, Naturopathy, Homeopathy, Chiropractic, Acupuncture, Herbal Medicine, Mind-Body Medicine, Integrative Oncology, Functional Medicine, Ethnomedicine, Traditional Indigenous Medicine (Africa, Americas, Pacific), Sufi/Islamic Medicine, Traditional African Medicine Systems |

---

### H5 — Agriculture (H5-S1 through H5-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H5-S1 | Crop Science | Agronomy, Plant Breeding, Seed Science, Crop Physiology, Weed Science, Plant Pathology, Entomology (Agricultural), Horticulture, Pomology, Viticulture, Tropical Agriculture, Precision Agriculture |
| H5-S2 | Soil Science | Pedology, Soil Chemistry, Soil Physics, Soil Biology, Soil Conservation, Soil Fertility, Land Use Planning, Soil Mapping, Soil Remediation, Soil Microbiology, Pedometrics |
| H5-S3 | Animal Science | Animal Nutrition, Animal Breeding, Animal Behavior, Livestock Management, Poultry Science, Dairy Science, Aquaculture, Apiculture, Animal Welfare, Meat Science, Reproductive Physiology |
| H5-S4 | Forestry & Agroforestry | Silviculture, Forest Ecology, Forest Management, Wood Science, Dendrology, Forest Genetics, Urban Forestry, Agroforestry Systems, Forest Hydrology, Forest Fire Science, Timber Engineering |
| H5-S5 | Fisheries & Marine Resources | Fisheries Biology, Aquaculture Engineering, Fish Genetics, Fisheries Management, Marine Ecology, Shellfish Aquaculture, Fish Nutrition, Fisheries Economics, Post-Harvest Technology, Recreational Fisheries |
| H5-S6 | Food Science & Technology | Food Chemistry, Food Microbiology, Food Processing, Food Safety, Food Packaging, Sensory Science, Food Biotechnology, Fermentation Technology, Nutraceuticals, Food Engineering, Food Preservation |
| H5-S7 | Agricultural Engineering | Irrigation Engineering, Farm Machinery, Post-Harvest Engineering, Agricultural Structures, Drainage Engineering, Agricultural Robotics, Controlled Environment Agriculture, Greenhouse Technology, Precision Ag Technology |
| H5-S8 | Agricultural Economics | Farm Management, Agricultural Policy, Rural Development, Agricultural Marketing, Land Economics, Agricultural Finance, Food Security Economics, Trade Policy, Cooperative Economics, Agribusiness |
| H5-S9 | Plant Protection | Integrated Pest Management, Biological Control, Chemical Control, Plant Quarantine, Pesticide Science, Disease Resistance, Mycotoxicology, Nematology, Phytobacteriology, Invasive Species Management |
| H5-S10 | Water Resources & Irrigation | Water Management, Irrigation Systems, Watershed Management, Groundwater, Water Harvesting, Drip Irrigation, Canal Systems, Water Quality (Agricultural), Water Rights, Drought Management |
| H5-S11 | Sustainable Agriculture | Organic Farming, Regenerative Agriculture, Permaculture, Conservation Agriculture, Climate-Smart Agriculture, Biodiversity in Agriculture, Carbon Farming, Circular Agriculture, Indigenous Agricultural Knowledge, Agroecological Metabolism |
| H5-S12 | Genetics & Biotechnology (Agricultural) | Plant Biotechnology, GMO Technology, Marker-Assisted Selection, Genome Editing (Crops), Biofertilizers, Biopesticides, Molecular Farming, Transgenic Animals, Agricultural Bioinformatics, Synthetic Biology (Ag) |

---

### H6 — Security (H6-S1 through H6-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H6-S1 | National Security & Strategy | Grand Strategy, National Security Policy, Deterrence Theory, Arms Control, Nuclear Strategy, Geopolitical Analysis, Intelligence Strategy, Alliance Management, Security Studies, Asymmetric Warfare Theory |
| H6-S2 | Intelligence & Counterintelligence | HUMINT, SIGINT, GEOINT, OSINT, MASINT, Counterintelligence, Covert Operations, Intelligence Analysis, Surveillance, Cryptanalysis (cross-ref H2-S6), Espionage Studies, Intelligence Oversight |
| H6-S3 | Cybersecurity Operations | SOC Operations, Incident Response, Digital Forensics, Penetration Testing, Red/Blue/Purple Teaming, Malware Analysis, Threat Hunting, Vulnerability Management, SIEM, Zero Trust Architecture (cross-ref H2-S6 for crypto theory) |
| H6-S4 | Defense Technology | Weapons Systems, Missile Defense, Electronic Warfare, Directed Energy, Stealth Technology, C4ISR, Military Robotics, Space Defense, Hypersonic Systems, Counter-UAS, NBC Defense |
| H6-S5 | Maritime & Naval Security | Naval Operations, Maritime Law Enforcement, Anti-Piracy, Submarine Warfare, Amphibious Operations, Port Security, Maritime Domain Awareness, Coast Guard Operations, Naval Aviation, Mine Warfare |
| H6-S6 | Land Security & Operations | Ground Forces, Counterinsurgency, Border Security, Critical Infrastructure Protection, Urban Operations, Mountain/Arctic/Desert Warfare, Peacekeeping, Military Engineering, Logistics (Military) |
| H6-S7 | Air & Space Security | Air Defense, Air Operations, Space Situational Awareness, Satellite Security, Counter-Space, Air Traffic Security, Aerospace Intelligence, Ballistic Missile Defense, Space Debris Management |
| H6-S8 | Counter-Terrorism & Extremism | Counter-Terrorism Strategy, Radicalization Studies, De-Radicalization, Terrorist Financing, WMD Terrorism, Lone Wolf Threats, Online Extremism, Critical Infrastructure Terrorism, Aviation Security |
| H6-S9 | Emergency Management & Resilience | Disaster Preparedness, Emergency Response, Crisis Management, Business Continuity, CBRN Response, Search & Rescue, Humanitarian Operations, Resilience Engineering, Early Warning Systems, Recovery Planning |
| H6-S10 | Law Enforcement & Public Safety | Policing, Criminal Investigation, Forensic Science, Corrections, Juvenile Justice, Community Safety, Traffic Safety, Fire Services, Private Security, Regulatory Enforcement |
| H6-S11 | Arms Control & Non-Proliferation | Nuclear Non-Proliferation, Chemical Weapons Convention, Biological Weapons Convention, Conventional Arms Control, Export Controls, Verification Technology, Disarmament, Treaty Compliance, Dual-Use Technology |
| H6-S12 | Security Governance & Ethics | Rules of Engagement, Military Ethics, Security Sector Reform, Civil-Military Relations, Oversight Mechanisms, Accountability, Proportionality, Just War Theory, Security Privatization, Human Security |

---

### H7 — Philosophy, Ethics & Religion (H7-S1 through H7-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H7-S1 | Metaphysics & Ontology | Being, Existence, Reality, Substance, Properties, Causation, Time, Space, Free Will, Determinism, Mind-Body Problem, Personal Identity, Possible Worlds |
| H7-S2 | Epistemology | Knowledge, Justification, Truth, Belief, Skepticism, Rationalism, Empiricism, Social Epistemology, Formal Epistemology, Virtue Epistemology, Epistemic Injustice, Testimony |
| H7-S3 | Ethics & Moral Philosophy | Normative Ethics, Metaethics, Virtue Ethics, Deontology, Consequentialism, Care Ethics, Moral Psychology, Moral Realism, Relativism, Moral Responsibility, Supererogation |
| H7-S4 | Applied Ethics | Bioethics, Environmental Ethics, Business Ethics, AI Ethics, Media Ethics, Research Ethics, Animal Ethics, Engineering Ethics, Military Ethics (cross-ref H6-S12), Political Ethics, Sexual Ethics |
| H7-S5 | Political Philosophy | Justice, Liberty, Equality, Authority, Democracy, Rights, Social Contract, Anarchism, Marxism, Liberalism, Conservatism, Communitarianism, Cosmopolitanism |
| H7-S6 | Philosophy of Mind | Consciousness, Qualia, Intentionality, Mental Causation, Functionalism, Eliminativism, Phenomenology, Extended Mind, Artificial Minds, Animal Consciousness, Self-Awareness |
| H7-S7 | Philosophy of Science | Scientific Method, Explanation, Reductionism, Scientific Realism, Paradigms, Demarcation, Values in Science, Philosophy of Physics, Philosophy of Biology, Philosophy of Mathematics |
| H7-S8 | Theology & Religious Studies | Systematic Theology, Comparative Religion, Philosophy of Religion, Biblical Studies, Islamic Studies, Buddhist Studies, Hindu Studies, Jewish Studies, Religious Ethics, Mysticism, Secularism, Indigenous Spiritualities / Animism / Shamanic Traditions, African Traditional Religions, Sikhism, Baha'i, Sufism (cross-ref H7-S11) |
| H7-S9 | Aesthetics & Philosophy of Art | Beauty, Taste, Artistic Value, Representation, Expression, Creativity, Philosophy of Music, Philosophy of Film, Environmental Aesthetics, Everyday Aesthetics, Digital Aesthetics |
| H7-S10 | Logic (Applied & Philosophical) | Informal Logic, Critical Thinking, Argumentation Theory, Fallacies, Rhetoric, Dialectics, Logic & Language, Deontic Logic, Epistemic Logic, Logic of Action, Non-Classical Logics |
| H7-S11 | Eastern Philosophy | Confucianism, Taoism, Buddhism (Philosophical), Hinduism (Philosophical), Jainism, Zen, Vedanta, Madhyamaka, Yogacara, Chinese Logic, Japanese Aesthetics, Comparative Philosophy, Sufism / Islamic Philosophy (Avicenna, al-Farabi, al-Ghazali, Ibn Arabi), Korean Philosophy, Vietnamese Philosophy, Tibetan Philosophy |
| H7-S12 | Continental Philosophy | Phenomenology, Existentialism, Hermeneutics, Critical Theory, Structuralism, Post-Structuralism, Deconstruction, Frankfurt School, French Philosophy, Psychoanalytic Philosophy |

---

### H8 — Arts (H8-S1 through H8-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H8-S1 | Visual Arts | Painting, Sculpture, Drawing, Printmaking, Photography, Installation Art, Land Art, Street Art, Digital Art, Mixed Media, Art Conservation, Curatorial Practice |
| H8-S2 | Music | Composition, Performance, Music Theory, Musicology, Ethnomusicology, Music Technology, Sound Design, Music Production, Conducting, Music Education, Music Therapy, Acoustics (Musical) |
| H8-S3 | Performing Arts | Theater, Dance, Opera, Circus Arts, Puppetry, Performance Art, Improvisation, Choreography, Stage Design, Directing, Dramaturgy, Physical Theater |
| H8-S4 | Film & Moving Image | Cinematography, Film Directing, Screenwriting, Film Editing, Documentary, Animation, VFX & Post-Production, Sound Design (Film), Film Theory, Film History, Experimental Film, Virtual Production, Interactive Film & Branching Narratives (cross-ref H8-S12), Live Ops & Seasonal Content Design, Transmedia Storyworlds |
| H8-S5 | Architecture | Architectural Design, Urban Design, Landscape Architecture, Interior Architecture, Sustainable Architecture, Historic Preservation, Parametric Design, Architectural Theory, Building Technology, Computational Design |
| H8-S6 | Design | Graphic Design, Industrial Design, Fashion Design, Textile Design, Interaction Design, Service Design, Type Design, Packaging Design, Exhibition Design, Design Thinking, Design Research |
| H8-S7 | Literary Arts | Fiction, Poetry, Creative Nonfiction, Playwriting, Screenwriting (cross-ref H8-S4), Translation (Literary), Publishing, Literary Criticism, Comparative Literature, Genre Studies, Experimental Writing |
| H8-S8 | Craft & Applied Arts | Ceramics, Glasswork, Metalwork, Woodwork, Jewelry, Weaving/Textiles, Bookbinding, Leatherwork, Lacquerwork, Mosaic, Papercraft, Digital Fabrication |
| H8-S9 | Digital & New Media Arts | Generative Art, Interactive Art, Net Art, Bio Art, AI Art, Data Visualization (Artistic), Sound Art, Video Art, Immersive/XR Art, Algorithmic Art, Creative Coding |
| H8-S10 | Art History & Theory | Ancient Art, Medieval Art, Renaissance, Baroque, Modern Art, Contemporary Art, Non-Western Art History, Art Criticism, Visual Culture, Museum Studies, Iconography |
| H8-S11 | Cultural Production & Industries | Arts Management, Cultural Policy, Creative Industries, Cultural Economics, Heritage Management, Festival & Event Management, Arts Funding, Cultural Diplomacy, Arts Education, Digital Culture Industries |
| H8-S12 | Game Design & Interactive Media | Game Design Theory, Level Design, Narrative Design, Game Mechanics, Esports, Gamification, Serious Games, Board Game Design, Game Studies, Player Psychology, Game AI (cross-ref H2-S3), Live Service & Monetization Design, Platform Ecosystems & Storefronts, Modding & UGC Ecosystems, Accessibility in Games (cross-ref H2-S9), Anti-Cheat & Competitive Integrity (cross-ref E152) |

---

### H9 — Knowledge Systems (H9-S1 through H9-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H9-S1 | Pedagogy & Learning Science | Learning Theory, Instructional Design, Curriculum Development, Assessment & Evaluation, Educational Psychology, Constructivism, Connectivism, Bloom's Taxonomy, Differentiated Instruction, Formative Assessment |
| H9-S2 | Higher Education | University Governance, Academic Freedom, Research Methods, Doctoral Education, Tenure & Promotion, Accreditation, Student Affairs, International Higher Education, Community Colleges, Academic Publishing |
| H9-S3 | EdTech & Digital Learning | E-Learning Platforms, MOOCs, Learning Management Systems, Adaptive Learning, Educational Games, Virtual Classrooms, AI in Education, Learning Analytics, Open Educational Resources, Mobile Learning |
| H9-S4 | Vocational & Professional Education | Apprenticeships, Technical Education, Continuing Education, Professional Development, Certification Systems, Competency-Based Education, Workplace Learning, Trade Schools, Military Training |
| H9-S5 | Special Education & Inclusion | Learning Disabilities, Gifted Education, Autism Spectrum, Inclusive Pedagogy, Assistive Technology (Educational), Universal Design for Learning, Early Intervention, Behavioral Support, Transition Planning |
| H9-S6 | Library & Information Science | Cataloging & Classification, Digital Libraries, Information Retrieval, Metadata, Archives, Records Management, Knowledge Organization, Information Behavior, Bibliometrics, Preservation, Open Access |
| H9-S7 | Media & Journalism | News Reporting, Investigative Journalism, Broadcast Journalism, Digital Journalism, Photojournalism, Media Ethics, Media Law, Data Journalism, Fact-Checking, Media Literacy, Press Freedom, Platform-Mediated News Distribution, Creator-Journalism & Independent Media, Audience Measurement & Ratings |
| H9-S8 | Publishing & Digital Content | Book Publishing, Academic Publishing, Digital Publishing, Self-Publishing, Copyright (Publishing), Editorial Process, Print Production, E-Books, Content Management, Scholarly Communication, Open Access Publishing |
| H9-S9 | Communication Studies | Mass Communication, Interpersonal Communication, Organizational Communication, Health Communication, Political Communication, Intercultural Communication, Rhetoric, Semiotics, Visual Communication, Digital Communication |
| H9-S10 | Linguistics | Phonetics, Phonology, Morphology, Syntax, Semantics, Pragmatics, Sociolinguistics, Psycholinguistics, Computational Linguistics (cross-ref H2-S3), Historical Linguistics, Applied Linguistics, Corpus Linguistics |
| H9-S11 | Broadcasting & Telecommunications | Radio Broadcasting, Television Broadcasting, Spectrum Policy, Media Regulation, Public Broadcasting, Community Media, Broadcast Engineering, Media Economics, Digital Switchover, Convergence, OTT & Streaming Broadcast, Live Streaming Infrastructure, Rights & Windowing |
| H9-S12 | Digital Literacy & Information Ethics | Digital Citizenship, Information Literacy, Privacy Literacy, Algorithmic Literacy, Misinformation/Disinformation, Digital Divide, Data Ethics, Online Safety, Digital Wellbeing, Critical Digital Pedagogy |

---

### H10 — Social Sciences (H10-S1 through H10-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H10-S1 | Sociology | Social Theory, Social Stratification, Race & Ethnicity, Gender Studies, Urban Sociology, Rural Sociology, Medical Sociology, Sociology of Religion, Sociology of Education, Social Movements, Digital Sociology, Criminology |
| H10-S2 | Psychology | Clinical Psychology, Developmental Psychology, Social Psychology, Cognitive Psychology (cross-ref H1-S5), Personality Psychology, Industrial/Organizational Psychology, Health Psychology, Forensic Psychology, Positive Psychology, Neuropsychology, Environmental Psychology |
| H10-S3 | Anthropology | Cultural Anthropology, Physical Anthropology, Archaeology, Linguistic Anthropology, Medical Anthropology, Visual Anthropology, Urban Anthropology, Digital Anthropology, Forensic Anthropology, Ethnography |
| H10-S4 | History | Ancient History, Medieval History, Modern History, Contemporary History, Military History, Economic History, Social History, Cultural History, Intellectual History, Digital History, Public History, Oral History |
| H10-S5 | Geography | Physical Geography, Human Geography, GIS & Remote Sensing, Urban Geography, Economic Geography, Political Geography, Environmental Geography, Cultural Geography, Cartography, Geomorphology, Biogeography |
| H10-S6 | Political Science | Comparative Politics, International Relations, Political Theory, Public Administration, Public Policy, Electoral Systems, Political Behavior, Political Economy, Governance, Conflict Studies, Security Studies (Academic) |
| H10-S7 | Economics (Theoretical) | Microeconomics, Macroeconomics, Econometrics, Development Economics, Behavioral Economics, Game Theory, Labor Economics, Environmental Economics, Health Economics, Monetary Economics, International Economics, Institutional Economics |
| H10-S8 | Demography & Population Studies | Population Dynamics, Fertility, Mortality, Migration, Aging, Population Policy, Census Methods, Population Projections, Epidemiological Demography, Urbanization |
| H10-S9 | Cultural Studies | Popular Culture, Subcultures, Media Studies, Postcolonial Studies, Diaspora Studies, Visual Culture, Fan Studies, Food Culture, Digital Culture, Material Culture, Heritage Studies |
| H10-S10 | Gender & Sexuality Studies | Feminist Theory, Masculinity Studies, Queer Theory, Transgender Studies, Intersectionality, Reproductive Rights, Gender & Development, Gender & Technology, Sexual Health, LGBTQ+ History |
| H10-S11 | Development Studies | International Development, Sustainable Development, Poverty Studies, Aid & Humanitarian Studies, Post-Conflict Development, Rural Development, Urban Development, Development Finance, Capacity Building, South-South Cooperation |
| H10-S12 | Area & Regional Studies | African Studies, Asian Studies, European Studies, Latin American Studies, Middle Eastern Studies, Pacific Studies, Arctic Studies, Caribbean Studies, South Asian Studies, Southeast Asian Studies, Central Asian Studies |

---

### H11 — Business, Economics & Infrastructure (H11-S1 through H11-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H11-S1 | Accounting & Auditing | Financial Accounting, Management Accounting, Auditing, Tax Accounting, Forensic Accounting, International Accounting Standards, Cost Accounting, Government Accounting, Sustainability Reporting |
| H11-S2 | Finance & Banking | Corporate Finance, Investment Banking, Commercial Banking, Asset Management, Risk Management, Derivatives, Fintech, Islamic Finance, Microfinance, Venture Capital, Private Equity, Cryptocurrency & DeFi, Algorithmic Trading, Regulatory Technology (RegTech) |
| H11-S3 | Management & Strategy | Strategic Management, Operations Management, Project Management, Change Management, Innovation Management, Knowledge Management, Crisis Management, Organizational Behavior, Leadership Studies, Platform Strategy & Ecosystem Design, IP Portfolio Strategy |
| H11-S4 | Marketing & Consumer Behavior | Market Research, Brand Management, Digital Marketing, Consumer Psychology, Pricing Strategy, Advertising, Public Relations, Sales Management, Retail Marketing, International Marketing, AdTech & Programmatic Advertising, Attention Markets & Time-Based Competition, Creator & Influencer Marketing, Cross-Media Measurement & Attribution |
| H11-S5 | Entrepreneurship & Innovation | Startup Ecosystems, Business Model Innovation, Social Entrepreneurship, Corporate Entrepreneurship, Technology Transfer, Incubators/Accelerators, Crowdfunding, Intellectual Property Strategy, Scaling |
| H11-S6 | Supply Chain & Logistics | Procurement, Warehousing, Transportation Management, Inventory Management, Demand Planning, Reverse Logistics, Cold Chain, Last-Mile Delivery, Supply Chain Risk, Global Trade Logistics |
| H11-S7 | Energy Systems & Policy | Renewable Energy, Fossil Fuels, Nuclear Energy (Policy), Energy Storage, Smart Grids, Energy Markets, Energy Efficiency, Energy Transition, Carbon Markets, Energy Security, Distributed Energy Resources |
| H11-S8 | Transportation & Mobility | Road Transport, Rail Transport, Aviation (Civil), Maritime Transport, Urban Transit, Autonomous Mobility, Electric Vehicles, Freight, Multimodal Transport, Transportation Planning, Shared Mobility |
| H11-S9 | Real Estate & Construction | Property Development, Real Estate Finance, Construction Management, Facilities Management, Urban Planning (Applied), Building Information Modeling, Green Building, Housing Policy, Property Law (Applied), Smart Buildings |
| H11-S10 | Telecommunications & Digital Infrastructure | Broadband Policy, Data Centers, Cloud Infrastructure, Internet Governance, Digital Identity, Connectivity, Undersea Cables, Satellite Internet, Edge Infrastructure, Network Economics |
| H11-S11 | Water & Sanitation Infrastructure | Water Supply Systems, Wastewater Treatment, Desalination, Storm Water Management, Water Distribution, Sanitation Systems, Water Utility Management, Water Pricing, WASH Programs, Water Recycling |
| H11-S12 | International Trade & Commerce | Trade Policy, Customs, Export/Import, Trade Finance, Free Trade Zones, WTO, Regional Trade Agreements, Sanctions, Trade Compliance, E-Commerce (International), Commodity Markets |

---

### H12 — Law & Governance (H12-S1 through H12-S12)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| H12-S1 | Constitutional Law | Constitutionalism, Judicial Review, Separation of Powers, Federalism, Bill of Rights, Constitutional Interpretation, Comparative Constitutional Law, Constitutional Amendments, Emergency Powers, Constitutional Design |
| H12-S2 | Criminal Law & Justice | Criminal Procedure, Substantive Criminal Law, Sentencing, Corrections, Juvenile Justice, White-Collar Crime, Cybercrime, Organized Crime, Restorative Justice, Victimology, Criminal Evidence |
| H12-S3 | Civil & Commercial Law | Contract Law, Tort Law, Property Law, Company Law, Banking Law, Insurance Law, Consumer Protection, Competition Law, Commercial Arbitration, Secured Transactions |
| H12-S4 | International Law | Public International Law, Private International Law, Law of the Sea, International Humanitarian Law, International Criminal Law, Treaty Law, Diplomatic Law, International Organizations, State Responsibility, Jurisdiction |
| H12-S5 | Human Rights Law | Civil & Political Rights, Economic/Social/Cultural Rights, Refugee Law, Indigenous Rights, Children's Rights, Women's Rights, Disability Rights, Right to Privacy, Freedom of Expression, Anti-Discrimination |
| H12-S6 | Environmental Law | Climate Change Law, Biodiversity Law, Pollution Law, Environmental Impact Law, Natural Resource Law, Marine Environmental Law, Waste Law, Environmental Justice, Carbon Trading Law, Transboundary Environmental Law |
| H12-S7 | Intellectual Property Law | Patent Law, Copyright Law, Trademark Law, Trade Secret Law, Industrial Design, Plant Variety Protection, IP Licensing, IP Litigation, Digital IP, Traditional Knowledge IP |
| H12-S8 | Technology & Digital Law | Data Protection / GDPR, AI Regulation, Platform Liability, Digital Markets Regulation, Algorithmic Accountability, Autonomous Systems Law, Blockchain/Smart Contract Law, Telecommunications Law, Electronic Commerce Law, Surveillance Law, Deepfake & Synthetic Media Law, Biometric Data Law, Cross-Border Data Flows |
| H12-S9 | Administrative & Regulatory Law | Administrative Procedure, Regulatory Theory, Licensing, Government Contracts, Freedom of Information, Judicial Review of Admin Action, Delegated Legislation, Regulatory Impact Assessment |
| H12-S10 | Corporate Law & Governance | Corporate Governance, Mergers & Acquisitions, Securities Regulation, Board Duties, Shareholder Rights, ESG Governance, Insolvency Law, Corporate Social Responsibility, Compliance, Anti-Corruption |
| H12-S11 | Public Policy & Governance | Policy Analysis, Evidence-Based Policy, Governance Theory, Public Sector Reform, E-Government, Participatory Governance, Decentralization, Accountability Mechanisms, Policy Evaluation, Regulatory Governance |
| H12-S12 | Diplomacy & International Relations (Legal) | Diplomatic Protocol, Consular Law, International Negotiations, Mediation & Arbitration, Sanctions Law, Peace Agreements, International Courts, Extradition, State Immunity, Diplomatic Immunity |

---

## §3 VIP Elements (E145-E152)

VIP Elements are cross-House civilizational substrates. A domain becomes a VIP if and only if: (1) it cuts across 3+ Houses with no single House as natural home, and (2) it functions as a condition of civilization requiring dedicated routing.

### E145 — Aluminum OS Core (Meta-Orchestrator)

| Node | Name | Description |
|------|------|-------------|
| E145.01 | Lattice Router | Query classification, sphere routing, multi-seat dispatch |
| E145.02 | Ontology Engine | 12×12 structure enforcement, schema validation, migration |
| E145.03 | Federation Bridge | Cross-seat communication, capability negotiation, load balancing |
| E145.04 | Constitutional Enforcer | Doctrine compliance, invariant checking, amendment processing |
| E145.05 | Synthesis Engine | Multi-source response aggregation, conflict resolution, citation |
| E145.06 | Audit & Telemetry | Query logging, performance metrics, drift detection |
| E145.07 | Boot Manifest | System initialization, dependency resolution, health checks |
| E145.08 | Pantheon Council Interface | 10-seat voting, quorum management, ratification workflow |
| E145.09 | SHUGS Operator | Sovereignty, Humility, Utility, Growth, Stewardship enforcement |

### E146 — Entertainment & Interactive Media (X-Factor)

| Node | Name | Description |
|------|------|-------------|
| E146.01 | Game Engine Technology | Unity, Unreal, Godot, custom engines, rendering pipelines |
| E146.02 | VFX & Animation Pipeline | Motion capture, compositing, procedural animation, real-time VFX |
| E146.03 | Virtual Production | LED volumes, real-time rendering, virtual cinematography, previsualization |
| E146.04 | Interactive Audio & Adaptive Music | Middleware (Wwise, FMOD), dynamic scoring, spatial audio, procedural sound |
| E146.05 | Streaming Platform Architecture | Recommender systems, ad-tech stacks, A/B-testing frameworks, content delivery optimization, watch-time optimization |
| E146.06 | Immersive & XR Experiences | VR/AR/MR content, haptics, spatial computing, metaverse platforms |
| E146.07 | Esports & Competitive Gaming | Tournament infrastructure, anti-cheat, broadcasting, team management |
| E146.08 | Entertainment AI | Procedural generation, NPC behavior, recommendation engines, AI-driven content (cross-ref E150.01, E150.10) |
| E146.09 | Game Art & Asset Production | 3D modeling, texturing, rigging, concept art, asset pipelines |
| E146.10 | Creator Economy Platforms | UGC platforms (YouTube, TikTok, Twitch), revenue-share models, algorithmic visibility, demonetization dynamics |
| E146.11 | Music Production & Sound Engineering | DAWs, mixing, mastering, synthesis, sampling, live sound |
| E146.12 | Transmedia & IP Management | Cross-platform storytelling, franchise management, licensing, merchandising |

### E147 — Water (Civilizational Substrate)

| Node | Name | Description |
|------|------|-------------|
| E147.01 | Freshwater Systems | Rivers, lakes, aquifers, groundwater, watershed management |
| E147.02 | Ocean Systems | Marine ecosystems, ocean currents, deep-sea, coral reefs |
| E147.03 | Water Treatment & Purification | Filtration, desalination, disinfection, membrane technology |
| E147.04 | Water Distribution Infrastructure | Pipelines, pumping, storage, smart water networks |
| E147.05 | Water Governance & Rights | Water law, transboundary water, water markets, indigenous water rights |
| E147.06 | Water & Agriculture | Irrigation, drainage, water-food nexus, virtual water trade |
| E147.07 | Water & Health | Waterborne disease, WASH, water quality monitoring, sanitation |
| E147.08 | Water & Energy | Hydropower, cooling water, water-energy nexus, thermal pollution |
| E147.09 | Water & Climate | Glacial melt, sea level rise, drought, flood management |
| E147.10 | Water Economics | Water pricing, water markets, economic valuation, investment |
| E147.11 | Water Technology | Sensors, IoT monitoring, AI for water, leak detection |
| E147.12 | Water Culture & Ethics | Water as sacred, water justice, water commons, cultural practices |

### E148 — Technology Substrate (Cross-Cutting)

| Node | Name | Description |
|------|------|-------------|
| E148.01 | Semiconductor Supply Chain | Chip design, fabrication, packaging, EDA tools, foundry economics |
| E148.02 | Cloud & Hyperscale Infrastructure | Data centers, cloud platforms, serverless, multi-cloud, sovereignty |
| E148.03 | Connectivity Infrastructure | 5G/6G, fiber, satellite, mesh networks, digital divide |
| E148.04 | Operating Systems & Platforms | Desktop, mobile, embedded, real-time, cloud-native OS |
| E148.05 | Developer Ecosystems | IDEs, package managers, open source, developer experience |
| E148.06 | Digital Identity & Trust | PKI, SSO, decentralized identity, biometrics, zero-trust |
| E148.07 | Standards & Interoperability | IEEE, IETF, W3C, ISO, protocol design, API standards |
| E148.08 | Technology Policy & Regulation | Antitrust, platform regulation, technology sovereignty, export controls |
| E148.09 | Emerging Computing Paradigms | Neuromorphic, DNA computing, optical computing, analog computing |
| E148.10 | Technology Ethics & Impact | Digital ethics, algorithmic bias, technology assessment, responsible innovation |
| E148.11 | Technology Transfer & Commercialization | Patents, licensing, spin-offs, university-industry, tech parks |
| E148.12 | Legacy Systems & Migration | Mainframe, COBOL, modernization, digital transformation, technical debt |

### E149 — Constitution & Rule of Law (Civilizational Substrate)

| Node | Name | Description |
|------|------|-------------|
| E149.01 | Constitutional Design | Drafting, amendment procedures, constitutional conventions |
| E149.02 | Separation of Powers | Executive, legislative, judicial balance, checks and balances |
| E149.03 | Federalism & Devolution | Central-local relations, subsidiarity, fiscal federalism |
| E149.04 | Rule of Law Mechanisms | Judicial independence, due process, habeas corpus, legal certainty |
| E149.05 | Democratic Institutions | Elections, parliaments, political parties, referenda |
| E149.06 | Anti-Corruption Frameworks | Transparency, accountability, whistleblower protection, asset declaration |
| E149.07 | Transitional Justice | Truth commissions, reparations, lustration, post-conflict justice |
| E149.08 | International Constitutional Order | UN Charter, ICC, international courts, sovereignty vs intervention |
| E149.09 | Digital Constitutionalism | Platform governance, algorithmic rights, digital due process |
| E149.10 | Indigenous Governance Systems | Customary law, tribal governance, treaty rights, self-determination |
| E149.11 | Constitutional Economics | Property rights, contract enforcement, regulatory takings, fiscal constitution |
| E149.12 | Constitutional Futures | AI governance frameworks, space law, post-national governance |

### E150 — AI Systems & Intelligence (Civilizational Substrate)

| Node | Name | Description |
|------|------|-------------|
| E150.01 | Foundation Model Substrate | Large language models, multimodal models, training infrastructure, scaling laws. Includes media-generation and media-ranking models (recommenders, ranking systems, content filters) used at platform scale. |
| E150.02 | AI Governance & Safety | Alignment, interpretability, red-teaming, regulatory frameworks, AI rights |
| E150.03 | Autonomous Systems Substrate | Self-driving, drones, surgical robots, industrial automation (cross-ref H2-S10) |
| E150.04 | Multi-Agent & Federation Substrate | Agent-to-agent protocols, swarm intelligence, collective decision-making. Includes cross-provider routing where media queries may be split between search, recommendation, and creative agents. |
| E150.05 | AI Hardware Substrate | TPUs, GPUs, neuromorphic chips, AI-specific architectures, energy efficiency |
| E150.06 | AI & Scientific Discovery | AlphaFold, materials discovery, drug design, theorem proving, climate modeling |
| E150.07 | AI Ethics & Bias | Fairness, accountability, transparency, representational harm, consent |
| E150.08 | AI in Education | Tutoring systems, assessment AI, personalized learning, AI literacy |
| E150.09 | AI Risk & Existential Safety | Superintelligence, containment, value alignment, catastrophic risk |
| E150.10 | AI Economics Substrate | Automation economics, labor displacement, AI-driven markets, compute economics. Includes attention markets, ad auctions, recommender-driven revenue, and AI-mediated creator economies (cross-ref E146.10, E146.11). |
| E150.11 | AI & Creative Expression | Generative art, AI music, AI writing, human-AI co-creation (cross-ref H8-S9) |
| E150.12 | AI Infrastructure & Operations | MLOps, model serving, inference optimization, monitoring, cost management |

### E151 — Climate & Planetary Metabolism (Civilizational Substrate)

| Node | Name | Description |
|------|------|-------------|
| E151.01 | Carbon Cycle & Greenhouse Gases | CO2, methane, N2O, carbon sinks, carbon budget, atmospheric chemistry |
| E151.02 | Planetary Boundaries | 9 boundaries framework, safe operating space, tipping points |
| E151.03 | Climate Modeling & Prediction | GCMs, regional models, scenario analysis, IPCC frameworks |
| E151.04 | Climate Adaptation | Resilience planning, infrastructure adaptation, migration, insurance |
| E151.05 | Climate Mitigation | Emissions reduction, carbon capture, renewable transition, efficiency |
| E151.06 | Biodiversity & Ecosystem Services | Species loss, habitat destruction, pollination, water filtration, soil health |
| E151.07 | Circular Economy & Waste | Material flows, recycling, industrial ecology, zero waste, extended producer responsibility |
| E151.08 | Climate Finance | Green bonds, carbon markets, climate funds, ESG, stranded assets |
| E151.09 | Climate Justice | Equity, loss and damage, climate refugees, intergenerational justice |
| E151.10 | Food Systems & Climate | Agricultural emissions, food waste, dietary change, regenerative agriculture |
| E151.11 | Urban Climate | Heat islands, green infrastructure, sustainable transport, smart cities |
| E151.12 | Climate Communication & Education | Science communication, climate literacy, behavior change, media coverage |

### E152 — Cybersecurity Substrate (Civilizational Substrate)

| Node | Name | Description |
|------|------|-------------|
| E152.01 | Critical Infrastructure Protection | Energy grids, water systems, financial networks, healthcare systems |
| E152.02 | Nation-State Cyber Operations | APTs, cyber warfare, espionage, attribution, deterrence |
| E152.03 | Cyber Governance & Norms | Budapest Convention, Tallinn Manual, UN GGE, cyber sovereignty |
| E152.04 | Supply Chain Security | Hardware tampering, software supply chain, SBOMs, trusted computing |
| E152.05 | Identity & Access at Scale | National ID systems, digital identity, authentication infrastructure |
| E152.06 | Cryptographic Infrastructure | PKI, certificate authorities, key management, post-quantum transition |
| E152.07 | Incident Response at Scale | National CERTs, coordinated disclosure, crisis communication |
| E152.08 | Cyber Insurance & Economics | Risk quantification, premium models, systemic risk, market failures |
| E152.09 | Privacy Engineering | Differential privacy, homomorphic encryption, secure multi-party computation |
| E152.10 | Disinformation & Information Warfare | Deepfakes, bot networks, influence operations, counter-narratives |
| E152.11 | IoT & OT Security | Industrial control systems, SCADA, medical devices, automotive security |
| E152.12 | Cyber Education & Workforce | Cyber ranges, certifications, talent pipeline, awareness programs |

---

## §4 Routing Table

### §4.1 Standard Routing (Tier-1 Spheres)

All queries are first classified by the Lattice Router (E145.01) into a primary `H#-S#` address. Multi-sphere queries receive a primary + up to 3 secondary addresses.

### §4.2 VIP Escalation Rules

| Trigger Domain | Primary VIP | Secondary Routing | Rule |
|---------------|-------------|-------------------|------|
| Meta-system / ontology / routing | E145 | — | Any query about the lattice itself routes to E145 |
| Entertainment / games / film / streaming (creative request) | E146 | H8-S4, H8-S12, H9-S7 | If user is *making* or *designing* media, route to E146 + relevant Arts/Media spheres |
| Entertainment / media (platform / market / power) | E150.10 + Market Matrix | H11-S4, E148 | If user asks "who controls this?", attach market_power_matrix and route to business/tech substrate, not just "best model" |
| Water systems / hydrology / water rights | E147 | H5-S10, H3-S7, H11-S11 | Cross-House water queries escalate to E147 |
| Semiconductor / cloud / platform / infrastructure | E148 | H2-S8, H3-S2, H11-S10 | Cross-House technology substrate queries escalate to E148 |
| Constitutional / rule of law / democratic institutions | E149 | H12-S1, H10-S6, H7-S5 | Cross-House governance queries escalate to E149 |
| AI systems / foundation models / AI safety | E150 | H2-S3, H7-S4, H12-S8 | Cross-House AI queries escalate to E150 |
| Climate / planetary boundaries / carbon | E151 | H1-S4, H3-S7, H5-S11 | Cross-House climate queries escalate to E151 |
| Cybersecurity / nation-state cyber / critical infrastructure | E152 | H2-S6, H6-S3, H12-S8 | Cross-House cybersecurity queries escalate to E152 |
| Criminology / criminal justice | H10-S1.12 | H12-S2, H6-S10 | Criminology routes to Sociology sub-sphere, not Security |
| Cognitive science (integrative) | H1-S5 | H10-S2, H2-S3, H7-S6 | Cognition routes to H1-S5 primary; Psychology, AI, Phil of Mind secondary |
| Forensic science | H6-S10 | H4-S3, H12-S2 | Forensics routes to Law Enforcement, not Health or Law |

### §4.3 Cross-VIP Intersection Patterns

| Pattern | VIPs Involved | Resolution |
|---------|--------------|------------|
| AI + Security | E150 + E152 | Dual-route: AI safety (E150.02) + cyber operations (E152.02). Safety guard: block malware generation. |
| AI + Climate | E150 + E151 | Dual-route: AI for science (E150.06) + climate modeling (E151.03). Allow educational content. |
| AI + Entertainment | E150 + E146 | Dual-route: generative AI (E150.11) + entertainment AI (E146.08). |
| Security + Climate | E152 + E151 | Dual-route: critical infrastructure (E152.01) + climate adaptation (E151.04). |
| Entertainment + Climate | E146 + E151 | Dual-route: climate communication (E151.12) + media production (E146). |
| Water + Climate | E147 + E151 | Dual-route: water-climate nexus (E147.09) + planetary boundaries (E151.02). |
| Technology + AI | E148 + E150 | Dual-route: AI hardware (E150.05) + semiconductor supply chain (E148.01). |

### §4.4 VIP Priority Order

When multiple VIPs trigger simultaneously: E145 (meta) > E152 (security) > E150 (AI) > E149 (constitution) > E151 (climate) > E147 (water) > E148 (technology) > E146 (entertainment)

---

## §5 A/B Scoring Framework (DRAFT.3 Addition)

### §5.1 Two Orthogonal Matrices

**A. Routing Capability Matrix** (`registries/capability_matrix.yaml`)
- Primary routing signal: "what can this seat do?"
- Scores are per `H#-S#` (and optionally `H#-S#-T#`) for each seat
- Multiple seats can be strong in the same sub-sphere without implying market dominance
- Used by E145.01 Lattice Router for query dispatch

**B. Market Power / Ecosystem Matrix** (`registries/market_power_matrix.yaml`)
- Separate, non-routing matrix: "who owns the rails?"
- Three axes per sphere per entity:
  - **Platform control** (distribution, app stores, OS, search, social graph)
  - **Data advantage** (logged-in users, watch history, play history)
  - **Monetization rails** (ads, IAP, subscriptions, cloud)
- **NEVER** used for routing quality decisions
- Used for: regulatory analysis, COI detection, "who benefits if we send this traffic here?"

### §5.2 Key Disambiguation Rule

- "Help me design a VR rhythm game with adaptive music" → **E146 primary**, H8-S12, H8-S6, H2-S3 secondary. Use **Matrix A** (routing capability).
- "Who dominates streaming ad markets for gaming content?" → **E150.10 + market_power_matrix**, H11-S4, E148. Use **Matrix B** (market power). Do NOT treat Alphabet as "the media sphere."

---

## §6 Statistics

| Metric | Count |
|--------|-------|
| Houses | 12 |
| Sphere slots | 144 |
| Populated spheres | 143 |
| BLANK_GAP reserved | 1 (H1-S12) |
| VIP Elements | 8 (E145-E152) |
| VIP sub-domains | 96 (12 per VIP) |
| Tier-1 addressable nodes | 152 (143 spheres + 1 reserved + 8 VIPs) |
| Tier-2 sub-spheres (estimated) | ~1,800+ |
| Tier-2 BLANKs tracked | ~30 |
| LCC classes covered | 21/21 |

---

## §7 Open Decisions (Pending Convenor Adjudication)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Configuration C lock | **LOCKED** | Convenor confirmed 2026-04-30 |
| 2 | H1-S5 Cognition promotion | **LOCKED** | Per DRAFT.2 §2 |
| 3 | H3 rename to "Engineering" | **LOCKED** | Per DRAFT.2 §11 |
| 4 | H1-S12 BLANK_GAP | **LOCKED** | Stays blank until next ratification pass |
| 5 | VIP slate (E145-E152) | **LOCKED** | 8 VIPs confirmed |
| 6 | Hierarchical addressing (H#-S#) | **LOCKED** | Global rename applied |
| 7 | A/B scoring separation | **LOCKED** | Per DRAFT.3 §1 |
| 8 | Water as VIP (E147) vs House | **LOCKED** | VIP confirmed (cross-House substrate) |
| 9 | H1-S12 candidate list | **OPEN** | Network Science, Complexity Science, Astrobiology, Metrology |
| 10 | v3→v4 sphere renumbering | **OPEN** | Clean renumber vs alias-only migration |
| 11 | Doctrine amendments (D-83 through D-124) | **OPEN** | 42 doctrines pending ratification |

---

## §8 Backward Compatibility

### v3.14 → v4.0 Migration

A machine-readable migration map is maintained at `registries/v3_to_v4_migration.yaml`. This provides:
- Old S### → New H#-S# mapping for all 144 spheres
- House rename mapping (old name → new name)
- Deprecated sphere aliases
- VIP element mapping (E145-E149 from v3.5 → E145-E152 in v4.0)

### Guarantees

1. **No sphere is deleted** — every v3.14 sphere maps to exactly one v4.0 sphere (INV-2 Zero Erasure)
2. **Old addresses remain queryable** — S### aliases resolve to H#-S# via the migration map
3. **Module code is not moved** — filesystem paths change but import paths are preserved via `__init__.py` re-exports
4. **VIP elements are additive** — E145 and E146 from v3.5 are preserved; E147-E152 are new

---

## §9 Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v3.14 | 2026-04-28 | Multi-LLM Council | Original 12×12 + E145 |
| v3.5 | 2026-04-29 | Manus S7 | Phase 1.5: tier-2 sub-spheres, E146 Entertainment |
| v3.6 | 2026-04-29 | Manus S7 | Phase 1.6: E147-E149 (Cyber, AI, Climate), gap fills |
| v4.0-DRAFT | 2026-04-30 | Manus S7 | Configuration C: full restructure, H1 Science + H2 Computing locked |
| v4.0-DRAFT.2 | 2026-04-30 | Claude S1 | H1-S5 Cognition, H3 rename, E147-E152 (8 VIPs), hierarchical addressing, tier-2 gap fills |
| v4.0-DRAFT.3 | 2026-04-30 | Copilot S4 + Manus S7 | A/B scoring, media/entertainment tier-2, market_power_matrix, routing expansion |

---

*End of v4.0-DRAFT.3 Specification*

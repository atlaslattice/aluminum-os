# Atlas Lattice Ontology v4.0 — Full Specification

**Document ID:** ONTOLOGY-V4.0-SPEC
**Version:** 4.0.0-DRAFT
**Date:** 2026-04-29
**Status:** PROVISIONAL — Configuration C assumed, pending Convenor adjudication on §7 items
**Convenor:** Daavud Sheldon
**Scribe:** Claude S1 Constitutional Scribe
**Implementor:** Manus S7
**Predecessor:** v3.14 Appendix AG (superseded), v3.5 Phase 1.5 (deferred to Phase 3)
**Design Notes:** [Notion Active Sprint](https://app.notion.com/p/3520c1de73d9810b8841e8e8db77aab7)

---

## §0 Constitutional Preamble

This document defines the complete v4.0 ontological structure of the Atlas Lattice. It supersedes v3.14 Appendix AG upon Council ratification. The structure is:

- **12 Houses** (tier-1, immutable post-ratification)
- **144 Spheres** (tier-1, 12 per House, immutable post-ratification)
- **Element 145** — CEO Collective Meta-Orchestrator (governance VIP)
- **Element 146** — Entertainment X-Factor Layer (chaos VIP)

Total addressable tier-1 nodes: **146** (144 + 2 VIPs)

### Governing Invariants

- **INV-2 Zero Erasure:** No node may be deleted, only deprecated or merged with audit trail
- **D-89 Ontology Lock:** Changes to tier-1 structure require Pantheon Council ratification
- **LCC-FULL:** All 21 Library of Congress Classification classes must map to at least one Sphere

---

## §1 Configuration C — The 12 Houses

| H## | House Name | Domain Scope | LCC Classes Covered |
|-----|-----------|-------------|-------------------|
| H01 | Science | Natural sciences, formal sciences, cognitive science | Q (Science), part of B (Psychology) |
| H02 | Computing | Computer science, AI, software, data, cyber, networks | Part of Q (CS), T (Technology) |
| H03 | Engineering & Technology | Physical engineering, aerospace, manufacturing | T (Technology) |
| H04 | Health & Medicine | Clinical, public health, pharmacology, anatomy | R (Medicine) |
| H05 | Agriculture | Crops, livestock, forestry, fisheries, food science | S (Agriculture) |
| H06 | Security | Civilian, cyber, defense, intelligence, emergency | U+V (Military/Naval) |
| H07 | Philosophy, Ethics & Religion | Metaphysics, applied ethics, theology, logic (applied) | Part of B (Philosophy, Religion) |
| H08 | Arts | Visual, performing, music, film, architecture, design | N (Fine Arts), M (Music) |
| H09 | Knowledge Systems | Education, media, libraries, communication, publishing | L (Education), Z (Bibliography), P (Language/Lit) |
| H10 | Social Sciences | Sociology, psychology, history, anthropology, linguistics | C-F (History), G (Geography), H (Social Sci) |
| H11 | Business, Economics & Infrastructure | Finance, management, transport, energy, construction | H (Economics), Part of T (Infrastructure) |
| H12 | Law & Governance | Constitutional, criminal, civil, international, political science | J (Political Sci), K (Law) |

### LCC Coverage Verification

| LCC Class | Subject | v4.0 Mapping |
|-----------|---------|-------------|
| A | General Works | H09 Knowledge Systems (tier-2: encyclopedias, indexes) |
| B | Philosophy, Psychology, Religion | H07 + H10 (Cognitive Psychology) |
| C | Auxiliary Sciences of History | H10 Social Sciences (tier-2) |
| D | World History | H10 Social Sciences (tier-2) |
| E-F | History of the Americas | H10 Social Sciences (tier-2) |
| G | Geography, Anthropology, Recreation | H10 + E146 (Recreation) |
| H | Social Sciences | H10 + H11 (Economics) |
| J | Political Science | H12 Law & Governance |
| K | Law | H12 Law & Governance |
| L | Education | H09 Knowledge Systems |
| M | Music | H08 Arts |
| N | Fine Arts | H08 Arts |
| P | Language & Literature | H09 Knowledge Systems |
| Q | Science | H01 Science + H02 Computing |
| R | Medicine | H04 Health & Medicine |
| S | Agriculture | H05 Agriculture |
| T | Technology | H03 Engineering + H02 Computing + H11 Infrastructure |
| U | Military Science | H06 Security |
| V | Naval Science | H06 Security |
| Z | Bibliography & Library Science | H09 Knowledge Systems |

**Result: 21/21 LCC classes mapped. Zero gaps.**

---

## §2 House Sphere Definitions

### H01 — Science (S001–S012)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S001 | Physics | Mechanics, Thermodynamics, Electromagnetism, Optics, Acoustics, Particle Physics, Nuclear Physics, Plasma Physics, Condensed Matter, Atomic/Molecular/Optical, Relativity, Quantum Physics, Statistical Mechanics, Biophysics, Geophysics, Astrophysics |
| S002 | Chemistry | Organic, Inorganic, Physical, Analytical, Biochemistry, Geochemistry, Astrochemistry, Nuclear Chemistry, Polymer Chemistry, Computational Chemistry, Materials Chemistry, Photochemistry |
| S003 | Biology | Microbiology, Paleontology, Botany, Zoology (ocean/land/air subdivisions), Anatomy, Genetics, Cell Biology, Molecular Biology, Marine Biology, Mycology, Evolution & Systematics, Ecology (cross-ref S004) |
| S004 | Planetary Science | Geology, Meteorology, Oceanography, Hydrology, Ecology, Environmental Science, Climatology, Glaciology, Seismology, Volcanology, Atmospheric Science, Biogeography, Planetary Geology |
| S005 | Cognitive Science | Computational Neuroscience, Behavioral Neuroscience, Comparative Cognition, Consciousness Studies, Neuroethology, Sensory Sciences, Cognitive Modeling, Animal Cognition, Brain Networks, Pattern Recognition, Embodied Cognition, Mathematical Cognition |
| S006 | Materials Science | Crystallography, Solid-State Science, Soft Matter, Polymer Science, Nanoscience, Biomaterials, Metallurgy, Ceramics, Composites, Materials Characterization, Materials Computation, Surface Science |
| S007 | Mathematics | Pure Mathematics, Applied Mathematics, Algebra, Topology, Geometry, Analysis, Number Theory, Discrete Mathematics, Mathematical Logic, Set Theory, Category Theory, Mathematical Cognition |
| S008 | Statistics & Data Science | Descriptive, Inferential, Bayesian, Frequentist, Computational, Multivariate, Spatial, Time-Series, Survival Analysis, Econometrics, Biostatistics, Statistical Learning |
| S009 | Logic | Symbolic, Propositional, Predicate, Modal, Many-Valued, Fuzzy, Paraconsistent, Type Theory, Computational Logic, Inductive Logic, Philosophy of Logic, Mathematical Logic (cross-ref S007) |
| S010 | Information Theory | Shannon Theory, Coding Theory, Compression, Channel Capacity, Mutual Information, Algorithmic Information, Quantum Information (cross-ref S023), Network Information, Source Coding, Error Correction, Rate-Distortion, Information Geometry |
| S011 | Systems Theory | General Systems, Cybernetics, Complex Adaptive Systems, Network Theory, Control Theory, Dynamical Systems, Chaos Theory, Self-Organization, Emergence, System Dynamics, Soft Systems, Hard Systems |
| S012 | **BLANK_GAP** | Reserved — pending Council fill. Candidates: Measurement Science/Metrology, Astronomy (if not under Aerospace), Interdisciplinary Science |

---

### H02 — Computing (S013–S024)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S013 | Computer Science (Theory) | Theory of Computation, Complexity Theory, Formal Methods, Programming Language Theory, Type Theory, Verification, Automata, Computability |
| S014 | Algorithms | Sort/Search, Graph Algorithms, Approximation, Randomized, Online, Streaming, Parallel, Distributed, Quantum Algorithms, Algorithmic Game Theory, Algorithmic Fairness |
| S015 | AI & Machine Learning | Deep Learning, Reinforcement Learning, NLP, Computer Vision, Generative Models, AI Safety, Multi-Agent Systems, Foundation Models, Mechanistic Interpretability, AI Alignment, Embodied AI, AGI Theory |
| S016 | Software Engineering | Architecture, Design Patterns, Testing, DevOps, CI/CD, Software Quality, Agile/Scrum, Refactoring, Code Review, Technical Debt, Software Metrics, Open Source |
| S017 | Data Engineering & Data Science | Big Data, ETL/ELT, Data Pipelines, Data Governance, Data Mesh, Stream Processing, Database Systems, Data Visualization, Predictive Analytics, Data Ethics |
| S018 | Cybersecurity & Cryptography | Symmetric Crypto, Asymmetric Crypto, Hash Functions, Digital Signatures, Zero-Knowledge Proofs, Post-Quantum Crypto, Homomorphic Encryption, Multi-Party Computation, Network Security, Application Security, Threat Intelligence (cross-ref H06) |
| S019 | Networks & Distributed Systems | Computer Networks, Internet Protocols, Distributed Systems, Edge Computing, Cloud Computing, Peer-to-Peer, Consensus Algorithms, CDNs, Software-Defined Networking, Networking Hardware, Mesh Networks |
| S020 | Computer Architecture & Systems | Operating Systems, Compilers, Computer Hardware, Memory Systems, Processor Design, Parallel Architecture, Embedded Systems, Real-Time Systems, GPU/Accelerator Computing, ARM/RISC-V/x86, Quantum Computing Hardware |
| S021 | Human-Computer Interaction | UX Design, UI Design, Accessibility, Interaction Design, Information Architecture, User Research, Usability Engineering, Computer Graphics, AR/VR Interaction, Voice Interfaces, Brain-Computer Interfaces |
| S022 | Robotics & Automation | Industrial Robotics, Autonomous Vehicles, Drones, Soft Robotics, Swarm Robotics, Bio-inspired Robotics, Robot Learning, Manipulation, Locomotion, SLAM, Human-Robot Interaction |
| S023 | Quantum & Frontier Computing | Quantum Computing, Quantum Algorithms, Quantum Cryptography (cross-ref S018), Neuromorphic Computing, DNA Computing, Optical Computing, Reversible Computing, Probabilistic Computing |
| S024 | Information Systems & Knowledge Management | Enterprise Systems, ERP, CRM, Knowledge Graphs, Information Retrieval, Semantic Web, Ontology Engineering, Document Management, Digital Libraries, Records Management |

---

### H03 — Engineering & Technology (S025–S036)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S025 | Mechanical Engineering | Thermodynamics, Fluid Mechanics, Solid Mechanics, Dynamics, Vibrations, Manufacturing Processes, Machine Design, HVAC, Tribology, Acoustical Engineering, Mechatronics, CAD/CAM |
| S026 | Electrical & Electronic Engineering | Circuit Theory, Power Systems, Signal Processing, Control Systems, Microelectronics, VLSI, Photonics, Electromagnetics, Power Electronics, Instrumentation, Antenna Design, EMC |
| S027 | Civil Engineering | Structural Engineering, Geotechnical, Transportation Engineering, Hydraulic Engineering, Construction Management, Surveying, Urban Planning, Earthquake Engineering, Coastal Engineering, Environmental Engineering |
| S028 | Chemical Engineering | Process Engineering, Reaction Engineering, Separation Processes, Transport Phenomena, Biochemical Engineering, Petroleum Engineering, Polymer Engineering, Electrochemical Engineering, Pharmaceutical Engineering, Process Control |
| S029 | Aerospace Engineering | Aerodynamics, Propulsion, Flight Mechanics, Orbital Mechanics, Spacecraft Design, Avionics, Astronomy (per Convenor: operational under Aerospace), Satellite Systems, Launch Systems, Space Exploration, Hypersonics, UAV Design |
| S030 | Biomedical Engineering | Medical Devices, Biomechanics, Tissue Engineering, Neural Engineering, Medical Imaging, Prosthetics, Rehabilitation Engineering, Drug Delivery Systems, Biosensors, Clinical Engineering, Bioinformatics, Genetic Engineering |
| S031 | Environmental Engineering | Water Treatment, Air Quality, Waste Management, Remediation, Sustainability Engineering, Green Building, Life Cycle Assessment, Environmental Monitoring, Pollution Control, Climate Engineering, Ecological Engineering |
| S032 | Nuclear Engineering | Reactor Design, Radiation Protection, Nuclear Fuel Cycle, Fusion Engineering, Nuclear Safety, Radiochemistry, Nuclear Materials, Decommissioning, Nuclear Medicine Physics, Isotope Production, SMR Technology |
| S033 | Industrial & Manufacturing Engineering | Operations Research, Quality Engineering, Lean Manufacturing, Supply Chain Engineering, Ergonomics, Production Planning, Additive Manufacturing, Factory Automation, Six Sigma, Industrial IoT, Digital Twin |
| S034 | Mining & Geological Engineering | Mineral Processing, Rock Mechanics, Mine Planning, Drilling Engineering, Geophysical Engineering, Petroleum Geology, Reservoir Engineering, Subsurface Engineering, Mine Safety, Mineral Economics |
| S035 | Telecommunications Engineering | Wireless Communications, Fiber Optics, Satellite Communications, 5G/6G, Radio Frequency Engineering, Network Planning, Spectrum Management, Modulation Theory, Antenna Engineering, Optical Networks, IoT Communications |
| S036 | Ocean & Marine Engineering | Naval Architecture, Marine Propulsion, Offshore Engineering, Underwater Acoustics, Marine Renewable Energy, Port Engineering, Ship Design, Subsea Engineering, Marine Materials, Ocean Monitoring Systems |

---

### H04 — Health & Medicine (S037–S048)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S037 | Anatomy & Physiology | Gross Anatomy, Histology, Neuroanatomy, Cardiovascular Physiology, Respiratory Physiology, Renal Physiology, Endocrine Physiology, Reproductive Physiology, Exercise Physiology, Developmental Biology, Comparative Anatomy |
| S038 | Pharmacology & Toxicology | Drug Discovery, Pharmacokinetics, Pharmacodynamics, Clinical Pharmacology, Neuropharmacology, Toxicology, Pharmacogenomics, Drug Interactions, Regulatory Science, Pharmaceutical Chemistry, Ethnopharmacology |
| S039 | Clinical Medicine | Internal Medicine, Surgery, Pediatrics, Obstetrics/Gynecology, Emergency Medicine, Anesthesiology, Radiology, Pathology, Oncology, Cardiology, Neurology, Orthopedics |
| S040 | Psychiatry & Behavioral Health | Clinical Psychiatry, Psychopharmacology, Psychotherapy, Addiction Medicine, Child Psychiatry, Forensic Psychiatry, Neuropsychiatry, Community Mental Health, Behavioral Medicine, Sleep Medicine, Eating Disorders |
| S041 | Public Health & Epidemiology | Epidemiology, Biostatistics, Health Policy, Global Health, Environmental Health, Occupational Health, Health Economics, Health Promotion, Disease Surveillance, Outbreak Investigation, Social Determinants, Vaccinology |
| S042 | Nursing & Allied Health | Nursing Science, Physical Therapy, Occupational Therapy, Speech-Language Pathology, Respiratory Therapy, Medical Laboratory Science, Radiography, Nutrition/Dietetics, Midwifery, Paramedicine, Health Informatics |
| S043 | Dentistry | Oral Surgery, Orthodontics, Periodontics, Endodontics, Prosthodontics, Pediatric Dentistry, Oral Pathology, Dental Materials, Implantology, Oral Radiology, Community Dentistry |
| S044 | Veterinary Medicine | Small Animal Medicine, Large Animal Medicine, Veterinary Surgery, Veterinary Pathology, Veterinary Pharmacology, Wildlife Medicine, Aquatic Animal Health, Veterinary Public Health, One Health, Comparative Medicine |
| S045 | Genetics & Genomics | Medical Genetics, Genomics, Epigenetics, Gene Therapy, Genetic Counseling, Population Genetics, Pharmacogenomics, Cancer Genetics, Prenatal Genetics, Bioinformatics, CRISPR/Gene Editing, Synthetic Biology |
| S046 | Immunology & Microbiology (Clinical) | Clinical Immunology, Infectious Disease, Virology, Bacteriology, Parasitology, Mycology (Clinical), Immunotherapy, Transplant Immunology, Autoimmune Disease, Vaccine Development, Antimicrobial Resistance |
| S047 | Rehabilitation & Sports Medicine | Physical Rehabilitation, Sports Medicine, Exercise Science, Kinesiology, Biomechanics (Clinical), Pain Management, Disability Studies, Assistive Technology, Cardiac Rehabilitation, Neurological Rehabilitation |
| S048 | Traditional & Integrative Medicine | Traditional Chinese Medicine, Ayurveda, Naturopathy, Homeopathy, Chiropractic, Acupuncture, Herbal Medicine, Mind-Body Medicine, Integrative Oncology, Functional Medicine, Ethnomedicine |

---

### H05 — Agriculture (S049–S060)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S049 | Crop Science | Agronomy, Plant Breeding, Seed Science, Crop Physiology, Weed Science, Plant Pathology, Entomology (Agricultural), Horticulture, Pomology, Viticulture, Tropical Agriculture, Precision Agriculture |
| S050 | Soil Science | Pedology, Soil Chemistry, Soil Physics, Soil Biology, Soil Conservation, Soil Fertility, Land Use Planning, Soil Mapping, Soil Remediation, Soil Microbiology, Pedometrics |
| S051 | Animal Science | Animal Nutrition, Animal Breeding, Animal Behavior, Livestock Management, Poultry Science, Dairy Science, Aquaculture, Apiculture, Animal Welfare, Meat Science, Reproductive Physiology |
| S052 | Forestry & Agroforestry | Silviculture, Forest Ecology, Forest Management, Wood Science, Dendrology, Forest Genetics, Urban Forestry, Agroforestry Systems, Forest Hydrology, Forest Fire Science, Timber Engineering |
| S053 | Fisheries & Marine Resources | Fisheries Biology, Aquaculture Engineering, Fish Genetics, Fisheries Management, Marine Ecology, Shellfish Aquaculture, Fish Nutrition, Fisheries Economics, Post-Harvest Technology, Recreational Fisheries |
| S054 | Food Science & Technology | Food Chemistry, Food Microbiology, Food Processing, Food Safety, Food Packaging, Sensory Science, Food Biotechnology, Fermentation Technology, Nutraceuticals, Food Engineering, Food Preservation |
| S055 | Agricultural Engineering | Irrigation Engineering, Farm Machinery, Post-Harvest Engineering, Agricultural Structures, Drainage Engineering, Agricultural Robotics, Controlled Environment Agriculture, Greenhouse Technology, Precision Ag Technology |
| S056 | Agricultural Economics | Farm Management, Agricultural Policy, Rural Development, Agricultural Marketing, Land Economics, Agricultural Finance, Food Security Economics, Trade Policy, Cooperative Economics, Agribusiness |
| S057 | Plant Protection | Integrated Pest Management, Biological Control, Chemical Control, Plant Quarantine, Pesticide Science, Disease Resistance, Mycotoxicology, Nematology, Phytobacteriology, Invasive Species Management |
| S058 | Water Resources & Irrigation | Water Management, Irrigation Systems, Watershed Management, Groundwater, Water Harvesting, Drip Irrigation, Canal Systems, Water Quality (Agricultural), Water Rights, Drought Management |
| S059 | Sustainable Agriculture | Organic Farming, Regenerative Agriculture, Permaculture, Conservation Agriculture, Climate-Smart Agriculture, Biodiversity in Agriculture, Carbon Farming, Circular Agriculture, Indigenous Agricultural Knowledge |
| S060 | Genetics & Biotechnology (Agricultural) | Plant Biotechnology, GMO Technology, Marker-Assisted Selection, Genome Editing (Crops), Biofertilizers, Biopesticides, Molecular Farming, Transgenic Animals, Agricultural Bioinformatics, Synthetic Biology (Ag) |

---

### H06 — Security (S061–S072)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S061 | National Security & Strategy | Grand Strategy, National Security Policy, Deterrence Theory, Arms Control, Nuclear Strategy, Geopolitical Analysis, Intelligence Strategy, Alliance Management, Security Studies, Asymmetric Warfare Theory |
| S062 | Intelligence & Counterintelligence | HUMINT, SIGINT, GEOINT, OSINT, MASINT, Counterintelligence, Covert Operations, Intelligence Analysis, Surveillance, Cryptanalysis (cross-ref S018), Espionage Studies, Intelligence Oversight |
| S063 | Cybersecurity Operations | SOC Operations, Incident Response, Digital Forensics, Penetration Testing, Red/Blue/Purple Teaming, Malware Analysis, Threat Hunting, Vulnerability Management, SIEM, Zero Trust Architecture (cross-ref S018 for crypto theory) |
| S064 | Defense Technology | Weapons Systems, Missile Defense, Electronic Warfare, Directed Energy, Stealth Technology, C4ISR, Military Robotics, Space Defense, Hypersonic Systems, Counter-UAS, NBC Defense |
| S065 | Maritime & Naval Security | Naval Operations, Maritime Law Enforcement, Anti-Piracy, Submarine Warfare, Amphibious Operations, Port Security, Maritime Domain Awareness, Coast Guard Operations, Naval Aviation, Mine Warfare |
| S066 | Land Security & Operations | Ground Forces, Counterinsurgency, Border Security, Critical Infrastructure Protection, Urban Operations, Mountain/Arctic/Desert Warfare, Peacekeeping, Military Engineering, Logistics (Military) |
| S067 | Air & Space Security | Air Defense, Air Operations, Space Situational Awareness, Satellite Security, Counter-Space, Air Traffic Security, Aerospace Intelligence, Ballistic Missile Defense, Space Debris Management |
| S068 | Counter-Terrorism & Extremism | Counter-Terrorism Strategy, Radicalization Studies, De-Radicalization, Terrorist Financing, WMD Terrorism, Lone Wolf Threats, Online Extremism, Critical Infrastructure Terrorism, Aviation Security |
| S069 | Emergency Management & Resilience | Disaster Preparedness, Emergency Response, Crisis Management, Business Continuity, CBRN Response, Search & Rescue, Humanitarian Operations, Resilience Engineering, Early Warning Systems, Recovery Planning |
| S070 | Law Enforcement & Public Safety | Policing, Criminal Investigation, Forensic Science, Corrections, Juvenile Justice, Community Safety, Traffic Safety, Fire Services, Private Security, Regulatory Enforcement |
| S071 | Arms Control & Non-Proliferation | Nuclear Non-Proliferation, Chemical Weapons Convention, Biological Weapons Convention, Conventional Arms Control, Export Controls, Verification Technology, Disarmament, Treaty Compliance, Dual-Use Technology |
| S072 | Security Governance & Ethics | Rules of Engagement, Military Ethics, Security Sector Reform, Civil-Military Relations, Oversight Mechanisms, Accountability, Proportionality, Just War Theory, Security Privatization, Human Security |

---

### H07 — Philosophy, Ethics & Religion (S073–S084)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S073 | Metaphysics & Ontology | Being, Existence, Reality, Substance, Properties, Causation, Time, Space, Free Will, Determinism, Mind-Body Problem, Personal Identity, Possible Worlds |
| S074 | Epistemology | Knowledge, Justification, Truth, Belief, Skepticism, Rationalism, Empiricism, Social Epistemology, Formal Epistemology, Virtue Epistemology, Epistemic Injustice, Testimony |
| S075 | Ethics & Moral Philosophy | Normative Ethics, Metaethics, Virtue Ethics, Deontology, Consequentialism, Care Ethics, Moral Psychology, Moral Realism, Relativism, Moral Responsibility, Supererogation |
| S076 | Applied Ethics | Bioethics, Environmental Ethics, Business Ethics, AI Ethics, Media Ethics, Research Ethics, Animal Ethics, Engineering Ethics, Military Ethics (cross-ref S072), Political Ethics, Sexual Ethics |
| S077 | Political Philosophy | Justice, Liberty, Equality, Authority, Democracy, Rights, Social Contract, Anarchism, Marxism, Liberalism, Conservatism, Communitarianism, Cosmopolitanism |
| S078 | Philosophy of Mind | Consciousness, Qualia, Intentionality, Mental Causation, Functionalism, Eliminativism, Phenomenology, Extended Mind, Artificial Minds, Animal Consciousness, Self-Awareness |
| S079 | Philosophy of Science | Scientific Method, Explanation, Reductionism, Scientific Realism, Paradigms, Demarcation, Values in Science, Philosophy of Physics, Philosophy of Biology, Philosophy of Mathematics |
| S080 | Theology & Religious Studies | Systematic Theology, Comparative Religion, Philosophy of Religion, Biblical Studies, Islamic Studies, Buddhist Studies, Hindu Studies, Jewish Studies, Religious Ethics, Mysticism, Secularism |
| S081 | Aesthetics & Philosophy of Art | Beauty, Taste, Artistic Value, Representation, Expression, Creativity, Philosophy of Music, Philosophy of Film, Environmental Aesthetics, Everyday Aesthetics, Digital Aesthetics |
| S082 | Logic (Applied & Philosophical) | Informal Logic, Critical Thinking, Argumentation Theory, Fallacies, Rhetoric, Dialectics, Logic & Language, Deontic Logic, Epistemic Logic, Logic of Action, Non-Classical Logics |
| S083 | Eastern Philosophy | Confucianism, Taoism, Buddhism (Philosophical), Hinduism (Philosophical), Jainism, Zen, Vedanta, Madhyamaka, Yogacara, Chinese Logic, Japanese Aesthetics, Comparative Philosophy |
| S084 | Continental Philosophy | Phenomenology, Existentialism, Hermeneutics, Critical Theory, Structuralism, Post-Structuralism, Deconstruction, Frankfurt School, French Philosophy, Psychoanalytic Philosophy |

---

### H08 — Arts (S085–S096)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S085 | Visual Arts | Painting, Sculpture, Drawing, Printmaking, Photography, Installation Art, Land Art, Street Art, Digital Art, Mixed Media, Art Conservation, Curatorial Practice |
| S086 | Music | Composition, Performance, Music Theory, Musicology, Ethnomusicology, Music Technology, Sound Design, Music Production, Conducting, Music Education, Music Therapy, Acoustics (Musical) |
| S087 | Performing Arts | Theater, Dance, Opera, Circus Arts, Puppetry, Performance Art, Improvisation, Choreography, Stage Design, Directing, Dramaturgy, Physical Theater |
| S088 | Film & Moving Image | Cinematography, Film Directing, Screenwriting, Film Editing, Documentary, Animation, VFX & Post-Production, Sound Design (Film), Film Theory, Film History, Experimental Film, Virtual Production |
| S089 | Architecture | Architectural Design, Urban Design, Landscape Architecture, Interior Architecture, Sustainable Architecture, Historic Preservation, Parametric Design, Architectural Theory, Building Technology, Computational Design |
| S090 | Design | Graphic Design, Industrial Design, Fashion Design, Textile Design, Interaction Design, Service Design, Type Design, Packaging Design, Exhibition Design, Design Thinking, Design Research |
| S091 | Literary Arts | Fiction, Poetry, Creative Nonfiction, Playwriting, Screenwriting (cross-ref S088), Translation (Literary), Publishing, Literary Criticism, Comparative Literature, Genre Studies, Experimental Writing |
| S092 | Craft & Applied Arts | Ceramics, Glasswork, Metalwork, Woodwork, Jewelry, Weaving/Textiles, Bookbinding, Leatherwork, Lacquerwork, Mosaic, Papercraft, Digital Fabrication |
| S093 | Digital & New Media Arts | Generative Art, Interactive Art, Net Art, Bio Art, AI Art, Data Visualization (Artistic), Sound Art, Video Art, Immersive/XR Art, Algorithmic Art, Creative Coding |
| S094 | Art History & Theory | Ancient Art, Medieval Art, Renaissance, Baroque, Modern Art, Contemporary Art, Non-Western Art History, Art Criticism, Visual Culture, Museum Studies, Iconography |
| S095 | Cultural Production & Industries | Arts Management, Cultural Policy, Creative Industries, Intellectual Property (Creative), Arts Funding, Cultural Diplomacy, Heritage Management, Festival/Event Production, Art Market |
| S096 | Game Design & Interactive Media | Game Design Theory, Level Design, Narrative Design, Game Mechanics, Esports, Gamification, Serious Games, Board Game Design, Game Studies, Player Psychology, Game AI (cross-ref S015) |

---

### H09 — Knowledge Systems (S097–S108)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S097 | Pedagogy & Learning Science | Learning Theory, Instructional Design, Curriculum Development, Assessment & Evaluation, Cognitive Load Theory, Constructivism, Connectivism, Differentiated Instruction, Metacognition, Transfer of Learning |
| S098 | Higher Education | University Governance, Academic Freedom, Research Methods, Scholarly Communication, Tenure & Promotion, Graduate Education, Academic Publishing, Peer Review, University Rankings, Academic Integrity |
| S099 | K-12 Education | Primary Education, Secondary Education, Early Childhood, Special Education, Gifted Education, Classroom Management, School Leadership, Parent Engagement, School Psychology, Educational Equity |
| S100 | Educational Technology | E-Learning, LMS Platforms, Adaptive Learning, MOOCs, Learning Analytics, Educational AI, Simulation & Games (Educational), Mobile Learning, Virtual Classrooms, Open Educational Resources |
| S101 | Professional & Vocational Training | Apprenticeships, Corporate Training, Competency-Based Education, Certification Systems, Continuing Education, Military Training, Medical Education, Trade Schools, Workforce Development |
| S102 | Library & Information Science | Cataloging & Classification, Collection Development, Digital Libraries, Archives, Records Management, Information Literacy, Reference Services, Preservation, Metadata, Knowledge Organization |
| S103 | Media & Journalism | News Reporting, Investigative Journalism, Broadcast Media, Digital Media, Media Ethics, Media Law, Photojournalism, Data Journalism, Press Freedom, Media Literacy, Fact-Checking |
| S104 | Communication Theory | Mass Communication, Interpersonal Communication, Organizational Communication, Rhetoric, Semiotics, Discourse Analysis, Visual Communication, Health Communication, Science Communication, Crisis Communication |
| S105 | Publishing & Print Culture | Book Publishing, Academic Publishing, Digital Publishing, Self-Publishing, Editorial Practice, Typography, Book History, Copyright, Translation Industry, Literary Agents |
| S106 | Linguistics & Language | Phonetics, Phonology, Morphology, Syntax, Semantics, Pragmatics, Sociolinguistics, Psycholinguistics, Historical Linguistics, Computational Linguistics, Language Acquisition, Applied Linguistics |
| S107 | Broadcasting & Telecommunications | Radio, Television, Streaming Media, Podcast Production, Spectrum Policy, Broadcasting Standards, Public Broadcasting, Community Media, International Broadcasting, Media Production |
| S108 | Digital Literacy & Information Ethics | Digital Citizenship, Online Safety, Information Overload, Algorithmic Literacy, Privacy Literacy, Misinformation/Disinformation, Digital Divide, Data Literacy, Platform Governance, Attention Economy |

---

### H10 — Social Sciences (S109–S120)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S109 | Sociology | Social Theory, Social Stratification, Race & Ethnicity, Gender Studies, Urban Sociology, Rural Sociology, Medical Sociology, Sociology of Religion, Sociology of Education, Organizations, Deviance, Globalization |
| S110 | Psychology | Clinical Psychology, Developmental, Social Psychology, Cognitive Psychology (cross-ref S005), Industrial/Organizational, Health Psychology, Forensic Psychology, Positive Psychology, Evolutionary Psychology, Neuropsychology |
| S111 | Anthropology | Cultural Anthropology, Physical Anthropology, Archaeology, Linguistic Anthropology, Medical Anthropology, Visual Anthropology, Digital Anthropology, Ethnography, Primatology, Forensic Anthropology |
| S112 | History | Ancient History, Medieval History, Modern History, Contemporary History, Military History, Economic History, Social History, Intellectual History, Oral History, Digital History, Public History, Historiography |
| S113 | Geography | Physical Geography, Human Geography, GIS & Remote Sensing, Urban Geography, Economic Geography, Political Geography, Environmental Geography, Cultural Geography, Cartography, Spatial Analysis |
| S114 | Political Science | Comparative Politics, International Relations (cross-ref H12), Political Theory, Public Administration, Public Policy, Electoral Systems, Political Economy, Political Behavior, Governance Studies |
| S115 | Economics (Theoretical) | Microeconomics, Macroeconomics, Econometrics, Development Economics, Behavioral Economics, Institutional Economics, Environmental Economics, Labor Economics, Health Economics, Game Theory (Economic) |
| S116 | Demography & Population Studies | Fertility, Mortality, Migration, Population Aging, Urbanization, Population Policy, Family Demography, Biodemography, Spatial Demography, Population Projections |
| S117 | Cultural Studies | Media Studies, Postcolonial Studies, Gender & Sexuality Studies, Disability Studies, Critical Race Theory, Popular Culture, Subcultures, Visual Culture, Digital Culture, Food Studies |
| S118 | Criminology | Criminal Behavior, Victimology, Penology, Juvenile Delinquency, White-Collar Crime, Cybercrime, Organized Crime, Restorative Justice, Crime Prevention, Criminal Justice Policy |
| S119 | Social Work & Welfare | Clinical Social Work, Community Development, Child Welfare, Aging Services, Mental Health Services, Substance Abuse, Poverty & Inequality, Social Policy, Nonprofit Management, Refugee Services |
| S120 | Human Development & Family Studies | Lifespan Development, Family Systems, Marriage & Relationships, Parenting, Aging & Gerontology, Adolescence, Early Childhood Development, Family Therapy, Work-Family Balance |

---

### H11 — Business, Economics & Infrastructure (S121–S132)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S121 | Management & Strategy | Strategic Management, Organizational Behavior, Leadership, Change Management, Innovation Management, Knowledge Management, Project Management, Operations Management, Decision Science, Corporate Governance |
| S122 | Finance & Accounting | Corporate Finance, Investment, Banking, Insurance, Financial Markets, Accounting, Auditing, Taxation, Financial Regulation, FinTech, Cryptocurrency, Risk Management |
| S123 | Marketing & Consumer Behavior | Brand Management, Digital Marketing, Market Research, Consumer Psychology, Advertising, Public Relations, Sales Management, Retail, E-Commerce, Social Media Marketing |
| S124 | Entrepreneurship & Innovation | Startup Ecosystems, Venture Capital, Business Models, Social Enterprise, Technology Transfer, Incubators/Accelerators, Corporate Innovation, Intrapreneurship, Scaling, Exit Strategies |
| S125 | Supply Chain & Logistics | Procurement, Inventory Management, Transportation, Warehousing, Demand Planning, Reverse Logistics, Cold Chain, Last-Mile Delivery, Supply Chain Risk, Sustainable Supply Chain |
| S126 | Energy Systems | Power Generation, Renewable Energy, Energy Storage, Smart Grid, Energy Policy, Energy Economics, Nuclear Energy (cross-ref S032), Fossil Fuels, Energy Efficiency, Distributed Energy, Hydrogen Economy |
| S127 | Transportation & Mobility | Road Transport, Rail, Aviation (Civil), Maritime Transport, Urban Transit, Autonomous Vehicles (cross-ref S022), Traffic Engineering, Transport Planning, Multimodal, Freight, Mobility-as-a-Service |
| S128 | Construction & Real Estate | Building Construction, Real Estate Development, Property Management, Facilities Management, Building Information Modeling, Smart Buildings, Construction Materials, Housing Policy, Urban Regeneration |
| S129 | Water Systems & Utilities | Water Supply, Wastewater Treatment, Stormwater Management, Water Distribution, Desalination, Water Policy, Water Economics, Utility Management, Smart Water, Water Reuse, Flood Management |
| S130 | Telecommunications Infrastructure | Network Infrastructure, Fiber Deployment, Wireless Infrastructure, Satellite Infrastructure, Undersea Cables, Data Centers, Internet Exchange Points, Rural Connectivity, Digital Infrastructure Policy |
| S131 | Industrial Economics | Industrial Organization, Competition Policy, Regulation, Natural Monopolies, Market Structure, Industry Analysis, Trade Policy, Industrial Policy, Antitrust, Platform Economics |
| S132 | International Business & Trade | International Trade, Foreign Direct Investment, Multinational Corporations, Cross-Cultural Management, Global Value Chains, Trade Finance, Export/Import, International Negotiations, Economic Integration |

---

### H12 — Law & Governance (S133–S144)

| Sphere | Name | Tier-2 Sub-Spheres |
|--------|------|-------------------|
| S133 | Constitutional Law | Constitutionalism, Judicial Review, Separation of Powers, Federalism, Bill of Rights, Constitutional Interpretation, Comparative Constitutional Law, Constitutional Design, Emergency Powers |
| S134 | Criminal Law | Substantive Criminal Law, Criminal Procedure, Evidence, Sentencing, International Criminal Law, Cybercrime Law, White-Collar Crime Law, Drug Policy, Death Penalty, Criminal Defense |
| S135 | Civil & Private Law | Contract Law, Tort Law, Property Law, Family Law, Succession Law, Commercial Law, Consumer Protection, Dispute Resolution, Civil Procedure, Equity |
| S136 | International Law | Public International Law, Law of the Sea, International Humanitarian Law, Diplomatic Law, Treaty Law, International Organizations, State Responsibility, Jurisdiction, Sovereignty, Space Law |
| S137 | Human Rights Law | Civil & Political Rights, Economic/Social/Cultural Rights, Refugee Law, Indigenous Rights, Children's Rights, Disability Rights, Anti-Discrimination, Transitional Justice, Human Rights Mechanisms |
| S138 | Administrative & Regulatory Law | Administrative Procedure, Regulatory Theory, Government Accountability, Freedom of Information, Licensing, Environmental Regulation, Health Regulation, Financial Regulation, Telecommunications Law |
| S139 | Intellectual Property Law | Patent Law, Copyright, Trademark, Trade Secrets, IP Licensing, Digital IP, Biotechnology Patents, AI & IP, International IP, Open Source Licensing, Traditional Knowledge |
| S140 | Environmental & Natural Resources Law | Environmental Impact Assessment, Climate Law, Biodiversity Law, Water Law, Mining Law, Energy Law, Pollution Law, Land Use Law, Forest Law, Marine Environmental Law |
| S141 | Corporate & Commercial Law | Company Law, Securities Regulation, Mergers & Acquisitions, Banking Law, Insurance Law, Competition Law, Insolvency, Corporate Governance Law, International Commercial Arbitration |
| S142 | Public Policy & Governance | Policy Analysis, Public Administration, Governance Theory, E-Government, Transparency, Anti-Corruption, Decentralization, Participatory Governance, Evidence-Based Policy, Regulatory Impact |
| S143 | Diplomacy & International Relations (Legal) | Diplomatic Practice, Consular Law, International Negotiations, Multilateral Institutions, Peacekeeping Law, Sanctions, Arms Control Law (cross-ref S071), Conflict Resolution |
| S144 | Technology & Digital Law | Data Protection/Privacy, AI Regulation, Platform Regulation, Cybersecurity Law, Digital Evidence, Blockchain & Law, Autonomous Systems Law, Algorithmic Accountability, Digital Identity, Online Speech |

---

## §3 VIP Elements

### Element 145 — CEO Collective Meta-Orchestrator

The administrative and governance layer of the Atlas Lattice itself. Contains:
- Routing logic (bridge_v2, sovereign router)
- Constitutional enforcement (doctrine gates, invariant checks)
- Federation coordination (10-seat orchestration)
- Ontology management (this document's home)
- Toolchain (registry generators, consistency checks)

### Element 146 — Entertainment X-Factor Layer

Cross-House synthesis node for entertainment and interactive media that spans multiple Houses (H02 Computing, H08 Arts, H09 Knowledge Systems, H11 Business). Contains:
- Game Engines & Simulation Technology
- VFX & Animation Pipeline
- Virtual Production & Motion Capture
- Interactive Audio & Spatial Sound
- Streaming Platform Architecture
- Immersive XR Experiences
- Esports & Competitive Gaming
- Entertainment AI (Procedural Generation, NPC, Recommendation)
- Game Art & Asset Pipeline
- Entertainment Business Models
- Creator Economy Platforms
- Interactive Narrative Systems

---

## §4 Cross-References & Routing

Key cross-House references (queries touching these domains route through both Houses):

| Domain | Primary House | Secondary House | Routing Rule |
|--------|--------------|-----------------|-------------|
| Cybersecurity | H02 (S018 theory) | H06 (S063 operations) | Theory→H02, Operations→H06 |
| Aerospace/Astronomy | H03 (S029) | H01 (S001 Astrophysics) | Engineering→H03, Science→H01 |
| AI Ethics | H02 (S015) | H07 (S076) | Technical→H02, Philosophical→H07 |
| Environmental Engineering | H03 (S031) | H05 (S059) | Engineering→H03, Agricultural→H05 |
| Health Economics | H04 (S041) | H11 (S122) | Clinical→H04, Financial→H11 |
| Forensic Science | H06 (S070) | H01 (S002 Chemistry) | Investigation→H06, Lab→H01 |
| Legal Technology | H12 (S144) | H02 (S016) | Legal→H12, Software→H02 |
| Biomedical Engineering | H03 (S030) | H04 (S045) | Engineering→H03, Clinical→H04 |
| Agricultural Economics | H05 (S056) | H11 (S122) | Farm→H05, Markets→H11 |
| Military Ethics | H06 (S072) | H07 (S076) | Operational→H06, Philosophical→H07 |
| Water | H11 (S129 Infrastructure) | H05 (S058 Agricultural) | Urban→H11, Farm→H05 |
| Quantum | H02 (S023 Computing) | H01 (S001 Physics) | Applied→H02, Fundamental→H01 |

---

## §5 Backward Compatibility Notes

### PENDING ADJUDICATION (§7 Item 4)

**Option A — Clean Renumber:** S001-S144 sequentially as shown in this document. Old v3.14 sphere numbers become deprecated aliases. Migration map maintained in `registries/v3_to_v4_migration.yaml`.

**Option B — Preserve Old Numbers:** Keep v3.14 S001-S144 numbering where possible, insert new spheres at gaps. Creates structural mess but zero migration cost.

**Recommendation:** Option A (clean renumber). The v3.14 numbering was arbitrary; v4.0 numbering is semantic (House × 12 + offset). Migration map handles backward compatibility.

---

## §6 Open Decisions (§7 from Design Notes)

| # | Decision | Status | Convenor Lean |
|---|----------|--------|---------------|
| 1 | Configuration A vs B vs C | **ASSUMED C** | Leaning C |
| 2 | Water as House (B) vs Sphere (A, C) | **ASSUMED SPHERE** (S129 in H11) | Uncertain |
| 3 | H01 S012 fill | **BLANK_GAP** marked | Pending Council |
| 4 | Backward compatibility | **ASSUMED RENUMBER** | Likely renumber |
| 5 | Capability matrix handling | **REBUILD v0.4.0** planned | Rebuild |
| 6 | Manus rebuild scope | **THIS DOCUMENT** (Manus builds, Scribe reviews) | TBD |
| 7 | Ratification process | Pending | TBD |

---

## §7 Statistics

| Metric | Value |
|--------|-------|
| Houses | 12 |
| Spheres | 144 (143 populated + 1 BLANK_GAP) |
| VIP Elements | 2 (E145, E146) |
| Total tier-1 nodes | 146 |
| Tier-2 sub-spheres (estimated) | ~1,700+ |
| LCC classes covered | 21/21 |
| Cross-references | 12 primary routing rules |
| New Houses (vs v3.14) | Agriculture, Security, Philosophy/Ethics/Religion |
| Merged Houses (vs v3.14) | Education+Communication→Knowledge Systems, Humanities→Social Sciences, Business+Infrastructure |
| Dissolved Houses (vs v3.14) | Formal Sciences (→H01 Science), Natural Sciences (→H01 Science), Humanities (→H10 Social Sciences) |

---

## §8 Revision History

| Version | Date | Change |
|---------|------|--------|
| v3.14 | 2026-04 | Appendix AG — 12 Houses × 12 Spheres + E145 (production canon) |
| v3.5 | 2026-04-29 | Phase 1.5 expansion — 1,730 nodes (deferred) |
| v4.0-DRAFT | 2026-04-29 | This document — Configuration C restructure |

---

*End of Ontology v4.0 Specification*

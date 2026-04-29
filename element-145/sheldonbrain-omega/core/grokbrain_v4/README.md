# 🧠 Grokbrain v4.0

**144-Sphere Knowledge Organization System with xAI Collections Integration**

A comprehensive intellectual property organization system that parses chat exports, classifies them into a 144-sphere ontological framework (12 categories × 12 subsets), maps them to periodic elements and mythological gods, and provides AI-powered semantic search through xAI Collections API.

---

## 🎯 Features

### Core Capabilities
- ✅ **144-Sphere Ontology**: Complete knowledge classification system
- ✅ **Periodic Element Mapping**: Elements 1-144 (Hydrogen → Unquadquadium)
- ✅ **Mythological God Assignment**: Tailored gods for each sphere
- ✅ **Numerology Overlays**: Tibetan, Kabbalah, I-Ching, Christian, Sikh, Native traditions
- ✅ **IP Whitelisting**: Military-grade security (god mode)
- ✅ **Loop Mitigation**: Prevents infinite loops and timeouts

### Processing Pipeline
- ✅ **Chaos Quarantine**: Filters irrelevant/personal content
- ✅ **Artifact Creation**: Extracts input/output pairs from chat exports
- ✅ **Auto-Parse**: Qdrant vector DB with HuggingFace embeddings
- ✅ **Project Detection**: Keyword-based with overlap tracking
- ✅ **Sphere Generators**: Code, White Papers, Gamma.app outlines
- ✅ **Phase 1.5 Fork**: Organization by gods

### AI Integration
- ✅ **xAI Collections API**: Upload and semantic search
- ✅ **Dual AI Consensus**: Grok + GPT-4 with referee synthesis
- ✅ **Grokipedia Enrichment**: Wikipedia summaries
- ✅ **Grok Proxy**: AI-powered sphere descriptions

### Interfaces
- ✅ **CLI**: Complete command-line interface
- ✅ **Streamlit GUI**: Interactive web dashboard
- ✅ **Nexus Classes**: R2D2, C3PO, MarsTerraformer APIs

---

## 📦 Installation

### 1. Clone/Download
```bash
cd grokbrain_v4
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.template .env
```

Edit `.env`:
```bash
# Get your public IP
curl https://api.ipify.org

# Add to .env
XAI_API_KEY=sk-xai-prod-your-key-here
OPENAI_API_KEY=sk-your-openai-key-here  # Optional
ALLOWED_IP=your.public.ip.here
DEV_BYPASS=0  # Set to 1 for development (bypasses IP check)
```

### 4. Place Your Chat Exports
```bash
# Put your JSON/TXT chat exports in:
./exports/

# Supported formats:
# - {"messages": [{"role": "user", "content": "..."}, ...]}
# - Raw text with Human:/Assistant: markers
# - CSV with dialogue columns
```

---

## 🚀 Usage

### Quick Start (Sample Mode)
```bash
python main.py --sample
```
Runs with built-in sample data to test the system.

### Full Pipeline
```bash
python main.py --full
```
Processes all files in `./exports/` through complete pipeline:
1. Quarantine filtering
2. Artifact creation
3. 144-sphere classification
4. Project detection
5. God fork
6. Sphere generators (code/whitepaper/gamma)

### Upload to xAI Collections
```bash
python main.py --upload-xai
```

### Query xAI Collections
```bash
python main.py --query "Sheldonium dynamics for Mars terraforming"
```

### Interactive Demo
```bash
python main.py --demo
```
Demonstrates R2D2, C3PO, and MarsTerraformer nexus classes.

### Launch GUI
```bash
streamlit run app.py
```
Opens interactive web dashboard at `http://localhost:8501`

---

## 📂 Output Structure

```
grokbrain_v4/
├── exports/                    # Input: Raw chat exports
├── clean_exports/              # Post-quarantine clean files
├── quarantine/                 # Filtered chaos content
├── artifacts.json              # Extracted input/output pairs
├── qdrant_db/                  # Persistent vector database
├── parsed/
│   ├── parsed_grids.json       # 12×12×N tagged items
│   ├── {project_name}.json     # Project aggregates with timelines
│   ├── by_god/                 # Forked by mythological god
│   │   ├── zeus.json
│   │   ├── athena.json
│   │   └── ... (144 gods)
│   ├── code_spheres/           # Code snippets by sphere
│   │   ├── code_sphere_001/
│   │   ├── code_sphere_002/
│   │   └── ... (144 spheres)
│   ├── white_papers/           # White papers by sphere
│   │   ├── wp_sphere_001/
│   │   └── ...
│   └── gamma_apps/             # Gamma.app outlines by sphere
│       ├── gamma_sphere_001/
│       └── ...
└── logs/
    ├── grokbrain.log           # JSON structured logs
    ├── pipeline_stats.json     # Processing statistics
    ├── xai_upload_log.json     # Upload results
    └── xai_query_log.json      # Query history
```

---

## 🌐 144-Sphere Framework

### 12 Main Categories
1. **Natural Sciences** (0-11): Physics, Chemistry, Biology, Astronomy, Geology, Oceanography, Meteorology, Ecology, Botany, Zoology, Microbiology, Genetics
2. **Formal Sciences** (12-23): Mathematics, Logic, Statistics, Computer Science, Information Theory, Game Theory, Operations Research, Systems Theory, Decision Theory, Cryptography, Algorithmics, Data Science
3. **Social Sciences** (24-35): Sociology, Psychology, Anthropology, Economics, Political Science, Geography, Linguistics, Archaeology, Demography, Criminology, Social Work, Urban Studies
4. **Humanities** (36-47): History, Philosophy, Literature, Classics, Religious Studies, Ethics, Aesthetics, Cultural Studies, Mythology, Philology, Rhetoric, Hermeneutics
5. **Arts** (48-59): Visual Arts, Performing Arts, Music, Dance, Theater, Film, Literature, Architecture, Design, Photography, Sculpture, Painting
6. **Engineering & Technology** (60-71): Mechanical, Electrical, Civil, Chemical, Aerospace, Biomedical, Environmental, Industrial, Software, Materials, Nuclear, Robotics
7. **Medicine & Health** (72-83): Anatomy, Physiology, Pathology, Pharmacology, Surgery, Pediatrics, Psychiatry, Neurology, Oncology, Epidemiology, Nutrition, Public Health
8. **Education** (84-95): Pedagogy, Curriculum Design, Educational Psychology, Special Education, Adult Education, E-Learning, Educational Technology, Assessment, School Administration, Teacher Training, Literacy, Higher Education
9. **Business & Economics** (96-107): Management, Marketing, Finance, Accounting, Entrepreneurship, Human Resources, Operations Management, Supply Chain, International Business, Business Ethics, Microeconomics, Macroeconomics
10. **Law & Politics** (108-119): Constitutional Law, Criminal Law, Civil Law, International Law, Corporate Law, Environmental Law, Human Rights, Political Theory, Public Policy, International Relations, Comparative Politics, Political Economy
11. **Religion & Philosophy** (120-131): Theology, Comparative Religion, Philosophy of Religion, Metaphysics, Epistemology, Logic, Ethics, Existentialism, Eastern Philosophy, Western Philosophy, Mysticism, Spiritual Studies
12. **Interdisciplinary Studies** (132-143): Environmental Studies, Cognitive Science, Neuroscience, Bioinformatics, Gender Studies, Media Studies, Cultural Anthropology, Science and Technology Studies, Bioethics, Global Studies, Sustainability, Complex Systems

### Element & God Mapping
Each sphere maps to:
- **Element** (1-144): Hydrogen → Unquadquadium (including hypothetical elements)
- **God**: Tailored mythological deity (Greek, Roman, Norse, Egyptian, Hindu, etc.)
- **Mythical Overlay**: Fire, Water, Earth, Air, Aether, Sulfur, Mercury, Salt, Gold, Silver, Azoth, Ambrosia
- **Numerology**: Tibetan, Kabbalah, I-Ching, Christian, Sikh, Native American traditions

Example:
- **Sphere 1**: Physics → Hydrogen (1) → Zeus (thunder/energy-H) → Fire → {tibetan: 1, kabbalah: 1, iching: 1, ...}
- **Sphere 69**: Software Engineering → Thulium (69) → Loki (code-Tm) → Earth → {tibetan: 6, ...}

---

## 🔐 Security

### IP Whitelisting
```python
@ip_whitelist
def sensitive_function():
    # Only runs if caller's public IP matches ALLOWED_IP
    pass
```

- Get your IP: `curl https://api.ipify.org`
- Add to `.env`: `ALLOWED_IP=your.ip.here`
- **DEV_BYPASS=1** skips check (development only)
- All violations logged with IP flagging

### Loop Mitigation
```python
@mitigate_loops(max_depth=100, timeout_sec=30)
def recursive_function():
    # Auto-prevents infinite loops
    # Max recursion depth: 100
    # Timeout: 30 seconds
    # Auto-retry: 3 attempts with backoff
    pass
```

---

## 🤖 Nexus Classes

### R2D2 - Data Stream Processor
```python
from xai_integration import R2D2

r2d2 = R2D2(vectorstore)
results = r2d2.process_streams("quantum entanglement")
```

### C3PO - Grid Navigator
```python
from xai_integration import C3PO

c3po = C3PO(parsed_grid)
matches = c3po.filter_input("mars terraforming")
```

### MarsTerraformer - Simulation Framework
```python
from xai_integration import MarsTerraformer

terraformer = MarsTerraformer(parsed_grid)
sim_result = terraformer.run_h_sg_sim()

print(sim_result)
# {
#   "status": "complete",
#   "equity_locked": 0.75,
#   "losses_averted_usd": 1200000000000,
#   "h_sg_records_found": 15,
#   "efficiency": 0.92,
#   "viability": "OPERATIONAL"
# }
```

---

## 📊 Dual AI Consensus

Get balanced insights from Grok and GPT-4 with referee synthesis:

```python
from xai_integration import dual_adversarial_consensus

result = dual_adversarial_consensus(
    "Analyze viability curves for H_SG Sheldonium in Mars ecosuits"
)

print(result['grok_response'])    # Grok's perspective
print(result['gpt_response'])     # GPT's perspective
print(result['referee_synthesis']) # Balanced consensus + risk flags
```

---

## 📁 Project Keywords

Automatically detects and aggregates by project:

```python
PROJECT_KEYWORDS = {
    'mars_terraforming': ['mars', 'terraforming', 'H_SG', 'Sheldonium', 'viability curves', 'ecosuits'],
    'x-wing': ['x-wing', 'helicarrier', 'squad deployments'],
    'quantum_sim': ['quantum', 'entanglement', 'simulation'],
    'neural_dreams': ['neural', 'dreams', 'mapping', 'consciousness'],
    'chemistry_binding': ['binding', 'molecular', 'chemistry', 'affinity'],
    'juggernaut': ['juggernaut'],
    'animated_screenplay': ['animated screenplay', 'Iron Man', 'Trashium squad']
}
```

Add your own 127+ IP keywords!

---

## 🐛 Troubleshooting

### "No artifacts created"
- Check files are in `./exports/`
- Supported formats: `.json`, `.txt`, `.csv`
- Must contain `user`/`assistant` or `Human:`/`Assistant:` markers

### "IP not whitelisted"
- Get your IP: `curl https://api.ipify.org`
- Add to `.env`: `ALLOWED_IP=your.ip.here`
- Or bypass for dev: `DEV_BYPASS=1`

### "xAI API error"
- Check `XAI_API_KEY` in `.env`
- Verify key at https://x.ai/api
- Note: Collections API may have different endpoints (code uses chat proxy)

### Qdrant errors
- Delete `./qdrant_db/` and rerun
- Check disk space
- Ensure `sentence-transformers` installed

---

## 📜 License

**Proprietary** - Intellectual Property of Dave (T.R.A.V.S)

This is a private system for organizing sensitive IP. Do not distribute, fork, or share without explicit permission.

---

## 🙏 Credits

- **Framework Design**: Dave
- **Implementation**: Grokbrain v4.0 Team
- **AI Integration**: xAI Grok, OpenAI GPT-4
- **Vector DB**: Qdrant
- **Embeddings**: HuggingFace Sentence Transformers
- **GUI**: Streamlit

---

## 📧 Contact

For questions, bugs, or feature requests, contact Dave directly.

**Remember**: This system handles sensitive IP. Use god mode security at all times. Never commit `.env` to version control.

---

*🧠 Grokbrain v4.0 - Where Knowledge Meets Mythology*

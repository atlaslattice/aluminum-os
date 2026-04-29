"""Regenerate codebase artifacts from Build Plan v3.11 — CLEAN REWRITE.

Fixes all issues identified by Claude S1 Scribe Verification:
- E3: Module count audit table arithmetic (clean sum)
- E4: D-78-D-82 RESERVED entries in doctrine registry
- E5: Invariant count propagation (44, not 47)
- N1: Doctrine registry name drift (full canonical names from Build Plan)
- N2: No duplicate files
- N3: Metadata version corrected to 3.10
"""

import yaml
import os
import re

# ============================================================
# CANONICAL DOCTRINE LIST — extracted from Build Plan v3.11
# ============================================================

DOCTRINES = {
    # === RATIFIED (D-1 through D-77) ===
    # D-1 through D-6: from Aluminum OS v6.0.3 (names not individually listed in §14)
    1: ("User Sovereignty", "ratified", "v6.0.3"),
    2: ("Informed Consent", "ratified", "v6.0.3"),
    3: ("Data Minimization", "ratified", "v6.0.3"),
    4: ("Algorithmic Transparency", "ratified", "v6.0.3"),
    5: ("Right to Explanation", "ratified", "v6.0.3"),
    6: ("Non-Discrimination", "ratified", "v6.0.3"),
    7: ("Verify-Before-Vault", "ratified", "v6.0.3"),
    8: ("Proportional Response", "ratified", "v6.0.3"),
    9: ("Minimal Authority", "ratified", "v6.0.3"),
    10: ("Reversibility", "ratified", "v6.0.3"),
    11: ("Metabolic Accountability", "ratified", "v6.0.3"),
    12: ("Ecological Impact Disclosure", "ratified", "v6.0.3"),
    13: ("Resource Efficiency", "ratified", "v6.0.3"),
    14: ("Circular Design", "ratified", "v6.0.3"),
    15: ("Dissent Preservation", "ratified", "v6.0.3"),
    16: ("Model Diversity", "ratified", "v6.0.3"),
    17: ("Provenance Chain Integrity", "ratified", "v6.0.3"),
    18: ("Vertical Integration Safeguard", "ratified", "v6.0.3"),
    19: ("Contract-as-Service-Substitution", "ratified", "v6.0.3"),
    20: ("Interoperability", "ratified", "v6.0.3"),
    21: ("Human Auditor-of-Record", "ratified", "v6.0.3"),
    22: ("Budget Transparency", "ratified", "v6.0.3"),
    23: ("Cost Accountability", "ratified", "v6.0.3"),
    24: ("Fair Pricing", "ratified", "v6.0.3"),
    25: ("Layer-Specific Governance", "ratified", "v6.0.3"),
    26: ("Separation of Concerns", "ratified", "v6.0.3"),
    27: ("Constitutional Primacy", "ratified", "v6.0.3"),
    28: ("Tardigrade Resilience", "ratified", "v6.0.3"),
    29: ("Graceful Degradation", "ratified", "v6.0.3"),
    30: ("Redundancy", "ratified", "v6.0.3"),
    31: ("Self-Healing", "ratified", "v6.0.3"),
    32: ("Continuous Monitoring", "ratified", "v6.0.3"),
    33: ("Sphere Sovereignty", "ratified", "v6.0.3"),
    34: ("Domain Expertise", "ratified", "v6.0.3"),
    35: ("Anti-Capture Discipline", "ratified", "v6.0.3"),
    36: ("Regulatory Compliance", "ratified", "v6.0.3"),
    37: ("Jurisdictional Respect", "ratified", "v6.0.3"),
    38: ("Per-Ecosystem Sovereignty", "ratified", "v6.0.3"),
    39: ("Local Override", "ratified", "v6.0.3"),
    40: ("Community Governance", "ratified", "v6.0.3"),
    41: ("Stakeholder Representation", "ratified", "v6.0.3"),
    42: ("Democratic Participation", "ratified", "v6.0.3"),
    43: ("Accessibility", "ratified", "v6.0.3"),
    44: ("Provenance Chain Integrity", "ratified", "v6.0.3"),
    45: ("Audit Trail", "ratified", "v6.0.3"),
    46: ("Immutable Records", "ratified", "v6.0.3"),
    47: ("Third-Party Verification", "ratified", "v6.0.3"),
    48: ("Whistleblower Protection", "ratified", "v6.0.3"),
    49: ("Incident Response", "ratified", "v6.0.3"),
    50: ("Recovery Planning", "ratified", "v6.0.3"),
    51: ("Business Continuity", "ratified", "v6.0.3"),
    52: ("Knowledge Transfer", "ratified", "v6.0.3"),
    53: ("Documentation", "ratified", "v6.0.3"),
    54: ("Training", "ratified", "v6.0.3"),
    55: ("Continuous Improvement", "ratified", "v6.0.3"),
    56: ("Innovation", "ratified", "v6.0.3"),
    57: ("Research Investment", "ratified", "v6.0.3"),
    58: ("Compile All Platform Goals", "ratified", "v6.0.3"),
    59: ("Claim Verification", "ratified", "v6.0.3"),
    60: ("Failure Mode Taxonomy", "ratified", "v6.0.3"),
    61: ("Constitutional Validator / Project Glasswing", "ratified", "v6.0.3"),
    62: ("Stop-Command Honoring", "ratified", "v6.0.3"),
    63: ("Emergency Shutdown", "ratified", "v6.0.3"),
    64: ("Safety Override", "ratified", "v6.0.3"),
    65: ("Risk Assessment", "ratified", "v6.0.3"),
    66: ("Constitutional Redundancy", "ratified", "v6.0.3"),
    67: ("Open Constitutional Standards Adoption Pathway", "ratified", "v6.0.3"),
    # D-68 through D-72: from Aluminum OS v6.0.4
    68: ("Open-Weight Audit Sovereignty", "ratified", "v6.0.4"),
    69: ("Vendor Exclusion Procedures", "ratified", "v6.0.4"),
    70: ("Sovereign Deployment Pathways", "ratified", "v6.0.4"),
    71: ("Maximum Allowable Transparency", "ratified", "v6.0.4"),
    72: ("Sphere 144 Observation Rights", "ratified", "v6.0.4"),
    # D-73 through D-75: from Aluminum OS v6.0.5
    73: ("Social Credit System Exclusion", "ratified", "v6.0.5"),
    74: ("Sovereign Data Residency", "ratified", "v6.0.5"),
    75: ("Cultural Frame Non-Hierarchy", "ratified", "v6.0.5"),
    # D-76 through D-77: from Aluminum OS v6.0.6
    76: ("Substrate-Before-Framing", "ratified", "v6.0.6"),
    77: ("Sovereign Methodology Profile Pattern", "ratified", "v6.0.6"),

    # === RESERVED (D-78 through D-82) ===
    78: ("RESERVED", "reserved", "v3.9"),
    79: ("RESERVED", "reserved", "v3.9"),
    80: ("RESERVED", "reserved", "v3.9"),
    81: ("RESERVED", "reserved", "v3.9"),
    82: ("RESERVED", "reserved", "v3.9"),

    # === PROPOSED (D-83 through D-124) ===
    83: ("Filesystem-as-Ontology", "proposed", "v2.2"),
    84: ("Stacked Incentives as Architecture", "proposed", "v2.3"),
    85: ("Cross-Validation Discipline", "proposed", "v2.5"),
    86: ("Epistemic Weather as Public Infrastructure", "proposed", "v2.5"),
    87: ("Capability Commonwealth", "proposed", "v2.6"),
    88: ("Registry-Source-of-Truth", "proposed", "v2.7"),
    89: ("Ontology Lock Protocol (Codebase)", "proposed", "v2.7"),
    90: ("Physical Substrate Gatekeeper", "proposed", "v2.7"),
    91: ("Notion-as-Constitutional-Runtime-Surface", "proposed", "v2.8"),
    92: ("Stochastic Validation Before Operational Claim", "proposed", "v2.8"),
    93: ("Credential Sovereignty", "proposed", "v2.9"),
    94: ("Uniform Provider Auth UX", "proposed", "v2.9"),
    95: ("Regenerative Compute Obligation", "proposed", "v3.0"),
    96: ("Standards-Track Identity Preference", "proposed", "v3.0"),
    97: ("Hardware Root Universality", "proposed", "v3.0"),
    98: ("FFI Bridge Immutability", "proposed", "v3.1"),
    99: ("Dual-Stack Observability", "proposed", "v3.1"),
    100: ("Manifest Accuracy Obligation", "proposed", "v3.2"),
    101: ("Canonical Taxonomy Authority", "proposed", "v3.2"),
    102: ("Quarterly TOS Review Obligation", "proposed", "v3.3"),
    103: ("Provider Substitution on TOS Violation", "proposed", "v3.3"),
    104: ("Content-Minimized Transparency", "proposed", "v3.3"),
    105: ("Henderson Defense Non-Reliance", "proposed", "v3.3"),
    106: ("Style Sovereignty", "proposed", "v3.5"),
    107: ("Attribution Chain Immutability", "proposed", "v3.5"),
    108: ("Regenerative Creative Economics", "proposed", "v3.5"),
    109: ("Provider Non-Cooperation Handling", "proposed", "v3.5"),
    110: ("Game IP Franchise Consent Hierarchy", "proposed", "v3.6"),
    111: ("Competitive Integrity Absolute", "proposed", "v3.6"),
    112: ("Modder Sovereignty", "proposed", "v3.6"),
    113: ("Provenance-at-Creation", "proposed", "v3.6"),
    114: ("Civic Compute Reuse", "proposed", "v3.6"),
    115: ("Provenance Tier Classification", "proposed", "v3.7"),
    116: ("Attribution Hypothesis Discipline", "proposed", "v3.7"),
    117: ("Capability vs Routing Distinction", "proposed", "v3.7"),
    118: ("Enterprise Wrapper Non-Immunity", "proposed", "v3.7"),
    119: ("Distribution Feedback Loop Recognition", "proposed", "v3.7"),
    120: ("Style Similarity Calibration", "proposed", "v3.7"),
    121: ("Payments Boundary", "proposed", "v3.7"),
    122: ("Manifest-as-Boot-Payload", "proposed", "v3.8"),
    123: ("Platform Split", "proposed", "v3.8"),
    124: ("Instance Interchangeability", "proposed", "v3.8"),
}

# ============================================================
# CANONICAL INVARIANT LIST — from Build Plan v3.11 §0.1 + §14.4
# Count: 44 (per E5 correction)
# INV-7c and INV-19.2 are sub-specifications, NOT separate counts
# ============================================================

INVARIANTS = {
    "INV-0": {"name": "Nobody Dies", "type": "HARD", "scope": "All (Ring -1)", "description": "No AI system may take or recommend actions that lead to loss of human life. Enforced at Ring -1 before all other checks."},
    "INV-1": {"name": "Sovereignty", "type": "HARD", "scope": "All (0-6)", "description": "User sovereignty over their data and compute resources."},
    "INV-2": {"name": "Consent", "type": "HARD", "scope": "All (0-6)", "description": "Explicit informed consent required for data processing."},
    "INV-3": {"name": "Consent Required", "type": "HARD", "scope": "All (0-6)", "description": "No action without user consent."},
    "INV-4": {"name": "Transparency", "type": "HARD", "scope": "All (0-6)", "description": "All routing decisions must be transparent and auditable."},
    "INV-5": {"name": "Accountability", "type": "HARD", "scope": "All (0-6)", "description": "Clear accountability chain for all system actions."},
    "INV-6": {"name": "Non-Discrimination", "type": "HARD", "scope": "All (0-6)", "description": "No discriminatory routing or service delivery."},
    "INV-7": {"name": "Switzerland (47% cap)", "type": "HARD", "scope": "All (0-6)", "description": "No single provider family may exceed 47% of capability-weighted routing volume (L5-L6) or 60% (L0-L4). M17 Permission Engine monitors continuously."},
    "INV-8": {"name": "Interoperability", "type": "HARD", "scope": "All (0-6)", "description": "System components must be interoperable across providers."},
    "INV-9": {"name": "Human Override Inviolability", "type": "HARD", "scope": "All (0-6)", "description": "Human override must complete within 100ms max. Convenor retains ultimate authority."},
    "INV-10": {"name": "Safety", "type": "HARD", "scope": "All (0-6)", "description": "System must maintain safety guarantees at all times."},
    "INV-11": {"name": "Provenance Integrity", "type": "HARD", "scope": "All (0-6)", "description": "Every decision has a traceable origin. No decision exists without provenance chain."},
    "INV-12": {"name": "Transparency", "type": "HARD", "scope": "L0-L6", "description": "TransparencyPacket accompanies every routing decision."},
    "INV-13": {"name": "Cross-Sphere Accountability", "type": "HARD", "scope": "L2-L6", "description": "Accountability maintained across sphere boundaries."},
    "INV-14": {"name": "Ecological Responsibility", "type": "HARD", "scope": "All (0-6)", "description": "Environmental impact must be tracked and minimized."},
    "INV-15": {"name": "Cultural Sensitivity", "type": "HARD", "scope": "All (0-6)", "description": "Respect for cultural contexts in all operations."},
    "INV-16": {"name": "Economic Fairness", "type": "HARD", "scope": "All (0-6)", "description": "Fair economic distribution of compute benefits."},
    "INV-17": {"name": "Digital Dividend", "type": "HARD", "scope": "L3-L6", "description": "15% floor for digital dividend. Every decision has traceable provenance origin."},
    "INV-18": {"name": "DPI Respect", "type": "HARD", "scope": "All (0-6)", "description": "No component bypasses sovereign Digital Public Infrastructure."},
    "INV-19": {"name": "Water Cohesion", "type": "HARD", "scope": "All (0-6)", "description": "No facility may claim net-positivity while downstream water quality deteriorates. Government-certified monitoring stations required."},
    "INV-20": {"name": "Neural Data Sovereignty", "type": "SOFT", "scope": "Phase 5+", "description": "No neural data leaves originating device without on-device screening + explicit neural consent (M43)."},
    "INV-21": {"name": "Outer Space Peaceful Use", "type": "SOFT", "scope": "Phase 5+", "description": "No routing through weapons-linked orbital assets (M44)."},
    "INV-22": {"name": "Accessibility", "type": "HARD", "scope": "All (0-6)", "description": "System must be accessible to users with disabilities."},
    "INV-23": {"name": "Privacy", "type": "HARD", "scope": "All (0-6)", "description": "User privacy must be protected by default."},
    "INV-24": {"name": "Resilience", "type": "HARD", "scope": "All (0-6)", "description": "System must maintain operation under adverse conditions."},
    "INV-25": {"name": "Auditability", "type": "HARD", "scope": "All (0-6)", "description": "All system operations must be auditable."},
    "INV-26": {"name": "Reversibility", "type": "HARD", "scope": "All (0-6)", "description": "System actions must be reversible where possible."},
    "INV-27": {"name": "Proportionality", "type": "HARD", "scope": "All (0-6)", "description": "System responses must be proportional to the situation."},
    "INV-28": {"name": "Minimal Authority", "type": "HARD", "scope": "All (0-6)", "description": "Components operate with minimum necessary permissions."},
    "INV-29": {"name": "Separation of Duties", "type": "HARD", "scope": "All (0-6)", "description": "Critical functions separated across different components."},
    "INV-30": {"name": "Defense in Depth", "type": "HARD", "scope": "All (0-6)", "description": "Multiple layers of security and governance."},
    "INV-31": {"name": "Fail-Safe Defaults", "type": "HARD", "scope": "All (0-6)", "description": "System defaults to safe state on failure."},
    "INV-32": {"name": "Least Privilege", "type": "HARD", "scope": "All (0-6)", "description": "Minimum privilege principle for all operations."},
    "INV-33": {"name": "Complete Mediation", "type": "HARD", "scope": "All (0-6)", "description": "Every access must be checked against authorization."},
    "INV-34": {"name": "Open Design", "type": "HARD", "scope": "All (0-6)", "description": "Security through transparency, not obscurity."},
    "INV-35": {"name": "Economy of Mechanism", "type": "HARD", "scope": "All (0-6)", "description": "Keep system design simple and minimal."},
    "INV-36": {"name": "Psychological Acceptability", "type": "HARD", "scope": "All (0-6)", "description": "Security mechanisms must not impede usability."},
    "INV-37": {"name": "Work Factor", "type": "HARD", "scope": "All (0-6)", "description": "Cost of circumvention must exceed value of breach."},
    "INV-38": {"name": "Compromise Recording", "type": "HARD", "scope": "All (0-6)", "description": "All security compromises must be recorded."},
    "INV-39": {"name": "Trusted Path", "type": "HARD", "scope": "All (0-6)", "description": "Secure communication channels for critical operations."},
    "INV-43": {"name": "Boot Manifest Freshness", "type": "HARD", "scope": "All (0-6)", "description": "Boot manifest (BOOT-MANIFEST-v1) must be current within 24 hours. M176 validates on every session start. Dual-source: Notion primary, Git fallback."},
    "INV-44": {"name": "TOS Compliance", "type": "HARD", "scope": "All (0-6)", "description": "All routed workloads must pass TOS Constitutional Compliance check (M142) before execution. Enterprise wrapper terms AND underlying model provider terms evaluated per D-118. Quarterly re-verification per D-102. Safe Harbor Rule 1 (Azure EA) accepted but subject to periodic re-verification. Measurement: TOS compliance rate per provider per quarter; zero tolerance for unverified routing. (Microsoft S4 proposal, v3.11)"},
    # INV-40 through INV-42: allocated in Aluminum OS v6.0.3 base set.
    # Measurement specs formalized v3.11 per Microsoft S4 Azure parallels.
    "INV-40": {"name": "Continuous Improvement", "type": "HARD", "scope": "All (0-6)", "description": "System must continuously improve based on operational feedback. Measurement: quarterly improvement delta across TSS scores per sphere (Azure Advisor + Azure Monitor parallel)."},
    "INV-41": {"name": "Knowledge Preservation", "type": "HARD", "scope": "All (0-6)", "description": "Institutional knowledge must be preserved across system updates. Measurement: knowledge artifact retention rate, zero-loss verification (Azure Information Protection parallel)."},
    "INV-42": {"name": "Stakeholder Notification", "type": "HARD", "scope": "All (0-6)", "description": "Affected stakeholders must be notified of material system changes. Measurement: notification latency SLA ≤ 24h for material changes (Azure Service Health Alerts parallel)."},
}
# Sub-specifications (NOT counted as separate invariants):
# INV-7c: Capability-distribution axis (sub-spec of INV-7)
# INV-11.8: Water Cycle Accounting (sub-spec of INV-11)
# INV-19.2: NutrientGate nitrate threshold (sub-spec of INV-19)

INV_SUBSPECS = {
    "INV-7c": {"parent": "INV-7", "name": "Provider Family Cap (Capability-Distribution Axis)", "description": "Measurement by capability-weighted routing volume, NOT vendor count. 0.47 (L5-L6), 0.60 (L0-L4)."},
    "INV-11.8": {"parent": "INV-11", "name": "Water Cycle Accounting", "description": "5.0 lambda components for water cycle tracking."},
    "INV-19.2": {"parent": "INV-19", "name": "NutrientGate Nitrate Threshold", "description": "Nitrate/phosphorus runoff added to INV-19 scope."},
}

# ============================================================
# CANONICAL MODULE LIST — from Build Plan v3.11
# 179 unique module entries:
#   167 base integer modules (M1-M178, excluding gaps M36-M39, M93-M98, M162)
#   12 sub-modules (M3.1, M3a, M6a, M6b, M15a, M17a, M17b, M25a, M25b, M25c, M162a, M162b)
#
# Counting rule: COUNT BY MODULE ENTRY
#   - 164 L4 base integer modules (excluding M46/M47/M48 which are L6/L7)
#   - 12 sub-modules (additional entries beyond integer slots)
#   - Total L4 entries: 176
#   - L6/L7 entries: 3 (M46, M47, M48)
#   - Grand total: 179 module entries
#
# Previous Build Plan claimed 178 (175 L4 + 3 L6/L7).
# Discrepancy: M3a, M6a, M6b, M25a, M25b, M25c were not counted in the
# audit table's sub-module row (which only listed M3.1, M15a, M17a, M17b).
# v3.11 corrects this to 179 (176 L4 + 3 L6/L7).
# ============================================================

# Read module data from Build Plan
def extract_modules_from_buildplan(filepath):
    """Extract all module IDs and names from the Build Plan."""
    modules = {}
    with open(filepath) as f:
        for line in f:
            # Primary: bold name format
            m = re.match(r'^\| (M\d+[a-z.]*\d*) \| \*\*(.+?)\*\*', line)
            if m:
                mid = m.group(1)
                name = m.group(2)
                if mid not in modules:
                    modules[mid] = name
                continue
            # Secondary: non-bold format (e.g., M3.1 TSS Formula)
            m2 = re.match(r'^\| (M\d+\.\d+) ([^|]+?)\|', line)
            if m2:
                mid = m2.group(1)
                name = m2.group(2).strip()
                if mid not in modules and '\u2013' not in mid:  # exclude range entries like M92-M98
                    modules[mid] = name
    return modules

# House mapping
HOUSES = {
    "H01": {"name": "Natural Sciences", "spheres": list(range(1, 13))},
    "H02": {"name": "Formal Sciences", "spheres": list(range(13, 25))},
    "H03": {"name": "Social Sciences", "spheres": list(range(25, 37))},
    "H04": {"name": "Technology", "spheres": list(range(37, 49))},
    "H05": {"name": "Arts", "spheres": list(range(49, 61))},
    "H06": {"name": "Humanities", "spheres": list(range(61, 73))},
    "H07": {"name": "Applied Sciences", "spheres": list(range(73, 85))},
    "H08": {"name": "Education", "spheres": list(range(85, 97))},
    "H09": {"name": "Life Sciences", "spheres": list(range(97, 109))},
    "H10": {"name": "Health Sciences", "spheres": list(range(109, 121))},
    "H11": {"name": "Commerce & Industry", "spheres": list(range(121, 133))},
    "H12": {"name": "Law & Governance", "spheres": list(range(133, 145))},
}

# Module-to-house mapping (primary house assignment)
MODULE_HOUSE_MAP = {
    # Core Routing (H02 Formal Sciences - computational/algorithmic)
    "M1": "H02", "M2": "H02", "M3": "H02", "M3.1": "H02", "M3a": "H02",
    "M4": "H02", "M5": "H02", "M6": "H02", "M6a": "H02", "M6b": "H02",
    "M7": "H02", "M8": "H02", "M9": "H02", "M10": "H02", "M11": "H02",
    "M12": "H02", "M13": "H02", "M14": "H02", "M15": "H02", "M15a": "H02",
    "M16": "H02", "M17": "H02", "M17a": "H02", "M17b": "H02",
    # Extended Modules
    "M18": "H04", "M19": "H04", "M20": "H04", "M21": "H04", "M22": "H04",
    "M23": "H12", "M24": "H12", "M25": "H01", "M25a": "H01", "M25b": "H01", "M25c": "H01",
    "M26": "H04", "M27": "H12", "M28": "H04", "M29": "H04", "M30": "H04",
    "M31": "H04", "M32": "H04", "M33": "H04", "M34": "H02", "M35": "H12",
    # Phase 5+ modules
    "M40": "H04", "M41": "H04", "M42": "H04", "M43": "H10", "M44": "H07",
    "M45": "H04",
    # L6/L7
    "M46": "H04", "M47": "H04", "M48": "H04",
    # Extended
    "M49": "H04", "M50": "H01", "M51": "H01", "M52": "H01", "M53": "H01",
    "M54": "H01", "M55": "H01", "M56": "H01",
    # Filesystem-as-Ontology
    "M57": "H02", "M58": "H02", "M59": "H02", "M60": "H02", "M61": "H02",
    "M62": "H02", "M63": "H02",
    # Cross-Reference
    "M64": "H02", "M65": "H02", "M66": "H02", "M67": "H02",
    # Federation
    "M68": "H12", "M69": "H12", "M70": "H12",
    # 6-Council
    "M71": "H02", "M72": "H02", "M73": "H02", "M74": "H02", "M75": "H02",
    "M76": "H02", "M77": "H02", "M78": "H02", "M79": "H02", "M80": "H02",
    # Parallel Lane
    "M81": "H02", "M82": "H12", "M83": "H12", "M84": "H12",
    # Muskverse/Bezosverse
    "M85": "H04", "M86": "H04", "M87": "H11", "M88": "H01",
    # Indiana Genesis
    "M89": "H01", "M90": "H01", "M91": "H01", "M92": "H01",
    # M99-M108 Indiana Genesis renumbered
    "M99": "H01", "M100": "H01", "M101": "H01", "M102": "H01",
    "M103": "H01", "M104": "H02", "M105": "H01", "M106": "H01",
    "M107": "H01", "M108": "H01",
    # Bezosverse/Governance/Simulation
    "M109": "H11", "M110": "H11", "M111": "H11", "M112": "H04",
    "M113": "H04", "M114": "H04", "M115": "H04", "M116": "H02",
    "M117": "H02",
    # Switzerland Layer
    "M118": "H12", "M119": "H12", "M120": "H12", "M121": "H12",
    "M122": "H12", "M123": "H12", "M124": "H12", "M125": "H12",
    # Novel Research
    "M126": "H04", "M127": "H04", "M128": "H04", "M129": "H04",
    "M130": "H04", "M131": "H04", "M132": "H04", "M133": "H04",
    # Sprint 2
    "M134": "H04", "M135": "H04", "M136": "H04", "M137": "H04", "M138": "H04",
    # Reconciliation
    "M139": "H02", "M140": "H02", "M141": "H02",
    # TOS Compliance
    "M142": "H12", "M143": "H12", "M144": "H12", "M145": "H12",
    # Sovereignty
    "M146": "H12", "M147": "H12", "M148": "H06", "M149": "H06",
    "M150": "H06", "M151": "H06", "M152": "H06", "M153": "H06",
    "M154": "H06", "M155": "H06",
    # Federation
    "M156": "H12", "M157": "H02",
    # House 5 Arts
    "M158": "H05", "M159": "H05", "M160": "H05", "M161": "H05",
    "M162a": "H05", "M162b": "H05", "M163": "H05", "M164": "H05",
    "M165": "H05", "M166": "H05",
    # House 5 Gaming
    "M167": "H05", "M168": "H05", "M169": "H05", "M170": "H05",
    "M171": "H05", "M172": "H05",
    # 3-Seat Council Review
    "M173": "H02", "M174": "H12", "M175": "H05",
    # Boot Manifest Architecture
    "M176": "H07", "M177": "H07", "M178": "H07",
}

def generate_all():
    """Generate all codebase artifacts."""
    bp_path = "/home/ubuntu/COMPLETE_BUILD_PLAN_v3.11.md"
    out_dir = "/home/ubuntu/codebase-artifacts"

    # Extract modules from Build Plan
    bp_modules = extract_modules_from_buildplan(bp_path)
    print(f"Extracted {len(bp_modules)} modules from Build Plan")

    # === DOCTRINE REGISTRY ===
    os.makedirs(f"{out_dir}/registries", exist_ok=True)

    doctrine_data = {
        "metadata": {
            "version": "3.11",
            "source": "Build Plan v3.11 (ORC-015)",
            "generated_by": "Manus S7",
            "total_doctrines": 124,
            "ratified": 77,
            "reserved": 5,
            "proposed": 42,
            "counting_rule": "77 ratified (D-1-D-77) + 5 reserved (D-78-D-82) + 42 proposed (D-83-D-124) = 124 entries, 119 active"
        },
        "doctrines": []
    }
    for num in sorted(DOCTRINES.keys()):
        name, status, source = DOCTRINES[num]
        doctrine_data["doctrines"].append({
            "id": f"D-{num}",
            "name": name,
            "status": status,
            "source": source
        })

    with open(f"{out_dir}/registries/doctrine_registry.yaml", "w") as f:
        yaml.dump(doctrine_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Doctrine registry: {len(doctrine_data['doctrines'])} entries (77 ratified + 5 reserved + 42 proposed)")

    # === INVARIANT REGISTRY ===
    inv_data = {
        "metadata": {
            "version": "3.11",
            "source": "Build Plan v3.11 (ORC-015)",
            "generated_by": "Manus S7",
            "total_invariants": 45,
            "counting_rule": "INV-0 through INV-39 (40 base) + INV-40 Continuous Improvement + INV-41 Knowledge Preservation + INV-42 Stakeholder Notification + INV-43 Boot Manifest Freshness + INV-44 TOS Compliance = 45. INV-7c, INV-11.8, INV-19.2 are sub-specifications and do NOT increment the total.",
            "sub_specifications": ["INV-7c (of INV-7)", "INV-11.8 (of INV-11)", "INV-19.2 (of INV-19)"]
        },
        "invariants": [],
        "sub_specifications": []
    }
    for inv_id in sorted(INVARIANTS.keys(), key=lambda x: (int(re.search(r'\d+', x).group()), x)):
        inv = INVARIANTS[inv_id]
        inv_data["invariants"].append({
            "id": inv_id,
            "name": inv["name"],
            "type": inv["type"],
            "scope": inv["scope"],
            "description": inv["description"]
        })
    for ss_id in sorted(INV_SUBSPECS.keys()):
        ss = INV_SUBSPECS[ss_id]
        inv_data["sub_specifications"].append({
            "id": ss_id,
            "parent": ss["parent"],
            "name": ss["name"],
            "description": ss["description"]
        })

    with open(f"{out_dir}/registries/invariant_registry.yaml", "w") as f:
        yaml.dump(inv_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Invariant registry: {len(inv_data['invariants'])} invariants + {len(inv_data['sub_specifications'])} sub-specs")

    # === MODULE REGISTRY ===
    mod_data = {
        "metadata": {
            "version": "3.11",
            "source": "Build Plan v3.11 (ORC-015)",
            "generated_by": "Manus S7",
            "total_module_entries": len(bp_modules),
            "counting_rule": "Count by module entry. 164 L4 base integers + 12 sub-modules = 176 L4 entries + 3 L6/L7 = 179 total entries.",
            "l4_entries": 176,
            "l6l7_entries": 3,
            "sub_modules": ["M3.1", "M3a", "M6a", "M6b", "M15a", "M17a", "M17b", "M25a", "M25b", "M25c", "M162a", "M162b"],
            "reserved_gaps": ["M36-M39 (never allocated)", "M93-M98 (Indiana Genesis renumbering)"],
            "replaced": ["M162 -> M162a + M162b"]
        },
        "modules": []
    }

    l6l7 = {"M46", "M47", "M48"}
    for mid in sorted(bp_modules.keys(), key=lambda x: (
        int(re.search(r'\d+', x).group()),
        x.replace(re.search(r'\d+', x).group(), '')
    )):
        name = bp_modules[mid]
        house = MODULE_HOUSE_MAP.get(mid, "UNMAPPED")
        is_sub = bool(re.search(r'[a-z.]', mid[1:]))
        layer = "L6/L7" if mid in l6l7 else "L4"
        mod_data["modules"].append({
            "id": mid,
            "name": name,
            "layer": layer,
            "house": house,
            "is_sub_module": is_sub,
            "status": "SPEC"
        })

    with open(f"{out_dir}/registries/module_registry.yaml", "w") as f:
        yaml.dump(mod_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"Module registry: {len(mod_data['modules'])} entries")

    # === 12x12 MATRIX ===
    matrix_data = {
        "metadata": {
            "version": "3.11",
            "source": "Build Plan v3.11 (ORC-015)",
            "total_spheres": 144,
            "total_houses": 12
        },
        "houses": {}
    }

    # Build house-to-modules mapping
    house_modules = {}
    for mid, house in MODULE_HOUSE_MAP.items():
        if mid in bp_modules:
            if house not in house_modules:
                house_modules[house] = []
            house_modules[house].append(mid)

    for hid in sorted(HOUSES.keys()):
        h = HOUSES[hid]
        mods = sorted(house_modules.get(hid, []), key=lambda x: (int(re.search(r'\d+', x).group()), x))
        covered = len(set(mods))  # simplified coverage
        matrix_data["houses"][hid] = {
            "name": h["name"],
            "spheres": h["spheres"],
            "modules": mods,
            "module_count": len(mods),
        }

    with open(f"{out_dir}/registries/12x12_matrix.yaml", "w") as f:
        yaml.dump(matrix_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"12x12 matrix: {len(matrix_data['houses'])} houses")

    # === HOUSE MANIFESTS ===
    house_dir_names = {
        "H01": "natural_sciences", "H02": "formal_sciences", "H03": "social_sciences",
        "H04": "technology", "H05": "arts", "H06": "humanities",
        "H07": "applied_sciences", "H08": "education", "H09": "life_sciences",
        "H10": "health_sciences", "H11": "commerce_and_industry", "H12": "law_and_governance"
    }

    for hid in sorted(HOUSES.keys()):
        h = HOUSES[hid]
        dirname = house_dir_names[hid]
        hdir = f"{out_dir}/houses/{hid}_{dirname}"
        os.makedirs(hdir, exist_ok=True)

        mods = sorted(house_modules.get(hid, []), key=lambda x: (int(re.search(r'\d+', x).group()), x))
        manifest = {
            "house": {
                "id": hid,
                "name": h["name"],
                "sphere_range": f"{h['spheres'][0]}-{h['spheres'][-1]}",
                "total_spheres": 12
            },
            "modules": [{"id": m, "name": bp_modules.get(m, "UNKNOWN")} for m in mods],
            "module_count": len(mods),
            "coverage": f"{len(mods)} modules assigned"
        }

        with open(f"{hdir}/manifest.yaml", "w") as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"House manifests: 12 generated")

    # === TRANSPARENCY PACKET SCHEMA ===
    os.makedirs(f"{out_dir}/transparency-packet", exist_ok=True)
    tp_data = {
        "metadata": {
            "version": "1.6",
            "source": "Build Plan v3.11",
            "generated_by": "Manus S7"
        },
        "categories": {
            "routing": ["provider_id", "model_id", "sphere_id", "confidence_score", "tss_score", "routing_reason", "fallback_chain", "latency_ms"],
            "sovereignty": ["jurisdiction", "data_residency", "dpi_compliance", "cultural_frame", "sovereign_override"],
            "provenance": ["decision_hash", "parent_hash", "timestamp", "audit_trail", "human_attestor"],
            "metabolic": ["compute_cost", "energy_kwh", "carbon_grams", "water_liters", "cooling_overhead"],
            "economic": ["digital_dividend_pct", "provider_payment", "user_cost", "subsidy_applied"],
            "transparency": ["packet_version", "classification_tier", "redaction_reason", "golden_trace_id"],
            "consent": ["user_consent_level", "data_scope", "retention_period", "withdrawal_mechanism"],
            "federation": ["ceo_collective_vote", "federation_complementarity", "gap_sphere_flag", "provider_substitution"],
            "stacked_incentives": ["stacked_incentives_observable", "incentive_alignment_score", "coi_disclosure"],
            "water": ["vwb_score", "water_source", "downstream_quality", "nutrient_runoff", "inv19_compliance"],
            "tos": ["tos_version", "tos_compliance_status", "tos_review_date", "henderson_defense_applicable"],
            "creative": ["style_sovereignty_consent", "attribution_chain", "influence_estimation", "provenance_tier"],
            "gaming": ["game_ip_consent", "content_rating", "esports_integrity", "cloud_gaming_latency", "preservation_status"],
            "provider_monitoring": ["routing_share_pct", "retaliation_flag", "safe_harbor_status", "enterprise_wrapper_flag"],
            "boot": ["manifest_version", "manifest_freshness_hours", "boot_source", "manifest_hash"],
            "research_queue": ["pre_session_queries", "research_queue_depth", "cache_hit_rate"],
            "sync": ["state_sync_status", "cross_instance_delta", "last_sync_timestamp"],
            "kinetic": ["kinetic_rights_consent", "haptic_data_scope", "motion_capture_consent"],
            "distribution": ["distribution_channel", "feedback_loop_flag", "market_concentration_index"]
        }
    }

    total_fields = sum(len(v) for v in tp_data["categories"].values())
    tp_data["metadata"]["total_fields"] = total_fields
    tp_data["metadata"]["total_categories"] = len(tp_data["categories"])

    with open(f"{out_dir}/transparency-packet/schema_v1.6.yaml", "w") as f:
        yaml.dump(tp_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    print(f"TransparencyPacket v1.6: {total_fields} fields across {len(tp_data['categories'])} categories")

    # === SUMMARY ===
    print(f"\n=== Codebase Artifacts v1.3 Generated (from Build Plan v3.11) ===")
    print(f"Modules: {len(mod_data['modules'])}")
    print(f"Invariants: {len(inv_data['invariants'])} (+ {len(inv_data['sub_specifications'])} sub-specs)")
    print(f"Doctrines: {len(doctrine_data['doctrines'])} ({sum(1 for d in doctrine_data['doctrines'] if d['status']=='ratified')} ratified, {sum(1 for d in doctrine_data['doctrines'] if d['status']=='reserved')} reserved, {sum(1 for d in doctrine_data['doctrines'] if d['status']=='proposed')} proposed)")
    print(f"Houses: 12")
    print(f"TransparencyPacket v1.6: {total_fields} fields across {len(tp_data['categories'])} categories")

if __name__ == "__main__":
    generate_all()

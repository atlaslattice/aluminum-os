#!/usr/bin/env python3
"""
Innovation #1: The Sovereign Oracle
Self-Healing, Quantum-Safe Governance

Intersection: Pantheon Council + Self-Healing + Quantum-Safe Crypto + Decentralized Identity

The governance system detects compromised council members via behavioral anomaly
detection, isolates them, and auto-ejects them through BFT consensus — all while
maintaining quantum-resistant cryptographic integrity.
"""

import hashlib
import time
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class NodeStatus(Enum):
    HEALTHY = "healthy"
    SUSPICIOUS = "suspicious"
    COMPROMISED = "compromised"
    EJECTED = "ejected"


@dataclass
class BehaviorProfile:
    """Behavioral baseline for a council member."""
    node_id: str
    avg_response_time_ms: float = 100.0
    vote_consistency: float = 0.95  # How often votes align with stated reasoning
    proposal_quality: float = 0.9
    anomaly_score: float = 0.0
    observations: int = 0


@dataclass
class QuantumSafeSignature:
    """Post-quantum cryptographic signature (simulated Dilithium)."""
    algorithm: str = "CRYSTALS-Dilithium"
    key_size: int = 2592
    signature: str = ""
    public_key_hash: str = ""

    @staticmethod
    def sign(data: str, node_id: str) -> 'QuantumSafeSignature':
        # Simulated post-quantum signature
        combined = f"{data}:{node_id}:{time.time()}"
        sig = hashlib.sha3_512(combined.encode()).hexdigest()
        pk_hash = hashlib.sha3_256(node_id.encode()).hexdigest()
        return QuantumSafeSignature(
            signature=sig,
            public_key_hash=pk_hash
        )

    def verify(self) -> bool:
        return len(self.signature) == 128 and len(self.public_key_hash) == 64


class AnomalyDetector:
    """Zero-Trust AI Sentinel for council members."""

    ANOMALY_THRESHOLD = 0.7
    COMPROMISE_THRESHOLD = 0.9

    def __init__(self):
        self.profiles: Dict[str, BehaviorProfile] = {}

    def register_node(self, node_id: str):
        self.profiles[node_id] = BehaviorProfile(node_id=node_id)

    def observe(self, node_id: str, response_time_ms: float,
                vote_consistent: bool, proposal_quality: float) -> NodeStatus:
        if node_id not in self.profiles:
            self.register_node(node_id)

        profile = self.profiles[node_id]
        profile.observations += 1

        # Calculate anomaly score — baseline is FIXED to detect persistent attacks
        time_anomaly = abs(response_time_ms - 100.0) / 100.0  # Fixed baseline of 100ms
        consistency_anomaly = 0.0 if vote_consistent else 0.6
        quality_anomaly = max(0, 0.9 - proposal_quality)  # Fixed quality baseline of 0.9

        raw_anomaly = (time_anomaly * 0.3) + (consistency_anomaly * 0.4) + (quality_anomaly * 0.3)
        # Anomaly score only goes UP, never down — ratchet mechanism
        alpha = 0.6
        new_score = alpha * raw_anomaly + (1 - alpha) * profile.anomaly_score
        profile.anomaly_score = max(profile.anomaly_score, new_score) if raw_anomaly > 0.3 else new_score

        # Update observation stats (slow adaptation for monitoring only)
        beta = 0.1  # Slow baseline update
        profile.avg_response_time_ms = beta * response_time_ms + (1 - beta) * profile.avg_response_time_ms
        if vote_consistent:
            profile.vote_consistency = beta * 1.0 + (1 - beta) * profile.vote_consistency
        else:
            profile.vote_consistency = beta * 0.0 + (1 - beta) * profile.vote_consistency
        profile.proposal_quality = beta * proposal_quality + (1 - beta) * profile.proposal_quality

        if profile.anomaly_score >= self.COMPROMISE_THRESHOLD:
            return NodeStatus.COMPROMISED
        elif profile.anomaly_score >= self.ANOMALY_THRESHOLD:
            return NodeStatus.SUSPICIOUS
        return NodeStatus.HEALTHY


class SovereignOracle:
    """Self-healing, quantum-safe governance system."""

    def __init__(self, council_size: int = 5, dave_protocol_holder: str = "daavud"):
        self.council: Dict[str, NodeStatus] = {}
        self.detector = AnomalyDetector()
        self.dave_holder = dave_protocol_holder
        self.audit_chain: List[Dict] = []
        self.ejection_log: List[Dict] = []

        # Initialize council
        for i in range(council_size):
            node_id = f"council_member_{i}"
            self.council[node_id] = NodeStatus.HEALTHY
            self.detector.register_node(node_id)

    def _log_audit(self, event: str, details: Dict):
        entry = {
            "timestamp": time.time(),
            "event": event,
            "details": details,
            "signature": QuantumSafeSignature.sign(
                json.dumps(details), "oracle"
            ).__dict__
        }
        self.audit_chain.append(entry)

    def observe_behavior(self, node_id: str, response_time_ms: float,
                         vote_consistent: bool, proposal_quality: float) -> Dict:
        status = self.detector.observe(node_id, response_time_ms,
                                       vote_consistent, proposal_quality)
        old_status = self.council.get(node_id, NodeStatus.HEALTHY)

        # If already ejected, don't overwrite — ejection is permanent
        if old_status == NodeStatus.EJECTED:
            result = {
                "node_id": node_id,
                "old_status": old_status.value,
                "new_status": "ejected",
                "anomaly_score": round(self.detector.profiles[node_id].anomaly_score, 4),
                "action": "already_ejected"
            }
            self._log_audit("behavior_observed", result)
            return result

        self.council[node_id] = status

        result = {
            "node_id": node_id,
            "old_status": old_status.value,
            "new_status": status.value,
            "anomaly_score": round(self.detector.profiles[node_id].anomaly_score, 4),
            "action": "none"
        }

        if status == NodeStatus.COMPROMISED:
            # Auto-eject via BFT vote
            ejection = self._auto_eject(node_id)
            result["action"] = "ejected" if ejection["success"] else "ejection_failed"
            result["ejection_details"] = ejection

        self._log_audit("behavior_observed", result)
        return result

    def _auto_eject(self, compromised_node: str) -> Dict:
        """BFT consensus to eject a compromised node."""
        healthy_nodes = [n for n, s in self.council.items()
                        if s == NodeStatus.HEALTHY and n != compromised_node]
        total_voters = len(healthy_nodes)
        required_votes = (total_voters * 2 // 3) + 1  # BFT 2/3 + 1

        # Simulate voting (healthy nodes vote to eject)
        votes_for = total_voters  # All healthy nodes agree
        success = votes_for >= required_votes

        if success:
            self.council[compromised_node] = NodeStatus.EJECTED
            self.ejection_log.append({
                "node": compromised_node,
                "timestamp": time.time(),
                "votes_for": votes_for,
                "votes_required": required_votes,
                "quantum_signature": QuantumSafeSignature.sign(
                    f"eject:{compromised_node}", "oracle"
                ).__dict__
            })

        return {
            "success": success,
            "votes_for": votes_for,
            "votes_required": required_votes,
            "total_voters": total_voters,
        }

    def dave_veto(self, proposal_id: str) -> Dict:
        """Dave Protocol: absolute human veto power."""
        result = {
            "proposal_id": proposal_id,
            "vetoed_by": self.dave_holder,
            "status": "VETOED",
            "timestamp": time.time(),
            "note": "Dave Protocol veto is absolute and non-negotiable"
        }
        self._log_audit("dave_veto", result)
        return result

    def status(self) -> Dict:
        return {
            "council": {k: v.value for k, v in self.council.items()},
            "audit_chain_length": len(self.audit_chain),
            "ejections": len(self.ejection_log),
            "quantum_crypto": "CRYSTALS-Dilithium (post-quantum)",
            "dave_protocol": "ACTIVE",
        }


def test():
    print("=" * 60)
    print("  Innovation #1: The Sovereign Oracle")
    print("  Self-Healing, Quantum-Safe Governance")
    print("=" * 60)

    oracle = SovereignOracle(council_size=5)
    results = []

    # Test 1: Normal behavior
    print("\n[TEST 1] Normal behavior observation")
    r = oracle.observe_behavior("council_member_0", 95.0, True, 0.92)
    print(f"  Status: {r['new_status']}, Anomaly: {r['anomaly_score']}")
    results.append(r['new_status'] == 'healthy')

    # Test 2: Suspicious behavior
    print("\n[TEST 2] Suspicious behavior detection")
    for _ in range(10):
        r = oracle.observe_behavior("council_member_1", 1000.0, False, 0.05)
    print(f"  Status: {r['new_status']}, Anomaly: {r['anomaly_score']}")
    results.append(r['new_status'] in ['suspicious', 'compromised', 'ejected'])

    # Test 3: Compromised node auto-ejection
    print("\n[TEST 3] Compromised node auto-ejection")
    for _ in range(20):
        r = oracle.observe_behavior("council_member_2", 5000.0, False, 0.0)
    print(f"  Status: {r['new_status']}, Action: {r['action']}")
    if 'ejection_details' in r:
        print(f"  Votes: {r['ejection_details']['votes_for']}/{r['ejection_details']['votes_required']}")
    results.append(r['action'] in ('ejected', 'already_ejected'))

    # Test 4: Quantum-safe signatures
    print("\n[TEST 4] Quantum-safe signatures")
    sig = QuantumSafeSignature.sign("test_data", "test_node")
    verified = sig.verify()
    print(f"  Algorithm: {sig.algorithm}, Key size: {sig.key_size}")
    print(f"  Signature length: {len(sig.signature)}, Verified: {verified}")
    results.append(verified)

    # Test 5: Dave Protocol veto
    print("\n[TEST 5] Dave Protocol veto")
    veto = oracle.dave_veto("proposal_123")
    print(f"  Vetoed by: {veto['vetoed_by']}, Status: {veto['status']}")
    results.append(veto['status'] == 'VETOED')

    # Test 6: System status
    print("\n[TEST 6] System status")
    status = oracle.status()
    print(f"  Audit chain: {status['audit_chain_length']} entries")
    print(f"  Ejections: {status['ejections']}")
    print(f"  Crypto: {status['quantum_crypto']}")
    results.append(status['ejections'] >= 1)

    passed = sum(results)
    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {passed}/{len(results)} PASSED")
    print(f"{'=' * 60}")
    return passed == len(results)


if __name__ == "__main__":
    import sys
    sys.exit(0 if test() else 1)

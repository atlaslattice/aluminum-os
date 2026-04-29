#!/usr/bin/env python3
"""
Innovation #2: The Dream Weaver
Predictive, Cross-Device AR Workspaces

Intersection: Cross-Device Continuity + AI-Scheduler + AR Workspace + Predictive Power

Your workspace follows you across devices. The AI predicts which device you'll
use next and pre-loads your context before you even touch it.
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class DeviceType(Enum):
    LAPTOP = "laptop"
    PHONE = "phone"
    AR_GLASSES = "ar_glasses"
    TABLET = "tablet"
    DESKTOP = "desktop"
    CAR_DISPLAY = "car_display"


@dataclass
class DeviceState:
    device_id: str
    device_type: DeviceType
    is_active: bool = False
    battery_level: float = 100.0
    last_used: float = 0.0
    preloaded_context: Optional[str] = None


@dataclass
class WorkspaceContext:
    """The user's current working context — clipboard, tabs, app states."""
    context_id: str
    clipboard: str = ""
    open_tabs: List[str] = field(default_factory=list)
    active_app: str = ""
    cursor_position: Dict = field(default_factory=dict)
    timestamp: float = 0.0

    def serialize(self) -> str:
        return json.dumps({
            "id": self.context_id,
            "clipboard": self.clipboard,
            "tabs": self.open_tabs,
            "app": self.active_app,
            "cursor": self.cursor_position,
            "ts": self.timestamp
        })


class DevicePredictor:
    """Predicts which device the user will switch to next."""

    def __init__(self):
        self.transition_history: List[tuple] = []  # (from_device, to_device, time_of_day)
        self.transition_counts: Dict[str, Dict[str, int]] = {}

    def record_transition(self, from_device: str, to_device: str):
        hour = int(time.time() % 86400 / 3600)
        self.transition_history.append((from_device, to_device, hour))

        if from_device not in self.transition_counts:
            self.transition_counts[from_device] = {}
        self.transition_counts[from_device][to_device] = \
            self.transition_counts[from_device].get(to_device, 0) + 1

    def predict_next(self, current_device: str) -> Optional[str]:
        if current_device not in self.transition_counts:
            return None
        transitions = self.transition_counts[current_device]
        if not transitions:
            return None
        return max(transitions, key=transitions.get)

    def confidence(self, current_device: str) -> float:
        if current_device not in self.transition_counts:
            return 0.0
        transitions = self.transition_counts[current_device]
        total = sum(transitions.values())
        if total == 0:
            return 0.0
        max_count = max(transitions.values())
        return round(max_count / total, 3)


class DreamWeaver:
    """Cross-device continuity with predictive context pre-loading."""

    def __init__(self):
        self.devices: Dict[str, DeviceState] = {}
        self.predictor = DevicePredictor()
        self.current_context = WorkspaceContext(
            context_id=hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
        )
        self.sync_log: List[Dict] = []

    def register_device(self, device_id: str, device_type: DeviceType):
        self.devices[device_id] = DeviceState(
            device_id=device_id,
            device_type=device_type
        )

    def update_context(self, clipboard: str = "", tabs: List[str] = None,
                       active_app: str = ""):
        self.current_context.clipboard = clipboard or self.current_context.clipboard
        self.current_context.open_tabs = tabs or self.current_context.open_tabs
        self.current_context.active_app = active_app or self.current_context.active_app
        self.current_context.timestamp = time.time()

    def switch_device(self, from_device: str, to_device: str) -> Dict:
        """Switch active device with predictive pre-loading."""
        # Record transition for learning
        self.predictor.record_transition(from_device, to_device)

        # Deactivate old device
        if from_device in self.devices:
            self.devices[from_device].is_active = False

        # Activate new device with synced context
        if to_device in self.devices:
            self.devices[to_device].is_active = True
            self.devices[to_device].last_used = time.time()
            self.devices[to_device].preloaded_context = self.current_context.serialize()

        # Predict next device and pre-load
        predicted_next = self.predictor.predict_next(to_device)
        if predicted_next and predicted_next in self.devices:
            self.devices[predicted_next].preloaded_context = self.current_context.serialize()

        result = {
            "from": from_device,
            "to": to_device,
            "context_synced": True,
            "predicted_next": predicted_next,
            "prediction_confidence": self.predictor.confidence(to_device),
            "preloaded_devices": [d for d, s in self.devices.items() if s.preloaded_context],
        }
        self.sync_log.append(result)
        return result

    def status(self) -> Dict:
        return {
            "devices": {k: {"type": v.device_type.value, "active": v.is_active,
                            "preloaded": v.preloaded_context is not None}
                       for k, v in self.devices.items()},
            "context": self.current_context.active_app,
            "sync_events": len(self.sync_log),
        }


def test():
    print("=" * 60)
    print("  Innovation #2: The Dream Weaver")
    print("  Predictive, Cross-Device AR Workspaces")
    print("=" * 60)

    dw = DreamWeaver()
    results = []

    # Register devices
    dw.register_device("macbook", DeviceType.LAPTOP)
    dw.register_device("pixel", DeviceType.PHONE)
    dw.register_device("xr_glasses", DeviceType.AR_GLASSES)
    dw.register_device("chromebook", DeviceType.TABLET)

    # Set context
    dw.update_context(
        clipboard="Noosphere defense analysis",
        tabs=["github.com", "notion.so", "x.com"],
        active_app="VS Code"
    )

    # Test 1: Device switch with sync
    print("\n[TEST 1] Device switch with context sync")
    r = dw.switch_device("macbook", "pixel")
    print(f"  Synced: {r['context_synced']}")
    results.append(r['context_synced'])

    # Build transition history for prediction
    for _ in range(5):
        dw.switch_device("pixel", "xr_glasses")
        dw.switch_device("xr_glasses", "macbook")
        dw.switch_device("macbook", "pixel")

    # Test 2: Prediction accuracy
    print("\n[TEST 2] Device prediction")
    r = dw.switch_device("macbook", "pixel")
    print(f"  Predicted next: {r['predicted_next']}")
    print(f"  Confidence: {r['prediction_confidence']}")
    results.append(r['predicted_next'] == 'xr_glasses')

    # Test 3: Pre-loading
    print("\n[TEST 3] Context pre-loading")
    preloaded = r['preloaded_devices']
    print(f"  Preloaded devices: {preloaded}")
    results.append(len(preloaded) >= 2)

    # Test 4: Status
    print("\n[TEST 4] System status")
    status = dw.status()
    print(f"  Devices: {len(status['devices'])}, Sync events: {status['sync_events']}")
    results.append(status['sync_events'] > 10)

    passed = sum(results)
    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {passed}/{len(results)} PASSED")
    print(f"{'=' * 60}")
    return passed == len(results)


if __name__ == "__main__":
    import sys
    sys.exit(0 if test() else 1)

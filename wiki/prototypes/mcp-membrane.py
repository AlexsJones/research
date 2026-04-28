#!/usr/bin/env python3
"""
Prototype A: MCP-based Synthetic Membrane

Uses MCP's Resources and Tools to create a shared membrane between agents.
Each agent exposes state as MCP resources and capabilities as MCP tools.
Agents discover each other through a directory resource.

Key insight: MCP resources are URI-addressable — perfect for shared state.
"""
import json
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any

# ── Membrane State ──

@dataclass
class MembraneEntry:
    """A single piece of shared state in the membrane."""
    id: str
    agent_id: str
    key: str              # e.g. "current_task", "discovery", "sensor_reading"
    value: Any            # structured data
    permeability: str = "public"   # public | trusted | private
    created: float = field(default_factory=time.time)
    ttl: float | None = None       # seconds until decay
    tags: list[str] = field(default_factory=list)
    
    def is_expired(self) -> bool:
        if self.ttl is None:
            return False
        return time.time() > self.created + self.ttl
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop('is_expired', None)
        return d


class Membrane:
    """
    The shared membrane — a permeable state layer between agents.
    
    Implements the three layers:
    1. Permeability — agents declare what they expose and subscribe to
    2. Shared Medium — the actual state store
    3. Coordination — discovery, broadcasting, swarm activation
    """
    
    def __init__(self):
        self._store: dict[str, MembraneEntry] = {}
        self._exposures: dict[str, set[str]] = {}  # agent_id -> keys exposed
        self._subscriptions: dict[str, set[str]] = {}  # agent_id -> key patterns
        self._trust: dict[str, set[str]] = {}  # agent_id -> trusted agent_ids
    
    # ── Registration ──
    
    def register_agent(self, agent_id: str, capabilities: list[str],
                       expose: list[str] | None = None,
                       subscribe: list[str] | None = None,
                       trust: list[str] | None = None):
        """Register an agent with the membrane."""
        self._exposures[agent_id] = set(expose or [])
        self._subscriptions[agent_id] = set(subscribe or [])
        self._trust[agent_id] = set(trust or [])
        # Publish agent capabilities as a membrane entry
        self.write_entry(
            agent_id=agent_id,
            key="__capabilities",
            value={"capabilities": capabilities, "registered_at": time.time()},
            permeability="public",
            tags=["discovery"],
        )
        caps = self.read_entry(agent_id, "__capabilities")
        return caps[0] if caps else {}
    
    # ── Core Operations ──
    
    def write_entry(self, agent_id: str, key: str, value: Any,
                    permeability: str = "public", tags: list[str] | None = None,
                    ttl: float | None = None) -> dict:
        """Write state to the membrane."""
        entry_id = str(uuid.uuid4())
        entry = MembraneEntry(
            id=entry_id, agent_id=agent_id, key=key, value=value,
            permeability=permeability, tags=tags or [], ttl=ttl,
        )
        self._store[entry_id] = entry
        # Notify subscribers
        events = self._notify_subscribers(agent_id, key, value)
        return {"id": entry_id, "events": events}
    
    def read_entry(self, reader_id: str, key: str,
                   agent_id: str | None = None) -> list[dict]:
        """Read from the membrane with permeability checks."""
        results = []
        for entry in self._store.values():
            if entry.is_expired():
                continue
            # Key match
            if key and not entry.key.startswith(key):
                continue
            # Agent filter
            if agent_id and entry.agent_id != agent_id:
                continue
            # Permeability check
            if not self._can_read(reader_id, entry):
                continue
            results.append(entry.to_dict())
        return results
    
    def _can_read(self, reader_id: str, entry: MembraneEntry) -> bool:
        if entry.permeability == "public":
            return True
        if entry.permeability == "trusted":
            # Writer trusts the reader
            return reader_id in self._trust.get(entry.agent_id, set())
        if entry.permeability == "private":
            return reader_id == entry.agent_id
        return False
    
    def _notify_subscribers(self, writer_id: str, key: str, value: Any) -> list[dict]:
        """Notify agents subscribed to this key."""
        events = []
        for agent_id, patterns in self._subscriptions.items():
            for pattern in patterns:
                if key.startswith(pattern) or key == pattern:
                    events.append({
                        "agent": agent_id,
                        "from": writer_id,
                        "key": key,
                        "value": value,
                        "time": time.time(),
                    })
        return events
    
    # ── Discovery ──
    
    def discover_agents(self, reader_id: str,
                        capability: str | None = None) -> list[dict]:
        """Discover registered agents, optionally filtered by capability."""
        agents = []
        for entry in self._store.values():
            if entry.key != "__capabilities" or entry.is_expired():
                continue
            if not self._can_read(reader_id, entry):
                continue
            if capability and capability not in entry.value.get("capabilities", []):
                continue
            agents.append({
                "agent_id": entry.agent_id,
                "capabilities": entry.value["capabilities"],
            })
        return agents
    
    # ── Broadcast ──
    
    def broadcast(self, agent_id: str, message: str,
                  target_capability: str | None = None) -> list[dict]:
        """Broadcast a message, optionally targeting agents with a capability."""
        entry_id = str(uuid.uuid4())
        entry = MembraneEntry(
            id=entry_id, agent_id=agent_id, key="__broadcast",
            value={"message": message, "targets": target_capability},
            permeability="public", tags=["broadcast"],
        )
        self._store[entry_id] = entry
        recipients = []
        for sub_agent_id in self._subscriptions:
            if "__broadcast" in self._subscriptions[sub_agent_id]:
                if target_capability:
                    caps = self._store.get(
                        next((eid for eid, e in self._store.items()
                              if e.agent_id == sub_agent_id and e.key == "__capabilities"),
                             None), None)
                    if caps and target_capability in caps.value.get("capabilities", []):
                        recipients.append(sub_agent_id)
                else:
                    recipients.append(sub_agent_id)
        return recipients
    
    # ── Cleanup ──
    
    def cleanup_expired(self) -> int:
        """Remove expired entries."""
        expired = [eid for eid, e in self._store.items() if e.is_expired()]
        for eid in expired:
            del self._store[eid]
        return len(expired)
    
    # ── State ──
    
    def state_summary(self) -> dict:
        return {
            "agents": list(self._exposures.keys()),
            "entries": len(self._store),
            "total_keys": len(set(e.key for e in self._store.values())),
        }


# ── Demo: Two agents sharing state through the membrane ──

def demo():
    print("=" * 60)
    print("SYNTHETIC MEMBRANE — MCP-Based Prototype")
    print("=" * 60)
    
    membrane = Membrane()
    
    # Agent A: Sensor agent
    sensor = membrane.register_agent(
        agent_id="sensor-01",
        capabilities=["temperature_reading", "humidity_reading"],
        expose=["sensors.temp", "sensors.humidity"],
        subscribe=["__broadcast"],
    )
    print(f"\n[Register] sensor-01: {json.dumps(sensor, indent=2)}")
    
    # Agent B: Analyzer agent
    analyzer = membrane.register_agent(
        agent_id="analyzer-01",
        capabilities=["anomaly_detection", "trend_analysis"],
        subscribe=["sensors.", "__broadcast"],
        trust=["sensor-01"],
    )
    print(f"[Register] analyzer-01: {json.dumps(analyzer, indent=2)}")
    
    # Sensor writes data (public)
    result = membrane.write_entry(
        agent_id="sensor-01", key="sensors.temp",
        value={"location": "server-room", "value": 42.5, "unit": "celsius"},
        permeability="public",
        tags=["sensor", "temperature"],
        ttl=60,  # expires in 60 seconds
    )
    print(f"\n[Write] sensor-01 -> sensors.temp: {json.dumps(result, indent=2)}")
    
    # Analyzer reads sensor data
    readings = membrane.read_entry("analyzer-01", "sensors.temp")
    print(f"[Read] analyzer-01 reads sensors.temp: {json.dumps(readings, indent=2)}")
    
    # Sensor writes private data
    result = membrane.write_entry(
        agent_id="sensor-01", key="sensors.calibration",
        value={"offset": 0.3, "last_calibrated": "2026-04-26"},
        permeability="trusted",
    )
    print(f"\n[Write] sensor-01 -> sensors.calibration (trusted): {json.dumps(result, indent=2)}")
    
    # Analyzer (trusted) can read it
    cal = membrane.read_entry("analyzer-01", "sensors.calibration")
    print(f"[Read] analyzer-01 (trusted) reads calibration: {json.dumps(cal, indent=2)}")
    
    # Unknown agent cannot read trusted data
    cal = membrane.read_entry("unknown-01", "sensors.calibration")
    print(f"[Read] unknown-01 (not trusted) reads calibration: {json.dumps(cal, indent=2)}")
    
    # Discovery
    agents = membrane.discover_agents("analyzer-01", "temperature_reading")
    print(f"\n[Discover] agents with 'temperature_reading': {json.dumps(agents, indent=2)}")
    
    # Broadcast
    recipients = membrane.broadcast("analyzer-01", "ANOMALY DETECTED: temp > 40C")
    print(f"\n[Broadcast] anomaly alert -> recipients: {recipients}")
    
    # State summary
    print(f"\n[State]: {json.dumps(membrane.state_summary(), indent=2)}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    
    return membrane


if __name__ == "__main__":
    demo()

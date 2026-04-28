#!/usr/bin/env python3
"""
Prototype D: Swarm Membrane — Quorum Sensing

Agents emit chemical-like signals. When concentration crosses a threshold,
swarm behavior activates automatically. Swarm dissolves when task completes.

Inspired by: bacterial quorum sensing, ant colony foraging.
"""
import json
import time
import uuid
import math
from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class SignalType(str, Enum):
    ALERT = "alert"           # Something needs attention
    RECRUIT = "recruit"       # Need more agents
    COMPLETED = "completed"   # Task done
    ALL_CLEAR = "all_clear"   # Situation resolved


class AgentState(str, Enum):
    IDLE = "idle"
    DETECTING = "detecting"
    SIGNALING = "signaling"
    SWARMING = "swarming"
    WORKING = "working"
    STANDBY = "standby"


@dataclass
class Signal:
    """A chemical-like signal in the environment."""
    id: str
    source: str
    signal_type: str
    intensity: float          # 0.0 - 1.0
    key: str                  # what this signal is about (e.g. "fire", "bug")
    created: float = field(default_factory=time.time)
    decay_rate: float = 0.1   # per second
    
    def concentration(self, now: float) -> float:
        age = now - self.created
        return self.intensity * math.exp(-self.decay_rate * age)
    
    def is_expired(self, now: float, threshold: float = 0.001) -> bool:
        return self.concentration(now) < threshold


class Swarm:
    """An active swarm working on a task."""
    
    def __init__(self, task_id: str, trigger_key: str, trigger_agent: str):
        self.task_id = task_id
        self.trigger_key = trigger_key
        self.trigger_agent = trigger_agent
        self.members: set[str] = {trigger_agent}
        self.created = time.time()
        self.status = "active"
        self.progress: dict = {}
    
    def join(self, agent_id: str):
        self.members.add(agent_id)
    
    def leave(self, agent_id: str):
        self.members.discard(agent_id)
    
    def update_progress(self, agent_id: str, progress: Any):
        self.progress[agent_id] = progress
    
    @property
    def quorum(self) -> int:
        return len(self.members)
    
    @property
    def is_dissolved(self) -> bool:
        return self.status == "dissolved"


class SwarmMembrane:
    """
    Quorum-sensing swarm coordination.
    
    Agents detect problems, emit signals. When total signal concentration
    for a key exceeds a threshold, a swarm activates. Agents join based on
    their capabilities matching the swarm's needs.
    """
    
    def __init__(self, swarm_threshold: float = 1.0, quorum_size: int = 2):
        self._signals: dict[str, list[Signal]] = {}  # key -> signals
        self._swarms: dict[str, Swarm] = {}
        self._agents: dict[str, dict] = {}
        self._swarm_threshold = swarm_threshold
        self._quorum_size = quorum_size
        self._event_log: list[dict] = []
    
    def register_agent(self, agent_id: str, capabilities: list[str],
                       sensitivity: float = 1.0):
        self._agents[agent_id] = {
            "capabilities": set(capabilities),
            "state": AgentState.IDLE,
            "sensitivity": sensitivity,
            "current_swarm": None,
        }
    
    def emit_signal(self, agent_id: str, signal_type: str, key: str,
                    intensity: float = 0.5):
        """An agent emits a signal into the environment."""
        signal = Signal(
            id=str(uuid.uuid4()),
            source=agent_id,
            signal_type=signal_type,
            intensity=min(intensity, 1.0),
            key=key,
        )
        if key not in self._signals:
            self._signals[key] = []
        self._signals[key].append(signal)
        
        self._log(agent_id, "emit_signal", {
            "type": signal_type, "key": key, "intensity": intensity,
        })
    
    def tick(self) -> list[dict]:
        """
        Advance the simulation by one tick.
        
        - Decay signals
        - Check thresholds
        - Activate swarms when threshold exceeded
        - Agents join swarms based on capability matching
        - Swarms complete and dissolve
        """
        now = time.time()
        events = []
        
        # Decay signals and clean expired
        for key in list(self._signals.keys()):
            self._signals[key] = [
                s for s in self._signals[key]
                if not s.is_expired(now)
            ]
            if not self._signals[key]:
                del self._signals[key]
        
        # Check thresholds and activate swarms
        for key, signals in self._signals.items():
            total_concentration = sum(s.concentration(now) for s in signals)
            
            if total_concentration >= self._swarm_threshold:
                if key not in self._swarms:
                    # Find the primary signal source
                    primary = max(signals, key=lambda s: s.concentration(now))
                    swarm = Swarm(key, key, primary.source)
                    self._swarms[key] = swarm
                    events.append({
                        "event": "swarm_activated",
                        "task": key,
                        "trigger": total_concentration,
                        "threshold": self._swarm_threshold,
                    })
                    self._log(primary.source, "swarm_activated", {"task": key})
        
        # Agents join swarms they're not already in
        for agent_id, info in self._agents.items():
            if info["state"] == AgentState.IDLE:
                # Find the strongest swarm this agent can contribute to
                best_swarm = None
                best_concentration = 0
                for key, signals in self._signals.items():
                    if key in self._swarms:
                        swarm = self._swarms[key]
                        if swarm.is_dissolved:
                            continue
                        conc = sum(s.concentration(now) for s in signals)
                        # Check if agent has relevant capabilities
                        if self._capability_matches(agent_id, key):
                            if conc > best_concentration:
                                best_concentration = conc
                                best_swarm = swarm
                
                if best_swarm and best_swarm.quorum < 10:  # max swarm size
                    best_swarm.join(agent_id)
                    info["state"] = AgentState.SWARMING
                    info["current_swarm"] = best_swarm.task_id
                    events.append({
                        "event": "agent_joined_swarm",
                        "agent": agent_id,
                        "swarm": best_swarm.task_id,
                        "quorum": best_swarm.quorum,
                    })
        
        # Simulate swarm work completion
        for key, swarm in self._swarms.items():
            if swarm.is_dissolved:
                continue
            if swarm.quorum >= self._quorum_size:
                # Swarm has enough members, simulate progress
                # In real system, agents would report actual progress
                swarm.status = "working"
                for member in swarm.members:
                    if member in self._agents:
                        self._agents[member]["state"] = AgentState.WORKING
                
                # Auto-complete after reaching quorum (simplified)
                swarm.status = "dissolved"
                events.append({
                    "event": "swarm_completed",
                    "task": key,
                    "members": list(swarm.members),
                })
                self._log("system", "swarm_completed", {"task": key})
                
                # Reset agents
                for member in swarm.members:
                    if member in self._agents:
                        self._agents[member]["state"] = AgentState.IDLE
                        self._agents[member]["current_swarm"] = None
        
        return events
    
    def _capability_matches(self, agent_id: str, task_key: str) -> bool:
        """Check if an agent has capabilities relevant to a task."""
        info = self._agents.get(agent_id, {})
        caps = info.get("capabilities", set())
        # Simple matching: task key contains a capability or vice versa
        task_parts = task_key.split(".")
        return bool(caps & set(task_parts)) or bool(caps)  # any agent can join for demo
    
    def get_state(self, agent_id: str) -> dict:
        info = self._agents.get(agent_id, {})
        return {
            "state": info.get("state", AgentState.IDLE).value,
            "current_swarm": info.get("current_swarm"),
        }
    
    def system_state(self) -> dict:
        now = time.time()
        return {
            "agents": {
                aid: {
                    "state": info["state"].value,
                    "swarm": info["current_swarm"],
                    "capabilities": list(info["capabilities"]),
                }
                for aid, info in self._agents.items()
            },
            "active_swarms": {
                k: {"members": list(s.members), "quorum": s.quorum, "status": s.status}
                for k, s in self._swarms.items()
                if not s.is_dissolved
            },
            "signal_keys": list(self._signals.keys()),
        }
    
    def _log(self, source: str, event: str, data: dict):
        self._event_log.append({
            "source": source, "event": event, "data": data,
            "time": time.time(),
        })
    
    def event_log(self) -> list[dict]:
        return self._event_log


# ── Demo: Swarm activation and dissolution ──

def demo():
    print("=" * 60)
    print("SYNTHETIC MEMBRANE — Swarm / Quorum Sensing")
    print("=" * 60)
    
    membrane = SwarmMembrane(swarm_threshold=1.5, quorum_size=2)
    
    # Register 5 agents with different capabilities
    membrane.register_agent("agent-1", ["monitoring", "alerting"])
    membrane.register_agent("agent-2", ["debugging", "fixing"])
    membrane.register_agent("agent-3", ["analysis", "debugging"])
    membrane.register_agent("agent-4", ["monitoring", "scaling"])
    membrane.register_agent("agent-5", ["testing", "validation"])
    
    print("\n--- Initial State: All agents idle ---")
    for i in range(1, 6):
        state = membrane.get_state(f"agent-{i}")
        print(f"  agent-{i}: {state['state']}")
    
    print("\n--- Event: Agent-1 detects a problem, emits signals ---")
    
    # Agent 1 detects something wrong and starts signaling
    membrane.emit_signal("agent-1", SignalType.ALERT, "bug.crash", intensity=0.6)
    membrane.emit_signal("agent-1", SignalType.RECRUIT, "bug.crash", intensity=0.5)
    
    print("  agent-1 -> ALERT + RECRUIT on 'bug.crash'")
    print("  Total signal concentration: {:.2f} (threshold: {:.2f})".format(
        1.1, membrane._swarm_threshold))
    
    # Agent 3 also detects the issue
    membrane.emit_signal("agent-3", SignalType.ALERT, "bug.crash", intensity=0.7)
    print("  agent-3 -> ALERT on 'bug.crash'")
    
    print("\n--- Tick 1: Swarm activates ---")
    events = membrane.tick()
    for ev in events:
        print(f"  [{ev['event']}] {json.dumps({k:v for k,v in ev.items() if k != 'event'})}")
    
    print("\n--- Agent States After Swarm ---")
    for i in range(1, 6):
        state = membrane.get_state(f"agent-{i}")
        print(f"  agent-{i}: {state['state']} (swarm: {state['current_swarm']})")
    
    print("\n--- System State ---")
    sys_state = membrane.system_state()
    print(json.dumps(sys_state, indent=2, default=str))
    
    # Simulate signal decay over time
    print("\n--- Signal Decay (simulated) ---")
    if "bug.crash" in membrane._signals:
        now = time.time()
        for s in membrane._signals["bug.crash"]:
            print(f"  {s.source}: conc = {s.concentration(now):.3f}")
    
    print("\n--- Event Log ---")
    for ev in membrane.event_log():
        print(f"  {ev['source']:12} | {ev['event']:20} | {json.dumps(ev['data'])}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE — Swarm activated, task completed, agents returned to idle")
    print("=" * 60)


if __name__ == "__main__":
    demo()

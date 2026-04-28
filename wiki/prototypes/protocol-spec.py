#!/usr/bin/env python3
"""
Prototype C: Membrane Protocol Specification

Defines the wire protocol for agent-to-agent membrane communication.
JSON messages over any transport (WebSocket, HTTP, gRPC, NATS).

Message types: EXPOSE | SUBSCRIBE | READ | WRITE | BROADCAST | SWARM | DECAY
"""
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any
from enum import Enum


class MsgType(str, Enum):
    EXPOSE = "expose"         # "I expose these state keys/capabilities"
    SUBSCRIBE = "subscribe"   # "Notify me when these keys change"
    READ = "read"             # "Send me current state for these keys"
    WRITE = "write"           # "I'm writing state to these keys"
    BROADCAST = "broadcast"   # "Attention all: here's something important"
    SWARM = "swarm"           # "I'm claiming/dropping/joining a task"
    DECAY = "decay"           # "This information is expiring"
    PING = "ping"             # "Are you alive?"
    PONG = "pong"             # "Yes"


@dataclass
class MembraneMessage:
    """A single message in the membrane protocol."""
    type: str
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str = ""
    to_agent: str = ""        # empty = broadcast to all
    key: str = ""             # state key path (e.g. "sensors.temp")
    value: Any = None
    ttl: float | None = None  # time-to-live in seconds
    priority: int = 0         # 0=normal, 1=high, 2=urgent
    permeability: str = "public"  # public | trusted | private
    tags: list[str] = field(default_factory=list)
    ts: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)
    
    @classmethod
    def from_json(cls, text: str) -> "MembraneMessage":
        d = json.loads(text)
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ── Protocol Handler ──

class ProtocolHandler:
    """
    Implements the membrane protocol.
    
    Each agent has one handler. Handlers communicate via a MessageBus.
    The handler manages subscriptions, permeability, and state.
    """
    
    def __init__(self, agent_id: str, trust: list[str] | None = None):
        self.agent_id = agent_id
        self._trust = set(trust or [])
        self._state: dict[str, Any] = {}         # key -> latest value
        self._subscriptions: set[str] = set()
        self._exposures: dict[str, str] = {}     # key -> permeability
        self._swarm_tasks: set[str] = set()      # task IDs this agent is part of
        self._bus = None  # set by the bus
        self._callbacks: dict[str, callable] = {} # event_type -> handler
    
    def set_bus(self, bus: "MessageBus"):
        self._bus = bus
    
    def register_callback(self, event_type: str, callback: callable):
        self._callbacks[event_type] = callback
    
    # ── Outbound Messages ──
    
    def send(self, msg: MembraneMessage):
        msg.from_agent = self.agent_id
        if self._bus:
            self._bus.deliver(msg)
    
    def expose(self, keys: list[str], permeability: str = "public"):
        for key in keys:
            self._exposures[key] = permeability
        self.send(MembraneMessage(
            type=MsgType.EXPOSE,
            key="|".join(keys),
            value=permeability,
        ))
    
    def subscribe(self, patterns: list[str]):
        self._subscriptions.update(patterns)
        self.send(MembraneMessage(
            type=MsgType.SUBSCRIBE,
            key="|".join(patterns),
        ))
    
    def read(self, key: str) -> list[MembraneMessage]:
        self.send(MembraneMessage(type=MsgType.READ, key=key))
        return []  # responses come as callbacks
    
    def write(self, key: str, value: Any, permeability: str = "public",
              ttl: float | None = None, tags: list[str] | None = None):
        self._state[key] = value
        self.send(MembraneMessage(
            type=MsgType.WRITE, key=key, value=value,
            permeability=permeability, ttl=ttl, tags=tags or [],
        ))
    
    def broadcast(self, message: str, target_pattern: str = "",
                  priority: int = 0):
        self.send(MembraneMessage(
            type=MsgType.BROADCAST, key=target_pattern,
            value=message, priority=priority,
        ))
    
    def join_swarm(self, task_id: str):
        self._swarm_tasks.add(task_id)
        self.send(MembraneMessage(
            type=MsgType.SWARM, key=task_id, value={"action": "join"},
        ))
    
    def leave_swarm(self, task_id: str):
        self._swarm_tasks.discard(task_id)
        self.send(MembraneMessage(
            type=MsgType.SWARM, key=task_id, value={"action": "leave"},
        ))
    
    # ── Inbound Processing ──
    
    def handle(self, msg: MembraneMessage):
        """Process an inbound message."""
        if msg.type == MsgType.WRITE and msg.from_agent != self.agent_id:
            if self._can_read(msg):
                for pattern in self._subscriptions:
                    if msg.key.startswith(pattern):
                        self._state[f"observed.{msg.key}"] = msg.value
                        self._invoke("on_write", msg)
                        break
        
        elif msg.type == MsgType.READ and msg.from_agent != self.agent_id:
            if msg.key in self._state and msg.key in self._exposures:
                perm = self._exposures.get(msg.key, "private")
                if perm == "public" or msg.from_agent in self._trust:
                    self.send(MembraneMessage(
                        type=MsgType.WRITE,  # response as write
                        to_agent=msg.from_agent,
                        key=msg.key,
                        value=self._state[msg.key],
                    ))
        
        elif msg.type == MsgType.BROADCAST and msg.from_agent != self.agent_id:
            self._invoke("on_broadcast", msg)
        
        elif msg.type == MsgType.SWARM and msg.from_agent != self.agent_id:
            self._invoke("on_swarm", msg)
        
        elif msg.type == MsgType.SUBSCRIBE and msg.from_agent != self.agent_id:
            self._invoke("on_subscribe", msg)
    
    def _can_read(self, msg: MembraneMessage) -> bool:
        if msg.permeability == "public":
            return True
        if msg.permeability == "trusted":
            return msg.from_agent in self._trust or self.agent_id in self._trust
        return msg.from_agent == self.agent_id
    
    def _invoke(self, event_type: str, msg: MembraneMessage):
        cb = self._callbacks.get(event_type)
        if cb:
            cb(msg)


class MessageBus:
    """
    Simple in-process message bus.
    In production, replace with NATS, Redis PubSub, or WebSocket relay.
    """
    
    def __init__(self):
        self._handlers: dict[str, ProtocolHandler] = {}
    
    def register(self, handler: ProtocolHandler):
        self._handlers[handler.agent_id] = handler
        handler.set_bus(self)
    
    def deliver(self, msg: MembraneMessage):
        if msg.to_agent:
            # Direct delivery
            h = self._handlers.get(msg.to_agent)
            if h:
                h.handle(msg)
        else:
            # Broadcast to all except sender
            for agent_id, h in self._handlers.items():
                if agent_id != msg.from_agent:
                    h.handle(msg)
    
    def list_agents(self) -> list[str]:
        return list(self._handlers.keys())


# ── Wire Format Examples ──

WIRE_FORMAT_DOCS = """
# Membrane Protocol — Wire Format

## Message Schema
```json
{
  "type": "expose|subscribe|read|write|broadcast|swarm|decay|ping|pong",
  "msg_id": "uuid-v4",
  "from_agent": "agent-id",
  "to_agent": "agent-id|\"\"",
  "key": "path.to.state",
  "value": "<any JSON>",
  "ttl": 60,
  "priority": 0,
  "permeability": "public|trusted|private",
  "tags": ["tag1", "tag2"],
  "ts": 1777235726.099,
  "metadata": {}
}
```

## Transport Options
- WebSocket: bidirectional streaming, lowest latency
- HTTP/3: simple, works through proxies
- gRPC: typed, efficient, streaming
- NATS: pub/sub at scale, jetstream persistence

## Key Conventions
- Keys use dot notation: `sensors.temp`, `task.status`, `shared.findings`
- Subscription patterns are prefix-based: `sensors.` matches all sensor keys
- TTL is optional; entries without TTL persist indefinitely
- `to_agent=""` means broadcast to all subscribers
"""


# ── Demo: Protocol conversation between 3 agents ──

def demo():
    print("=" * 60)
    print("SYNTHETIC MEMBRANE — Protocol Specification")
    print("=" * 60)
    
    bus = MessageBus()
    messages_log: list[str] = []
    
    # Create agents
    sensor = ProtocolHandler("sensor-01", trust=["analyzer-01"])
    analyzer = ProtocolHandler("analyzer-01", trust=["sensor-01"])
    actuator = ProtocolHandler("actuator-01")
    
    # Log all messages
    orig_deliver = bus.deliver
    def logged_deliver(msg):
        orig_deliver(msg)
        messages_log.append(msg.to_json())
    bus.deliver = logged_deliver
    
    bus.register(sensor)
    bus.register(analyzer)
    bus.register(actuator)
    
    print("\n--- Phase 1: Discovery & Registration ---")
    
    # Agents expose their capabilities
    sensor.expose(["sensors.temp", "sensors.humidity"], "public")
    sensor.subscribe(["__broadcast"])
    analyzer.expose(["analysis.anomalies"], "trusted")
    analyzer.subscribe(["sensors."])
    actuator.subscribe(["__broadcast", "actions."])
    
    print(f"Messages so far: {len(messages_log)}")
    for m in messages_log[:3]:
        msg = MembraneMessage.from_json(m)
        print(f"  {msg.from_agent} -> [{msg.type}] {msg.key}")
    
    print("\n--- Phase 2: Data Flow ---")
    
    # Sensor writes temperature
    sensor.write("sensors.temp", {"value": 42.5, "unit": "C"})
    print(f"  sensor-01 -> WRITE sensors.temp")
    
    # Analyzer reacts (via callback)
    received = []
    def on_write(msg):
        received.append(msg)
        if msg.key == "sensors.temp" and msg.value.get("value", 0) > 40:
            analyzer.write("analysis.anomalies",
                          {"alert": "HIGH_TEMP", "value": msg.value["value"]},
                          permeability="trusted")
            analyzer.broadcast("ANOMALY: temp exceeds threshold", priority=1)
    
    analyzer.register_callback("on_write", on_write)
    analyzer.register_callback("on_broadcast", lambda msg: print(f"    actuator received broadcast: {msg.value}"))
    actuator.register_callback("on_broadcast", lambda msg: print(f"    actuator received broadcast: {msg.value}"))
    
    # Re-run with callbacks registered
    messages_log.clear()
    sensor.write("sensors.temp", {"value": 42.5, "unit": "C"})
    
    print(f"  analyzer detected anomaly, wrote alert + broadcast")
    print(f"  Messages in this phase: {len(messages_log)}")
    
    print("\n--- Phase 3: Swarm Activation ---")
    
    # Analyzer detects critical situation, creates swarm
    analyzer.broadcast("CRITICAL: cooling failure detected, swarm needed", priority=2)
    analyzer.send(MembraneMessage(
        type=MsgType.SWARM, key="task.cooling-repair",
        value={"action": "create", "urgency": "critical"},
        priority=2,
    ))
    # Others join
    sensor.join_swarm("task.cooling-repair")
    actuator.join_swarm("task.cooling-repair")
    print(f"  Swarm 'task.cooling-repair' created with 3 members")
    
    print("\n--- Phase 4: Task Resolution & Dissolution ---")
    
    actuator.write("actions.cooling", {"status": "repairing", "agent": "actuator-01"})
    actuator.write("actions.cooling", {"status": "repaired", "agent": "actuator-01"})
    analyzer.write("analysis.anomalies", {"status": "resolved"})
    
    # Swarm dissolves
    sensor.leave_swarm("task.cooling-repair")
    actuator.leave_swarm("task.cooling-repair")
    analyzer.leave_swarm("task.cooling-repair")
    print(f"  Swarm dissolved, agents return to normal")
    
    print(f"\n--- Wire Format Sample ---")
    if messages_log:
        sample = json.loads(messages_log[0])
        print(json.dumps(sample, indent=2))
    
    print(f"\n--- Protocol Stats ---")
    print(f"  Total messages: {len(messages_log)}")
    print(f"  Agents: {bus.list_agents()}")
    
    print("\n" + WIRE_FORMAT_DOCS)
    print("=" * 60)


if __name__ == "__main__":
    demo()

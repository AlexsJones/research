"""
Data models for the Synthetic Membrane.

These models are CRDT-ready: each event carries a monotonic sequence number
and agent_id, enabling later upgrade to vector-clock or LWW-style resolution.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PermeabilityLevel(str, Enum):
    """Three-tier permeability control for exposed state."""

    PUBLIC = "public"       # Anyone can read
    TRUSTED = "trusted"     # Registered agents only
    PRIVATE = "private"     # Owner only


class EventType(str, Enum):
    """Types of events in the append-only event log."""

    AGENT_REGISTERED = "agent_registered"
    AGENT_UNREGISTERED = "agent_unregistered"
    STATE_EXPOSED = "state_exposed"
    STATE_RETRACTED = "state_retracted"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_REMOVED = "subscription_removed"
    BROADCAST_SENT = "broadcast_sent"
    BROADCAST_DELIVERED = "broadcast_delivered"
    SWARM_CREATED = "swarm_created"
    SWARM_JOINED = "swarm_joined"
    SWARM_LEFT = "swarm_left"
    SWARM_ACTIVATED = "swarm_activated"
    SWARM_DISSOLVED = "swarm_dissolved"
    SWARM_DEACTIVATED = "swarm_deactivated"


@dataclass
class Agent:
    """An agent registered with the membrane."""

    agent_id: str
    name: str
    capabilities: list[str] = field(default_factory=list)
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True


@dataclass
class Entry:
    """A piece of exposed state in the shared medium."""

    entry_id: str
    agent_id: str
    key: str
    value: Any
    permeability: PermeabilityLevel = PermeabilityLevel.PUBLIC
    exposed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True


@dataclass
class Subscription:
    """An agent's subscription to a state pattern."""

    subscription_id: str
    agent_id: str
    pattern: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Broadcast:
    """A broadcast message and its delivery receipts."""

    broadcast_id: str
    agent_id: str
    message: str
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    recipients: list[str] = field(default_factory=list)


@dataclass
class Swarm:
    """A quorum-sensing swarm."""

    swarm_id: str
    name: str
    capability_required: str
    threshold: int
    members: list[str] = field(default_factory=list)
    active: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Event:
    """An event in the append-only event log.

    CRDT-ready design:
    - `seq` provides a total order (Lamport clock or physical clock).
    - `agent_id` identifies the originator for conflict resolution.
    - `timestamp` enables time-based queries and replay.
    - `payload` is an opaque dict — each event type defines its own schema.

    For Phase 2 CRDT support, `seq` can be replaced with vector clocks,
    and `payload` can carry mergeable state deltas.
    """

    event_id: str
    seq: int
    agent_id: str
    event_type: EventType
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = field(default_factory=dict)

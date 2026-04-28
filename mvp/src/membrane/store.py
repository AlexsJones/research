"""
Event-sourced in-memory store for the Synthetic Membrane.

Provides the shared medium — the "cytoplasm" between agents.
Append-only event log with materialized current state.
CRDT-ready: each event carries a monotonic sequence number.
"""

from __future__ import annotations

import fnmatch
import uuid
from datetime import datetime, timezone
from typing import Any

from membrane.models import (
    Agent,
    Broadcast,
    Entry,
    Event,
    EventType,
    PermeabilityLevel,
    Swarm,
    Subscription,
)


class MembraneStore:
    """In-memory event-sourced store for the membrane shared medium.

    Architecture:
    - Append-only event log (list of Events) — the source of truth
    - Materialized state indices for efficient queries:
      * agents: dict of registered agents
      * entries: dict of active state entries
      * subscriptions: dict of active subscriptions
      * broadcasts: list of broadcast messages
      * swarms: dict of swarms

    The materialized state is rebuilt from events on replay.
    For Phase 2, this becomes a persistent store (SQLite) with CRDT support.
    """

    def __init__(self):
        self._seq: int = 0
        self.events: list[Event] = []

        # Materialized state
        self.agents: dict[str, Agent] = {}
        self.entries: dict[str, Entry] = {}
        self.subscriptions: dict[str, Subscription] = {}
        self.broadcasts: list[Broadcast] = []
        self.swarms: dict[str, Swarm] = {}

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def _emit(self, agent_id: str, event_type: EventType, payload: dict[str, Any] | None = None) -> Event:
        event = Event(
            event_id=str(uuid.uuid4()),
            seq=self._next_seq(),
            agent_id=agent_id,
            event_type=event_type,
            payload=payload or {},
        )
        self.events.append(event)
        return event

    def replay(self, events: list[Event]) -> None:
        """Rebuild materialized state from a list of events. Used for recovery."""
        for event in events:
            self._apply_event(event)

    def _apply_event(self, event: Event) -> None:
        """Apply a single event to materialized state."""
        p = event.payload

        if event.event_type == EventType.AGENT_REGISTERED:
            self.agents[event.agent_id] = Agent(
                agent_id=event.agent_id,
                name=p.get("name", event.agent_id),
                capabilities=p.get("capabilities", []),
                registered_at=event.timestamp,
            )

        elif event.event_type == EventType.AGENT_UNREGISTERED:
            if event.agent_id in self.agents:
                self.agents[event.agent_id].active = False
            # Clean up their entries
            for entry in list(self.entries.values()):
                if entry.agent_id == event.agent_id:
                    entry.active = False
            # Remove subscriptions
            for sub in list(self.subscriptions.values()):
                if sub.agent_id == event.agent_id:
                    del self.subscriptions[sub.subscription_id]

        elif event.event_type == EventType.STATE_EXPOSED:
            self.entries[p["entry_id"]] = Entry(
                entry_id=p["entry_id"],
                agent_id=event.agent_id,
                key=p["key"],
                value=p["value"],
                permeability=PermeabilityLevel(p["permeability"]),
                exposed_at=event.timestamp,
            )

        elif event.event_type == EventType.STATE_RETRACTED:
            eid = p.get("entry_id")
            if eid in self.entries:
                self.entries[eid].active = False

        elif event.event_type == EventType.SUBSCRIPTION_CREATED:
            self.subscriptions[p["subscription_id"]] = Subscription(
                subscription_id=p["subscription_id"],
                agent_id=event.agent_id,
                pattern=p["pattern"],
                created_at=event.timestamp,
            )

        elif event.event_type == EventType.SUBSCRIPTION_REMOVED:
            sid = p.get("subscription_id")
            if sid in self.subscriptions:
                del self.subscriptions[sid]

        elif event.event_type == EventType.BROADCAST_SENT:
            self.broadcasts.append(Broadcast(
                broadcast_id=p["broadcast_id"],
                agent_id=event.agent_id,
                message=p["message"],
                sent_at=event.timestamp,
                recipients=p.get("recipients", []),
            ))

        elif event.event_type == EventType.SWARM_CREATED:
            self.swarms[p["swarm_id"]] = Swarm(
                swarm_id=p["swarm_id"],
                name=p["name"],
                capability_required=p["capability_required"],
                threshold=p["threshold"],
                created_at=event.timestamp,
            )

        elif event.event_type == EventType.SWARM_JOINED:
            swarm = self.swarms.get(p["swarm_id"])
            if swarm and event.agent_id not in swarm.members:
                swarm.members.append(event.agent_id)
                if len(swarm.members) >= swarm.threshold and not swarm.active:
                    swarm.active = True
                    self._emit("system", EventType.SWARM_ACTIVATED, {
                        "swarm_id": swarm.swarm_id,
                        "members": swarm.members[:],
                    })

        elif event.event_type == EventType.SWARM_LEFT:
            swarm = self.swarms.get(p["swarm_id"])
            if swarm and event.agent_id in swarm.members:
                swarm.members.remove(event.agent_id)
                if len(swarm.members) < swarm.threshold and swarm.active:
                    swarm.active = False
                    self._emit("system", EventType.SWARM_DEACTIVATED, {
                        "swarm_id": swarm.swarm_id,
                    })

        elif event.event_type == EventType.SWARM_DISSOLVED:
            swarm = self.swarms.get(p["swarm_id"])
            if swarm:
                swarm.members.clear()
                swarm.active = False

    # ── Public API ──────────────────────────────────────────────

    def register_agent(self, agent_id: str, name: str, capabilities: list[str]) -> Event:
        """Register an agent with the membrane."""
        event = self._emit(agent_id, EventType.AGENT_REGISTERED, {
            "name": name,
            "capabilities": capabilities,
        })
        self._apply_event(event)
        return event

    def unregister_agent(self, agent_id: str) -> Event:
        """Unregister an agent (e.g., on disconnect)."""
        event = self._emit(agent_id, EventType.AGENT_UNREGISTERED)
        self._apply_event(event)
        return event

    def expose(self, agent_id: str, key: str, value: Any, permeability: str = PermeabilityLevel.PUBLIC) -> tuple[Event, Entry]:
        """Expose a piece of state to the shared medium."""
        entry_id = str(uuid.uuid4())
        entry = Entry(
            entry_id=entry_id,
            agent_id=agent_id,
            key=key,
            value=value,
            permeability=PermeabilityLevel(permeability),
        )
        event = self._emit(agent_id, EventType.STATE_EXPOSED, {
            "entry_id": entry_id,
            "key": key,
            "value": value,
            "permeability": permeability,
        })
        self._apply_event(event)
        return event, entry

    def retract(self, agent_id: str, entry_id: str) -> Event:
        """Retract (deactivate) an exposed state entry."""
        event = self._emit(agent_id, EventType.STATE_RETRACTED, {
            "entry_id": entry_id,
        })
        self._apply_event(event)
        return event

    def query(self, reader_id: str, pattern: str, permeability: str | None = None) -> list[Entry]:
        """Query the shared state for entries matching a pattern.

        Args:
            reader_id: The agent doing the query (for permeability checks)
            pattern: Glob pattern to match against entry keys
            permeability: Optional filter by permeability level

        Returns:
            List of active entries matching the pattern and permeability
        """
        reader = self.agents.get(reader_id)

        results = []
        for entry in self.entries.values():
            if not entry.active:
                continue
            if not fnmatch.fnmatch(entry.key, pattern):
                continue

            # Permeability check
            if entry.permeability == PermeabilityLevel.PRIVATE:
                if reader_id != entry.agent_id:
                    continue
            elif entry.permeability == PermeabilityLevel.TRUSTED:
                if reader is None:
                    continue

            if permeability and entry.permeability.value != permeability:
                continue

            results.append(entry)

        return results

    def subscribe(self, agent_id: str, pattern: str) -> tuple[Event, Subscription]:
        """Subscribe to state changes matching a pattern."""
        sub_id = str(uuid.uuid4())
        sub = Subscription(subscription_id=sub_id, agent_id=agent_id, pattern=pattern)
        event = self._emit(agent_id, EventType.SUBSCRIPTION_CREATED, {
            "subscription_id": sub_id,
            "pattern": pattern,
        })
        self._apply_event(event)
        return event, sub

    def broadcast(self, agent_id: str, message: str) -> tuple[Event, Broadcast]:
        """Broadcast a message to all registered agents."""
        recipients = [a.agent_id for a in self.agents.values() if a.active and a.agent_id != agent_id]
        bcast_id = str(uuid.uuid4())
        bcast = Broadcast(broadcast_id=bcast_id, agent_id=agent_id, message=message, recipients=recipients)
        event = self._emit(agent_id, EventType.BROADCAST_SENT, {
            "broadcast_id": bcast_id,
            "message": message,
            "recipients": recipients,
        })
        self._apply_event(event)

        # Deliver to recipients
        for target_id in recipients:
            self._emit(target_id, EventType.BROADCAST_DELIVERED, {
                "broadcast_id": bcast_id,
                "from": agent_id,
                "message": message,
            })

        return event, bcast

    def get_events(self, since_seq: int = 0) -> list[Event]:
        """Get events since a given sequence number (for incremental sync)."""
        return [e for e in self.events if e.seq > since_seq]

    def get_stats(self) -> dict[str, Any]:
        """Get store statistics."""
        return {
            "total_events": len(self.events),
            "registered_agents": len([a for a in self.agents.values() if a.active]),
            "active_entries": len([e for e in self.entries.values() if e.active]),
            "active_subscriptions": len(self.subscriptions),
            "broadcasts": len(self.broadcasts),
            "active_swarms": len([s for s in self.swarms.values() if s.active]),
            "last_seq": self._seq,
        }

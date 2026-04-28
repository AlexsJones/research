"""
Quorum-sensing swarm engine for the Synthetic Membrane.

Agents emit capability signals. When enough agents with the required
capability register, a swarm activates automatically. Swarms dissolve
when members drop below the threshold.

Biologically inspired by bacterial quorum sensing — the membrane's
coordination layer for emergent collaboration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from membrane.models import Event, EventType, Swarm


@dataclass
class SwarmSignal:
    """A signal emitted by an agent for quorum sensing."""

    signal_id: str
    agent_id: str
    capability: str
    strength: float = 1.0  # Signal strength (concentration)
    emitted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    decay_rate: float = 0.0  # Per-second decay (0.0 = no decay)


class SwarmEngine:
    """Manages quorum-sensing swarms on top of the membrane store.

    Lifecycle:
    1. swarm_create(name, capability, threshold) — Define a swarm
    2. swarm_join(swarm_id, agent_id) — Agent joins with required capability
    3. When member count >= threshold → swarm ACTIVATES
    4. When member count < threshold → swarm DEACTIVATES
    5. swarm_dissolve(swarm_id) — Explicit dissolution

    Signals:
    - SWARM_CREATED → when a swarm is defined
    - SWARM_JOINED → when an agent joins
    - SWARM_LEFT → when an agent leaves
    - SWARM_ACTIVATED → when threshold is crossed upward
    - SWARM_DEACTIVATED → when threshold is crossed downward
    - SWARM_DISSOLVED → when explicitly dissolved

    For Phase 2, this integrates with:
    - Signal decay (biological quorum sensing)
    - Capability-based membership filtering
    - Swarm communication channels (swarm-local broadcasts)
    """

    def __init__(self, store: Any):
        """Initialize with a MembraneStore reference."""
        self._store = store
        self.signals: list[SwarmSignal] = []

    def create_swarm(
        self,
        name: str,
        capability_required: str,
        threshold: int,
    ) -> tuple[Event, Swarm]:
        """Create a new quorum-sensing swarm.

        Args:
            name: Human-readable swarm name
            capability_required: Agents must have this capability to join
            threshold: Minimum members needed for activation

        Returns:
            (Event, Swarm) tuple
        """
        swarm = Swarm(
            swarm_id=f"swarm_{len(self._store.swarms) + 1}",
            name=name,
            capability_required=capability_required,
            threshold=threshold,
        )
        event = self._store._emit(
            "system",
            EventType.SWARM_CREATED,
            {
                "swarm_id": swarm.swarm_id,
                "name": name,
                "capability_required": capability_required,
                "threshold": threshold,
            },
        )
        self._store._apply_event(event)
        return event, swarm

    def join_swarm(self, swarm_id: str, agent_id: str) -> tuple[Event, Swarm | None]:
        """Join a swarm. Agent must have the required capability.

        Args:
            swarm_id: The swarm to join
            agent_id: The agent joining

        Returns:
            (Event, Swarm) tuple, or (Event, None) if join denied
        """
        swarm = self._store.swarms.get(swarm_id)
        if swarm is None:
            return self._store._emit(agent_id, EventType.SWARM_JOINED, {
                "swarm_id": swarm_id,
                "denied": "swarm not found",
            }), None

        agent = self._store.agents.get(agent_id)
        if agent is None or not agent.active:
            return self._store._emit(agent_id, EventType.SWARM_JOINED, {
                "swarm_id": swarm_id,
                "denied": "agent not registered",
            }), None

        if swarm.capability_required and swarm.capability_required not in agent.capabilities:
            return self._store._emit(agent_id, EventType.SWARM_JOINED, {
                "swarm_id": swarm_id,
                "denied": f"missing capability: {swarm.capability_required}",
            }), None

        if agent_id in swarm.members:
            return None, swarm  # Already a member

        event = self._store._emit(agent_id, EventType.SWARM_JOINED, {
            "swarm_id": swarm_id,
        })
        self._store._apply_event(event)
        return event, self._store.swarms.get(swarm_id)

    def leave_swarm(self, swarm_id: str, agent_id: str) -> Event | None:
        """Leave a swarm."""
        swarm = self._store.swarms.get(swarm_id)
        if swarm is None or agent_id not in swarm.members:
            return None

        event = self._store._emit(agent_id, EventType.SWARM_LEFT, {
            "swarm_id": swarm_id,
        })
        self._store._apply_event(event)
        return event

    def dissolve_swarm(self, swarm_id: str) -> Event | None:
        """Explicitly dissolve a swarm."""
        swarm = self._store.swarms.get(swarm_id)
        if swarm is None:
            return None

        event = self._store._emit("system", EventType.SWARM_DISSOLVED, {
            "swarm_id": swarm_id,
        })
        self._store._apply_event(event)
        return event

    def emit_signal(
        self,
        agent_id: str,
        capability: str,
        strength: float = 1.0,
        decay_rate: float = 0.0,
    ) -> SwarmSignal:
        """Emit a quorum-sensing signal (capability advertisement).

        Args:
            agent_id: The agent emitting the signal
            capability: The capability being signaled
            strength: Signal strength (like chemical concentration)
            decay_rate: Per-second decay rate (0.0 = no decay)

        Returns:
            SwarmSignal
        """
        import uuid
        signal = SwarmSignal(
            signal_id=str(uuid.uuid4()),
            agent_id=agent_id,
            capability=capability,
            strength=strength,
            decay_rate=decay_rate,
        )
        self.signals.append(signal)
        return signal

    def get_active_swarms(self) -> list[Swarm]:
        """Get all active swarms."""
        return [s for s in self._store.swarms.values() if s.active]

    def get_swarm_info(self, swarm_id: str) -> dict[str, Any] | None:
        """Get detailed swarm information."""
        swarm = self._store.swarms.get(swarm_id)
        if swarm is None:
            return None
        return {
            "swarm_id": swarm.swarm_id,
            "name": swarm.name,
            "capability_required": swarm.capability_required,
            "threshold": swarm.threshold,
            "members": swarm.members[:],
            "member_count": len(swarm.members),
            "active": swarm.active,
            "created_at": swarm.created_at.isoformat(),
        }

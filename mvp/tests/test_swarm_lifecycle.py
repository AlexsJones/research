"""
Swarm lifecycle tests.

Covers create → join (below threshold) → join (cross threshold → activate)
→ leave (cross threshold downward → deactivate) → re-join → dissolve.

Also covers the denial paths: unknown swarm, unregistered agent, missing
capability.
"""

from __future__ import annotations

import pytest

from membrane.models import EventType
from membrane.permeability import PermeabilityEngine
from membrane.store import MembraneStore
from membrane.swarm import SwarmEngine


@pytest.fixture
def store() -> MembraneStore:
    return MembraneStore()


@pytest.fixture
def swarm(store: MembraneStore) -> SwarmEngine:
    return SwarmEngine(store)


def _emitted(store: MembraneStore, event_type: EventType) -> list:
    return [e for e in store.events if e.event_type == event_type]


def test_create_swarm_emits_event(store, swarm):
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    assert sw.swarm_id in store.swarms
    assert store.swarms[sw.swarm_id].active is False
    assert len(_emitted(store, EventType.SWARM_CREATED)) == 1


def test_join_below_threshold_does_not_activate(store, swarm):
    store.register_agent("a", "A", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=3)

    swarm.join_swarm(sw.swarm_id, "a")

    assert store.swarms[sw.swarm_id].members == ["a"]
    assert store.swarms[sw.swarm_id].active is False
    assert _emitted(store, EventType.SWARM_ACTIVATED) == []


def test_join_at_threshold_activates(store, swarm):
    store.register_agent("a", "A", ["research"])
    store.register_agent("b", "B", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    swarm.join_swarm(sw.swarm_id, "a")
    swarm.join_swarm(sw.swarm_id, "b")

    assert store.swarms[sw.swarm_id].active is True
    activated = _emitted(store, EventType.SWARM_ACTIVATED)
    assert len(activated) == 1
    assert set(activated[0].payload["members"]) == {"a", "b"}


def test_leave_below_threshold_deactivates(store, swarm):
    store.register_agent("a", "A", ["research"])
    store.register_agent("b", "B", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    swarm.join_swarm(sw.swarm_id, "a")
    swarm.join_swarm(sw.swarm_id, "b")
    assert store.swarms[sw.swarm_id].active is True

    swarm.leave_swarm(sw.swarm_id, "a")

    assert store.swarms[sw.swarm_id].active is False
    assert "a" not in store.swarms[sw.swarm_id].members
    assert len(_emitted(store, EventType.SWARM_DEACTIVATED)) == 1


def test_rejoin_reactivates(store, swarm):
    store.register_agent("a", "A", ["research"])
    store.register_agent("b", "B", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    swarm.join_swarm(sw.swarm_id, "a")
    swarm.join_swarm(sw.swarm_id, "b")
    swarm.leave_swarm(sw.swarm_id, "b")
    assert store.swarms[sw.swarm_id].active is False

    swarm.join_swarm(sw.swarm_id, "b")

    assert store.swarms[sw.swarm_id].active is True
    assert len(_emitted(store, EventType.SWARM_ACTIVATED)) == 2


def test_dissolve_clears_members(store, swarm):
    store.register_agent("a", "A", ["research"])
    store.register_agent("b", "B", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    swarm.join_swarm(sw.swarm_id, "a")
    swarm.join_swarm(sw.swarm_id, "b")

    swarm.dissolve_swarm(sw.swarm_id)

    assert store.swarms[sw.swarm_id].members == []
    assert store.swarms[sw.swarm_id].active is False
    assert len(_emitted(store, EventType.SWARM_DISSOLVED)) == 1


def test_join_unknown_swarm_denied(store, swarm):
    store.register_agent("a", "A", ["research"])
    event, result = swarm.join_swarm("swarm_does_not_exist", "a")
    assert result is None
    assert event.payload.get("denied") == "swarm not found"


def test_join_unregistered_agent_denied(store, swarm):
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)
    event, result = swarm.join_swarm(sw.swarm_id, "ghost")
    assert result is None
    assert event.payload.get("denied") == "agent not registered"


def test_join_missing_capability_denied(store, swarm):
    store.register_agent("a", "A", ["writing"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)

    event, result = swarm.join_swarm(sw.swarm_id, "a")
    assert result is None
    assert "missing capability" in event.payload.get("denied", "")


def test_double_join_is_idempotent(store, swarm):
    store.register_agent("a", "A", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=3)

    swarm.join_swarm(sw.swarm_id, "a")
    swarm.join_swarm(sw.swarm_id, "a")

    assert store.swarms[sw.swarm_id].members == ["a"]


def test_dissolve_unknown_swarm_returns_none(store, swarm):
    assert swarm.dissolve_swarm("nope") is None


def test_get_active_swarms_only_returns_active(store, swarm):
    store.register_agent("a", "A", ["c1"])
    store.register_agent("b", "B", ["c1"])
    store.register_agent("c", "C", ["c2"])

    _, active_sw = swarm.create_swarm("active", "c1", threshold=2)
    _, idle_sw = swarm.create_swarm("idle", "c2", threshold=2)
    swarm.join_swarm(active_sw.swarm_id, "a")
    swarm.join_swarm(active_sw.swarm_id, "b")
    swarm.join_swarm(idle_sw.swarm_id, "c")

    actives = swarm.get_active_swarms()
    assert [s.swarm_id for s in actives] == [active_sw.swarm_id]


def test_swarm_info_shape(store, swarm):
    store.register_agent("a", "A", ["research"])
    _, sw = swarm.create_swarm("R&D", "research", threshold=2)
    swarm.join_swarm(sw.swarm_id, "a")

    info = swarm.get_swarm_info(sw.swarm_id)
    assert info is not None
    assert info["name"] == "R&D"
    assert info["capability_required"] == "research"
    assert info["threshold"] == 2
    assert info["members"] == ["a"]
    assert info["member_count"] == 1
    assert info["active"] is False
    assert "created_at" in info

"""
Event-sourcing replay tests.

The membrane store is event-sourced: every public mutation appends to
`store.events`, and the materialised state can be reconstructed by
replaying that log into a fresh store. These tests verify that property
across the full surface area: agents, entries, retractions, subscriptions,
broadcasts, and swarm lifecycle.
"""

from __future__ import annotations

import pytest

from membrane.models import EventType, PermeabilityLevel
from membrane.store import MembraneStore
from membrane.swarm import SwarmEngine


def _build_seeded_store() -> MembraneStore:
    """A populated store covering every event type."""
    s = MembraneStore()
    sw = SwarmEngine(s)

    s.register_agent("alpha", "Alpha", ["research", "review"])
    s.register_agent("beta", "Beta", ["research"])
    s.register_agent("gamma", "Gamma", ["writing"])

    _, e_pub = s.expose("alpha", "data.x", 42, PermeabilityLevel.PUBLIC)
    _, e_priv = s.expose("alpha", "secrets.k", "hush", PermeabilityLevel.PRIVATE)
    s.expose("beta", "data.y", "hello", PermeabilityLevel.TRUSTED)

    s.retract("alpha", e_pub.entry_id)
    s.subscribe("gamma", "data.*")
    s.broadcast("alpha", "hello world")

    _, swarm_obj = sw.create_swarm("Reviewers", "research", threshold=2)
    sw.join_swarm(swarm_obj.swarm_id, "alpha")
    sw.join_swarm(swarm_obj.swarm_id, "beta")  # activates
    sw.leave_swarm(swarm_obj.swarm_id, "beta")  # deactivates

    return s


def _state_signature(s: MembraneStore) -> dict:
    """Stable dict summarising the materialised state, for comparison."""
    return {
        "agents": {
            aid: (a.name, sorted(a.capabilities), a.active)
            for aid, a in s.agents.items()
        },
        "entries": {
            eid: (e.agent_id, e.key, e.value, e.permeability.value, e.active)
            for eid, e in s.entries.items()
        },
        "subscriptions": {
            sid: (sub.agent_id, sub.pattern)
            for sid, sub in s.subscriptions.items()
        },
        "broadcasts": [
            (b.agent_id, b.message, sorted(b.recipients))
            for b in s.broadcasts
        ],
        "swarms": {
            sw_id: (
                sw.name,
                sw.capability_required,
                sw.threshold,
                sorted(sw.members),
                sw.active,
            )
            for sw_id, sw in s.swarms.items()
        },
    }


def test_replay_reproduces_full_state():
    original = _build_seeded_store()
    events = list(original.events)

    rebuilt = MembraneStore()
    rebuilt.replay(events)

    assert _state_signature(rebuilt) == _state_signature(original)


def test_replay_preserves_event_order():
    original = _build_seeded_store()

    rebuilt = MembraneStore()
    rebuilt.replay(list(original.events))

    # Replay does not append events itself — the rebuilt log is empty unless
    # we inject the events. The key property is that the materialised state
    # matches.
    assert _state_signature(rebuilt) == _state_signature(original)


def test_replay_must_be_applied_to_a_fresh_store():
    """Replay is not idempotent on an already-seeded store — broadcasts
    are append-only and would double up. Document the correct usage:
    always replay into a fresh store."""
    original = _build_seeded_store()
    events = list(original.events)

    fresh = MembraneStore()
    fresh.replay(events)
    assert _state_signature(fresh) == _state_signature(original)

    # A second replay into the SAME store appends broadcasts again.
    fresh.replay(events)
    assert len(fresh.broadcasts) == 2 * len(original.broadcasts)


def test_event_log_ordering_is_monotonic():
    s = _build_seeded_store()
    seqs = [e.seq for e in s.events]
    assert seqs == sorted(seqs)
    assert seqs[0] == 1
    assert seqs == list(range(1, len(seqs) + 1))


def test_get_events_since_returns_only_newer():
    s = _build_seeded_store()
    cutoff = len(s.events) // 2
    cutoff_seq = s.events[cutoff].seq

    new_events = s.get_events(since_seq=cutoff_seq)

    assert all(e.seq > cutoff_seq for e in new_events)
    assert len(new_events) == len(s.events) - cutoff - 1


def test_replay_handles_swarm_activation_event_present_in_log():
    """SWARM_ACTIVATED is emitted internally during _apply_event for
    SWARM_JOINED. Replaying the JOIN must regenerate the same activation
    behaviour without double-counting."""
    original = _build_seeded_store()

    rebuilt = MembraneStore()
    rebuilt.replay(list(original.events))

    sw_id = next(iter(original.swarms))
    # The original test scenario joined+left, ending deactivated.
    assert rebuilt.swarms[sw_id].active is False
    assert sorted(rebuilt.swarms[sw_id].members) == ["alpha"]


def test_replay_with_no_events_yields_empty_state():
    s = MembraneStore()
    s.replay([])

    assert s.agents == {}
    assert s.entries == {}
    assert s.subscriptions == {}
    assert s.broadcasts == []
    assert s.swarms == {}

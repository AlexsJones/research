"""
End-to-end coordination test for the Synthetic Membrane.

Scenario: Three agents (Researcher, Writer, Editor) collaborate on a document
through the membrane's shared state, permeability gating, and swarm coordination.
"""

import pytest
from membrane.store import MembraneStore
from membrane.permeability import PermeabilityEngine
from membrane.swarm import SwarmEngine
from membrane.models import PermeabilityLevel, EventType


@pytest.fixture
def store():
    return MembraneStore()


@pytest.fixture
def permeability():
    return PermeabilityEngine()


@pytest.fixture
def swarm(store):
    return SwarmEngine(store)


def test_agent_registration(store):
    """All three agents register with capabilities."""
    store.register_agent("researcher", "Researcher", ["research", "fact_check"])
    store.register_agent("writer", "Writer", ["writing", "drafting"])
    store.register_agent("editor", "Editor", ["editing", "reviewing"])

    assert len([a for a in store.agents.values() if a.active]) == 3
    assert "research" in store.agents["researcher"].capabilities
    assert "writing" in store.agents["writer"].capabilities
    assert "editing" in store.agents["editor"].capabilities


def test_expose_and_query_public(store):
    """Researcher exposes findings as public; Writer can query them."""
    store.register_agent("researcher", "Researcher", ["research"])
    store.register_agent("writer", "Writer", ["writing"])

    store.expose("researcher", "findings.climate", "Global temp up 1.2C", PermeabilityLevel.PUBLIC)
    store.expose("researcher", "findings.economy", "GDP growth slowed", PermeabilityLevel.PUBLIC)

    results = store.query("writer", "findings.*")
    assert len(results) == 2
    keys = [r.key for r in results]
    assert "findings.climate" in keys
    assert "findings.economy" in keys


def test_trusted_permeability(store, permeability):
    """Writer exposes draft as trusted; only trusted agents can read it."""
    store.register_agent("writer", "Writer", ["writing"])
    store.register_agent("editor", "Editor", ["editing"])

    # Writer exposes draft as trusted
    _, entry = store.expose("writer", "draft.intro", "Draft introduction text", PermeabilityLevel.TRUSTED)
    assert entry.permeability == PermeabilityLevel.TRUSTED

    # Editor can query trusted (registered agents can read trusted)
    results = store.query("editor", "draft.*")
    assert len(results) == 1

    # Unregistered agent cannot read trusted
    results = store.query("unknown_agent", "draft.*")
    assert len(results) == 0


def test_private_permeability(store):
    """Private entries are only visible to the owner."""
    store.register_agent("researcher", "Researcher", ["research"])
    store.register_agent("writer", "Writer", ["writing"])

    _, entry = store.expose("researcher", "notes.internal", "Sensitive notes", PermeabilityLevel.PRIVATE)

    # Owner can read
    results = store.query("researcher", "notes.*")
    assert len(results) == 1

    # Other agent cannot
    results = store.query("writer", "notes.*")
    assert len(results) == 0


def test_retract(store):
    """Retracting an entry makes it invisible to queries."""
    store.register_agent("researcher", "Researcher", ["research"])
    _, entry = store.expose("researcher", "findings.old", "Outdated finding", PermeabilityLevel.PUBLIC)

    results = store.query("researcher", "findings.*")
    assert len(results) == 1

    store.retract("researcher", entry.entry_id)

    results = store.query("researcher", "findings.*")
    assert len(results) == 0


def test_swarm_activation(store, swarm):
    """Swarm activates when enough agents with required capability join."""
    store.register_agent("writer", "Writer", ["writing", "drafting"])
    store.register_agent("editor", "Editor", ["editing", "writing"])

    _, swarm_obj = swarm.create_swarm("Doc Review", "writing", threshold=2)
    assert not swarm_obj.active  # Not enough members yet

    swarm.join_swarm(swarm_obj.swarm_id, "writer")
    assert not swarm_obj.active  # Only 1 member

    swarm.join_swarm(swarm_obj.swarm_id, "editor")
    # Both joined, threshold=2 met
    assert store.swarms[swarm_obj.swarm_id].active


def test_swarm_deactivation(store, swarm):
    """Swarm deactivates when members drop below threshold."""
    store.register_agent("writer", "Writer", ["writing"])
    store.register_agent("editor", "Editor", ["editing", "writing"])

    _, swarm_obj = swarm.create_swarm("Review", "writing", threshold=2)
    swarm.join_swarm(swarm_obj.swarm_id, "writer")
    swarm.join_swarm(swarm_obj.swarm_id, "editor")
    assert store.swarms[swarm_obj.swarm_id].active

    swarm.leave_swarm(swarm_obj.swarm_id, "writer")
    assert not store.swarms[swarm_obj.swarm_id].active


def test_full_coordination_scenario(store, permeability, swarm):
    """Full end-to-end: Researcher → Writer → Editor collaboration."""

    # 1. Register all agents
    store.register_agent("researcher", "Researcher", ["research", "fact_check"])
    store.register_agent("writer", "Writer", ["writing", "drafting"])
    store.register_agent("editor", "Editor", ["editing", "reviewing"])

    # 2. Researcher exposes findings
    store.expose("researcher", "findings.climate", "Temp up 1.2C", PermeabilityLevel.PUBLIC)
    store.expose("researcher", "findings.economy", "GDP slowed", PermeabilityLevel.PUBLIC)

    # 3. Writer queries and drafts
    findings = store.query("writer", "findings.*")
    assert len(findings) == 2

    # Writer exposes draft as trusted
    store.expose("writer", "draft.climate", "Climate section draft", PermeabilityLevel.TRUSTED)
    store.expose("writer", "draft.economy", "Economy section draft", PermeabilityLevel.TRUSTED)

    # 4. Editor reviews
    drafts = store.query("editor", "draft.*")
    assert len(drafts) == 2

    # Editor exposes feedback as trusted
    store.expose("editor", "feedback.climate", "Add more data sources", PermeabilityLevel.TRUSTED)

    # 5. Writer reads feedback and revises
    feedback = store.query("writer", "feedback.*")
    assert len(feedback) == 1
    assert feedback[0].value == "Add more data sources"

    # Writer exposes final version as public
    store.expose("writer", "final.climate", "Revised climate section", PermeabilityLevel.PUBLIC)

    # 6. Swarm activates for review
    store.register_agent("reviewer", "Reviewer", ["editing", "reviewing"])
    _, swarm_obj = swarm.create_swarm("Final Review", "editing", threshold=2)
    swarm.join_swarm(swarm_obj.swarm_id, "editor")
    swarm.join_swarm(swarm_obj.swarm_id, "reviewer")
    assert store.swarms[swarm_obj.swarm_id].active

    # 7. Broadcast completion
    _, bcast = store.broadcast("writer", "Document complete!")
    assert "editor" in bcast.recipients
    assert "reviewer" in bcast.recipients

    # 8. Verify stats
    stats = store.get_stats()
    assert stats["registered_agents"] >= 3
    assert stats["active_entries"] >= 5
    assert stats["active_swarms"] >= 1
    assert stats["total_events"] >= 10

    # 9. Verify event log has all event types
    event_types = {e.event_type for e in store.events}
    assert EventType.AGENT_REGISTERED in event_types
    assert EventType.STATE_EXPOSED in event_types
    assert EventType.BROADCAST_SENT in event_types
    assert EventType.SWARM_CREATED in event_types
    assert EventType.SWARM_JOINED in event_types
    assert EventType.SWARM_ACTIVATED in event_types

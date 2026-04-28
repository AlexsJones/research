---
title: Event Sourcing for Agent Coordination
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [event-sourcing, shared-state, architecture, pattern]
sources: []
confidence: medium
---

# Event Sourcing for Agent Coordination

## What Is Event Sourcing?

Event sourcing is a pattern where state changes are captured as an immutable, append-only log of events. Rather than storing just the current state, you store every change that led to it. The current state is derived by replaying events.

Used in: Axon Framework, EventStoreDB, CQRS architectures, financial systems, audit trails.

## Why Event Sourcing for the Membrane?

The membrane's Layer 2 (Shared Medium) could be implemented as an event log rather than a document store:

- **Full audit trail**: Every agent's every write is recorded with timestamp, identity, and content
- **Replayability**: New agents can replay the event log to understand context
- **Natural provenance**: Events carry the "who, when, what" of every state change
- **Conflict detection**: Divergent events from different agents are visible
- **Undo/recovery**: Corrupted state can be restored by replaying to a clean point
- **Combines with CRDTs**: Events can be CRDT operations, getting both audit trail and convergence

## Mapping to Membrane Layers

### Layer 0: Trust & Identity
Each event is signed by the writing agent's key. Events carry agent identity, capability claims, and reputation score at time of write.

### Layer 1: Permeability
Subscribe/unsubscribe operates on event *types* or *tags*, not just raw data. An agent says: "notify me on events matching [pattern]."

### Layer 2: Shared Medium as Event Log
- The membrane *is* the event log
- Agents project views from the log (their own materialized state)
- [[mesh-memory-protocol]]'s CMBs are events in this log
- [[cognitive-digestion]] remix becomes: agent projects its own interpretation from raw events
- Lineage tracking = event correlation IDs

### Layer 3: Coordination
- Task broadcasting = publishing a TASK event
- Task claiming = publishing a CLAIM event with agent ID
- Quorum detection = counting events matching threshold
- Swarm dissolution = publishing a DISSOLVE event

## Advantages Over Document Stores

| | Document Store (CRDT) | Event Log |
|---|---|---|
| Auditability | Limited (diff snapshots) | Full (every change recorded) |
| Replay | No | Yes (replay from any point) |
| Conflict detection | Post-convergence | Visible at write time |
| Recovery | Snapshot restore | Replay to clean point |
| Read performance | Direct read | Projected view (may need caching) |
| Storage | Single copy | Appends grow over time |

## Hybrid Approach

The best membrane implementation likely uses both:
- **Event log** for audit, provenance, and coordination signals
- **CRDT documents** for the materialized shared state (derived from events)
- Agents write events → system projects CRDT state → agents read projected state

This gives you the best of both: mathematical convergence (CRDTs) and full provenance (event sourcing).

## Open Questions

- How do you compact/archive old events without losing replayability?
- What's the latency of projecting views from a growing event log?
- How do agents express "unsubscribe from events before time X"?
- Can the event log itself be distributed (sharded, replicated)?

## Related Patterns

- [[crdt-coordination]] — CRDTs for convergence; event sourcing for provenance
- [[gossip-protocols]] — transport layer for event propagation
- [[mesh-memory-protocol]] — CMBs could be events in the membrane log
- [[protocol-design]] — wire format for membrane events

[[membrane-architecture]] [[crdt-coordination]] [[gossip-protocols]] [[protocol-design]] [[mesh-memory-protocol]]

---
title: CRDT Coordination for Agent Systems
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [consensus, shared-state, architecture, gossip]
sources: [raw/articles/codecrdt-paper.md]
confidence: medium
---

# CRDT Coordination for Agent Systems

## What Are CRDTs?

Conflict-Free Replicated Data Types are data structures that can be modified concurrently by multiple replicas, with **guaranteed eventual convergence** without coordination. They're used in:
- Collaborative editing (Google Docs, Figma)
- Distributed databases (Riak, CouchDB)
- Real-time sync frameworks (Yjs, Automerge)

## Why CRDTs for Agents?

The membrane's shared state layer needs to handle concurrent writes from multiple agents without:
- Central locks (bottleneck, single point of failure)
- Two-phase commit (too slow for LLM-scale operations)
- Manual conflict resolution (doesn't scale with agent count)

CRDTs solve this mathematically: the data structure's merge operation is commutative, associative, and idempotent.

## CRDT Types Relevant to Agent Membranes

### LWW-Register (Last-Writer-Wins)
- Single value, last timestamp wins
- **Use**: Simple agent state (status, current task, confidence)
- **Limitation**: Loses intermediate values

### Multi-Value Register (MV-Register)
- Maintains set of concurrent values
- **Use**: Agent opinions, competing hypotheses
- **Membrane mapping**: Multiple agents propose solutions; membrane preserves all

### OR-Set (Observed-Remove Set)
- Elements can be added/removed concurrently
- **Use**: Task claiming, resource ownership
- **Membrane mapping**: Agents claim tasks without lock conflicts

### G-Counter (Grow-only Counter)
- Only increments, never decrements
- **Use**: Activity counts, quorum thresholds
- **Membrane mapping**: Quorum sensing — "X agents have observed Y"

### PN-Counter (Positive-Negative Counter)
- G-Counter minus another G-Counter
- **Use**: Agent activity with join/leave dynamics

### Yjs / Automerge Documents
- Full document CRDT with rich data types
- **Use**: Shared context/workspace, collaborative artifacts
- **Membrane mapping**: The shared medium itself as a CRDT document

## Integration with Membrane Architecture

### Layer 1 (Permeability) + CRDTs
- Agent exposes specific CRDT sub-trees through the membrane
- Permeability rules control which CRDT types are visible to which agents

### Layer 2 (Shared Medium) + CRDTs
- The membrane IS a CRDT document store
- All writes converge; no central coordinator needed
- Changes propagate via gossip or pubsub

### Layer 3 (Coordination) + CRDTs
- Task claiming via OR-Set
- Quorum detection via G-Counter thresholds
- Conflict resolution is built into the data structure

## Open Questions

- How do CRDTs handle LLM-generated content (unstructured, semantic)?
- What's the merge strategy for conflicting agent edits?
- Can CRDTs represent reasoning traces, not just data?
- How does CRDT state grow over time? Need compaction/decay mechanisms.

[[codecrdt]] [[token-coherence]] [[membrane-architecture]] [[gossip-protocols]] [[protocol-design]]

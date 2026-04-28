---
title: Structured Shared Memory — Beyond Flat Key-Value
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [shared-state, architecture, agent-memory, multi-agent]
sources: [entities/structmem.md, entities/token-coherence-mesi.md, concepts/crdt-coordination.md]
confidence: medium
---

# Structured Shared Memory — Beyond Flat Key-Value

## The Gap

Current membrane proposals ([[membrane-architecture]]) describe shared state as a "distributed document store" or event log. These are essentially flat key-value stores. But [[structmem]] shows that agents need to reason about *relationships between facts* — requiring structured data.

## Flat vs Structured

| Flat KV Store | Structured (Graph) |
|---------------|---------------------|
| Simple, fast lookups | Supports relational queries |
| No implicit relationships | Captures how facts connect |
| Easy to implement | Higher query complexity |
| Scales well | Needs indexing strategy |

## Why Structure Matters for the Membrane

1. **Multi-hop reasoning**: Agent needs to find "all code changes made by agents who also reviewed PR #123"
2. **Causal tracking**: Understanding that Event A caused Event B in the shared state
3. **Dependency graphs**: Agents working on interdependent tasks need to see how their work relates
4. **Temporal structure**: Events have sequences; flat stores lose ordering semantics

## Proposed Design

The membrane's Layer 2 should support:

- **Graph structure**: Nodes (facts/events) and edges (relationships)
- **CRDT-backed**: Use structured CRDTs (Yjs, Automerge) for conflict-free concurrent edits
- **Vector index**: Semantic search over structured data
- **Time-decay**: Entries expire unless reinforced (like [[quorum-sensing-agents]] signal decay)
- **Access control**: Per-node/per-edge permissions (from [[collaborative-memory]])

## Integration with Existing Components

- [[crdt-coordination]]: CRDTs provide the consistency layer; structure is the data model
- [[token-coherence-mesi]]: MESI-style coherence works on structured data (cache lines = subgraphs)
- [[selective-memory-sharing]]: Selective sharing operates on graph regions, not flat keys

[[membrane-architecture]] [[protocol-design]] [[crdt-coordination]] [[best-paths-forwards]]

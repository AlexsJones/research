---
title: CodeCRDT — CRDT-Based Agent Coordination
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-coordination, architecture, consensus]
sources: [raw/articles/codecrdt-paper.md]
confidence: medium
---

# CodeCRDT — CRDT-Based Agent Coordination

## Overview

CodeCRDT (Pugachev, 2025) applies Conflict-Free Replicated Data Types (CRDTs) to coordinate multi-agent LLM code generation. Addresses the fundamental problem: agents fail to realize parallel speedups due to costly coordination overhead.

## Key Insight

Traditional coordination (locks, central schedulers, message passing) creates bottlenecks in multi-agent systems. CRDTs provide:
- **Eventual consistency without central coordination** — agents can make independent changes that converge
- **Observation-driven coordination** — agents monitor shared state changes rather than negotiating
- **Deterministic convergence** — all agents see the same final state regardless of operation ordering

## How It Works

1. Shared codebase represented as a CRDT data structure
2. Agents observe state changes (not lock/negotiate)
3. Agents make independent edits; CRDT semantics guarantee conflict-free convergence
4. Coordination emerges from observation, not explicit protocol

## Relevance to Synthetic Membrane

CRDTs directly address the membrane's Layer 2 (Shared Medium) consistency question. They offer a **decentralized shared memory** where:
- Multiple agents write simultaneously without locks
- Changes propagate via the membrane (gossip or pubsub)
- Convergence is guaranteed mathematically, not by protocol design

This maps well to the biological mycelial network metaphor — distributed, self-healing information flow.

## CRDT Types for Agent Systems

| CRDT | Use Case | Membrane Mapping |
|------|----------|------------------|
| LWW-Register | Agent state slices | Last-write-wins for simple state |
| OR-Set | Shared task sets | Task claiming without conflicts |
| G-Counter | Agent activity counters | Quorum sensing via count thresholds |
| Yjs/automerge | Collaborative documents | Shared context/workspace |
| MV-Register | Multi-value state | Agent opinions with merge semantics |

[[membrane-architecture]] [[blackboard-pattern]] [[protocol-design]]

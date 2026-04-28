---
title: Token Coherence (MESI for LLM Agents)
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [architecture, shared-state, optimization, multi-agent]
sources: [raw/papers/token-coherence-2603.15183.md]
confidence: medium
---

# Token Coherence: MESI Cache Protocols for Multi-Agent LLM Systems

Adapting hardware cache coherence protocols (MESI) to solve synchronization overhead in multi-agent LLM systems. By V. Parakhin (2026-03).

## The Problem

Multi-agent LLM orchestration suffers from **broadcast-induced triply-multiplicative overhead**: synchronization costs scale as O(n × S × |D|) in agents, steps, and artifact size. Under naive broadcast, every state change is re-transmitted to every agent at every step.

## The Insight

This problem maps **with formal precision** onto the cache coherence problem in shared-memory multiprocessor systems — solved by MESI (Modified, Exclusive, Shared, Invalid) protocol since the 1990s.

## MESI Applied to LLM Agents

| State | Hardware Meaning | LLM Agent Meaning |
|-------|-----------------|-------------------|
| **Modified** | Cache line dirty, only here | Agent owns exclusive write access to a knowledge chunk |
| **Exclusive** | Cache line clean, only here | Agent has read-only access, no one else has it |
| **Shared** | Multiple caches have it | Multiple agents have read copies |
| **Invalid** | Not in cache | Agent doesn't have this data |

## Benefits for Synthetic Membrane

This is **the** solution to the shared memory consistency problem in the membrane:

1. **Selective synchronization** — only modified data is broadcast, not full state
2. **Ownership tracking** — clear notion of who can write vs read
3. **Reduced token waste** — agents don't receive updates for data they don't use
4. **Scalable** — avoids O(n²) broadcast to all agents

## Key Claim

> "Synchronization cost explosion in LLM multi-agent systems maps with formal precision onto the cache coherence problem in shared-memory multiprocessors"

This paper argues that the membrane's shared memory layer should use MESI-style protocols rather than naive broadcast or full-state snapshots.

## Integration with Architecture

In [[membrane-architecture]], Layer 2 (Shared Memory) should implement MESI-like coherence:
- Each shared document/state has an MESI state per agent
- Write invalidation: when Agent A modifies data, Agents B/C with stale copies get invalidated
- Read promotion: agent requesting write gets exclusive access

## Related

- [[membrane-architecture]] — Layer 2 should use MESI coherence
- [[protocol-design]] — MESI messages as new message types
- [[distributed-state-patterns]] — CRDTs vs MESI trade-offs
- [[rcr-router]] — Complementary: RCR handles routing, MESI handles coherence

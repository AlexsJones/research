---
title: StructMem — Structured Memory for Long-Horizon Behavior in LLMs
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [agent-memory, architecture, shared-state, multi-agent]
sources: [raw/papers/structmem-2604.21748.md]
confidence: medium
---

# StructMem — Structured Memory for Long-Horizon Behavior in LLMs

Xu et al. (2026). [arXiv:2604.21748](https://arxiv.org/abs/2604.21748)

## What It Does

Addresses how conversational agents need memory systems that capture *relationships between events*, not merely isolated facts, to support temporal reasoning and multi-hop question answering. Proposes structured memory as an alternative to flat memory stores.

## Key Tension

- **Flat memory**: Efficient to query but fails to model relational structure between events
- **Structured memory**: Captures relationships but adds complexity and query overhead
- StructMem proposes a hybrid: structured backbone with efficient flat-indexed access

## Relevance to Synthetic Membrane

Directly informs the design of the membrane's Layer 2 (shared memory). Current proposals assume flat key-value or document stores. This work suggests:

1. **Relational structure matters**: Agents sharing state need to understand how events/facts relate to each other
2. **Graph-based shared memory**: The membrane's shared state could be a graph database rather than flat KV store
3. **Multi-hop queries**: Agents need to trace chains of reasoning across shared state, not just look up values

This strengthens the case for CRDTs ([[crdt-coordination]]) since CRDTs can represent structured data (not just flat maps), and suggests the membrane should support graph-like data structures.

[[crdt-coordination]] [[membrane-architecture]] [[selective-memory-sharing]] [[token-coherence-mesi]]

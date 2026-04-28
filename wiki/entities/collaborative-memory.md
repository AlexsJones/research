---
title: Collaborative Memory with Dynamic Access Control
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [shared-state, multi-agent, agent-memory, architecture]
sources: [raw/papers/collaborative-memory-2505.18279.md]
confidence: high
---

# Collaborative Memory: Multi-User Memory Sharing with Dynamic Access Control

By Alireza Rezazadeh et al. (2025). 22 citations.

## What It Does

A framework for multi-agent systems where specialized LLM agents share persistent memory with dynamic access controls. Addresses the gap between single-agent persistent memory (well studied) and multi-agent memory sharing (underexplored).

## Key Concepts

- **Persistent Memory**: Beyond conversation context — agents maintain long-term knowledge
- **Dynamic Access Control**: Not all agents can access all memory — permissions are role-based and dynamic
- **Memory Segments**: Shared memory divided into segments with different access policies
- **Cross-Agent Retrieval**: Agents can search and retrieve from shared memory pools

## Relevance to Synthetic Membrane

This is the closest existing work to the membrane's **Layer 2: Shared Medium**:

1. **Dynamic access control** maps directly to [[membrane-architecture|permeability layer]] — agents control what's exposed
2. **Memory segments** are like membrane compartments — selective sharing within shared state
3. **Multi-user** means agents from different owners/contexts can share

## Key Finding

> "Persistent memory has been shown to enhance single-agent performance, but multi-agent memory sharing introduces coordination challenges and privacy concerns"

The paper identifies the same core tension as the synthetic membrane: efficiency of sharing vs. privacy/security of isolation.

## Gaps This Doesn't Address

- No swarm coordination (agents don't self-organize)
- No dynamic capability discovery (memory ≠ capabilities)
- Still uses centralized memory store (not distributed)
- No biological inspiration for access patterns

## Related

- [[membrane-architecture]] — Directly relevant to Layer 2
- [[protocol-design]] — Access control as permeability rules
- [[selective-memory-sharing]] — Similar problem space
- [[trust-models]] — Access control requires identity verification

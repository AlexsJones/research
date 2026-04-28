---
title: Token Coherence — MESI Cache Protocol for Multi-Agent LLMs
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, architecture, shared-state, optimization]
sources: [raw/articles/token-coherence-mesi.md]
confidence: medium
---

# Token Coherence — MESI Cache Protocol for Multi-Agent LLMs

## Overview

Token Coherence (Parakhin, 2026) adapts the MESI cache coherence protocol (used in multi-core CPUs) to minimize synchronization overhead in multi-agent LLM systems.

## The Problem

Naive broadcast synchronization in multi-agent LLM systems has triply-multiplicative overhead: **O(n × S × |D|)** where n=agents, S=steps, D=data/artifact size. This "broadcast-induced overhead" makes multi-agent systems slower than single agents for many tasks.

## MESI Protocol Adaptation

MESI (Modified, Exclusive, Shared, Invalid) tracks cache line states in multi-core processors:

| State | Multi-Core | Multi-Agent Adaptation |
|-------|-----------|----------------------|
| **Modified** | Cache has dirty data not in memory | Agent has modified context tokens not yet shared |
| **Exclusive** | Cache has clean data no one else has | Agent has context data no other agent needs |
| **Shared** | Data shared across multiple caches | Context tokens visible to multiple agents |
| **Invalid** | Cache line is stale | Agent's view of shared state is outdated |

## Key Benefits

- **Synchronization only when needed** — agents don't broadcast every change
- **Dirty state tracking** — agents know what they've modified that others should see
- **Invalidation signaling** — agents learn when their view is stale
- **Reduces communication by orders of magnitude** vs naive broadcast

## Relevance to Synthetic Membrane

This is a concrete implementation of the membrane's **permeability layer** (Layer 1):
- The MESI states define *when* information crosses the membrane
- Modified → Shared transition = agent publishing changes through the membrane
- Invalid state = membrane signaling that an agent's view is stale

Combined with [[codecrdt]], this gives us both the consistency model (CRDT) and the synchronization protocol (MESI-like) for the shared state layer.

[[membrane-architecture]] [[codecrdt]] [[protocol-design]] [[diffmas]]

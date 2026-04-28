---
title: LangGraph
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: ["architecture", "orchestration", "multi-agent"]
sources: []
confidence: medium
---

# LangGraph

LangChain's state-machine based orchestration framework for multi-agent workflows.

## What It Does
- Define agent workflows as graphs (state machines)
- Shared state within a graph execution
- Checkpointing and human-in-the-loop
- Multi-agent patterns (supervisor, handoff, parallel)

## Relevance to Synthetic Membrane
LangGraph has "shared state" but it's scoped to a single graph execution — not a persistent, distributed membrane. Key insight: the state object in LangGraph is a structured dict that nodes read/write. This is essentially a blackboard pattern.

## Limitations for Our Use Case
- Single-process, single-workflow scope
- No cross-workflow state sharing
- Requires pre-defined graph topology (not emergent)
- Tied to LangChain ecosystem


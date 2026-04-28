---
title: Blackboard Pattern
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: ["architecture", "shared-state", "pattern"]
sources: []
confidence: medium
---

# Blackboard Pattern

Classic AI architecture where multiple specialized agents read/write to a shared "blackboard."

## How It Works
1. A shared data structure (the blackboard) holds the current state
2. Multiple independent agents monitor the blackboard
3. When conditions are met, an agent writes its contribution
4. Other agents react to changes
5. Process continues until a solution emerges

## Biological Parallel
Like a mycelial network — distributed sensing and response through a shared medium.

## Relevance to Synthetic Membrane
The blackboard IS the membrane. Every agent can:
- Read from it (sense the environment)
- Write to it (contribute knowledge)
- Subscribe to changes (react dynamically)

This is the closest existing pattern to what we're imagining. The question is how to make it modern, distributed, and LLM-native.

## Modern Implementation Ideas
- Redis Streams / PubSub for the blackboard
- Event-sourced document store
- CRDTs for conflict-free distributed state
- Vector embeddings for semantic querying of the blackboard


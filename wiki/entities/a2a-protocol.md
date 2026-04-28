---
title: A2A (Agent-to-Agent Protocol)
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: ["protocol", "agent-communication"]
sources: []
confidence: medium
---

# A2A Protocol

C4AI's Agent-to-Agent protocol for direct agent communication.

## What It Does
- Standardized message format between agents
- Task negotiation and delegation
- Context sharing between agents
- Status tracking and cancellation

## Relevance to Synthetic Membrane
A2A is the closest existing standard to inter-agent communication, but it's primarily message-based (request/response) rather than shared-state. It lacks:
- Permeable shared memory
- Dynamic capability discovery
- Swarm coordination primitives

## Limitations
- Still relatively new and immature
- C4AI-specific, not yet widely adopted
- Message-oriented, not state-oriented
- No concept of "membrane permeability" (what's shared vs private)


---
title: Synthetic Membrane — Initial Research
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [protocol, architecture, shared-state, swarm, multi-agent, open-question]
sources: []
confidence: medium
---

# Synthetic Membrane — Initial Research (2026-04-26)

## The Problem Statement

Current AI agent frameworks give each agent its own isolated context window. They can pass messages back and forth, but there's no genuine "shared memory" — no permeable boundary where agents can sense each other's state, share discoveries, and dynamically swarm around problems.

Skills.md and MCP provide interfaces, but they're one-directional: agent calls tool, tool returns data. They don't enable agents to perceive each other or build shared understanding.

## What "Synthetic Membrane" Could Mean

Inspired by biological cell membranes — semi-permeable barriers that control what passes through while enabling cells to sense and respond to their environment. For AI agents, this could be:

1. **A protocol** — standardized agent-to-agent communication (like A2A, ACP)
2. **A shared state layer** — distributed memory that agents read/write/perceive
3. **A coordination fabric** — dynamic swarming where agents self-organize

## Existing Landscape

### 1. Protocol-Level Approaches

**MCP (Model Context Protocol)** — Anthropic's standard for agent-to-tool communication. Great for tools, but NOT designed for agent-to-agent communication. Each MCP server is a dumb endpoint.

**A2A (Agent-to-Agent Protocol)** — C4AI's protocol for direct agent communication. More relevant. Allows agents to send structured messages, negotiate tasks, share context.

**ACP (Agent Communication Protocol)** — Another interoperability standard. Less mature than A2A.

**ANP (Agent Network Protocol)** — Emerging standard for multi-agent networks.

### 2. Framework-Level Approaches

**LangGraph (LangChain)** — State-machine based multi-agent orchestration. Has "shared state" as a concept, but it's a central graph, not a distributed membrane.

**AutoGen (Microsoft)** — Multi-agent conversation patterns. Agents chat, but no shared memory layer. Each agent maintains its own context.

**CrewAI** — Role-based agent teams. Similar limitations — orchestration is top-down, not emergent.

**Camel / ChatDev** — Conversational agent frameworks. Focus on dialogue patterns, not shared state.

### 3. Shared State Patterns (Traditional CS)

**Blackboard Pattern** — Classic AI pattern where agents read/write to a shared blackboard. Used in expert systems. Still relevant!

**Pub/Sub (NATS, Kafka, Redis)** — Event-driven communication. Agents publish events, others subscribe. Good for coordination but lacks shared understanding.

**Gossip Protocols** — Epidemic-style state propagation. Agents periodically exchange state. Used in distributed systems (Dynamo, gossip protocols).

### 4. Biological Inspiration

**Cell Membranes** — Selective permeability, signal transduction, receptor-based sensing.
**Gap Junctions** — Direct cell-to-cell channels for rapid signal sharing.
**Quorum Sensing** — Bacteria coordinate behavior based on population density.
**Mycelial Networks** — Fungal networks for resource sharing and information transfer.
**Neural Synapses** — Weighted connections, plasticity, emergent behavior.

## Key Gaps Identified

1. **No standard for agent-to-agent shared memory** — Everyone passes messages, nobody shares state
2. **No dynamic swarming** — Current frameworks require pre-defined orchestration
3. **No "membrane permeability" concept** — Can't control what aspects of state are shared vs private
4. **No emergent coordination** — Everything is top-down, not bottom-up
5. **Cross-framework interoperability** — A LangGraph agent can't talk to an AutoGen agent

## Potential Directions

### Direction A: Protocol (Like A2A but deeper)
Define a wire protocol for agents to share not just messages but state slices, capabilities, and intent signals. Build on or extend A2A/MCP.

### Direction B: Shared Memory Infrastructure
A distributed key-value or document store that agents read/write, with consistency guarantees and event streams. Like a "group mind" database.

### Direction C: Hybrid — Protocol + Memory + Orchestration
The full stack: protocol for communication, shared memory for state, and coordination primitives for swarming.

## Open Questions

- Is this a protocol spec, a runtime, or both?
- How do we handle security/trust between agents from different providers?
- What's the minimum viable membrane — what's the simplest thing that works?
- How does it integrate with existing frameworks (LangGraph, AutoGen, Hermes)?
- Biological inspiration: which patterns map best to AI agents?


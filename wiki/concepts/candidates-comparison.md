---
title: Synthetic Membrane — Candidate Approaches Comparison
created: 2026-04-26
updated: 2026-04-26
type: comparison
tags: [comparison, architecture, protocol, proposal, shared-state, swarm]
sources: [prototypes/mcp-membrane.py, prototypes/blackboard-membrane.py, prototypes/protocol-spec.py, prototypes/swarm-membrane.py]
confidence: medium
---

# Synthetic Membrane — Candidate Approaches

Four prototype approaches have been built and tested. This document compares them and recommends the best path forward.

## Candidate A: MCP-Based Membrane (In-Memory Store)

**What it is:** Each agent exposes state as permeable entries in a shared in-memory store. Three-tier permeability: public / trusted / private.

**Prototype:** `prototypes/mcp-membrane.py`

**Strengths:**
- Leverages existing MCP ecosystem (Anthropic, 500+ servers, growing adoption)
- Permeability model is natural and flexible
- Agent discovery through capability registration
- Broadcast and event subscription built in
- In-memory = zero latency

**Weaknesses:**
- No persistence (in-memory only)
- Single-process (no distributed operation)
- MCP is fundamentally client-server, not peer-to-peer
- Requires wrapping the membrane as an MCP server for agents to use

**Maturity:** Proof-of-concept, ~200 lines

## Candidate B: Blackboard Membrane (SQLite-Persisted)

**What it is:** SQLite-backed shared blackboard with event log. Agents contribute to sections, subscribe to changes, and resolve entries.

**Prototype:** `prototypes/blackboard-membrane.py`

**Strengths:**
- SQLite = durable, ACID, no server needed, single file
- Immutable event log enables replay and audit
- Section-based organization matches agent workflows
- Priority system for urgent contributions
- Entry lifecycle: active → resolved → expired

**Weaknesses:**
- SQLite file locking limits concurrent writes (single writer)
- No network transport — agents must share filesystem
- Not designed for distributed operation
- Event subscriptions are reactive, not proactive discovery

**Maturity:** Proof-of-concept, ~300 lines

## Candidate C: Wire Protocol (Transport-Agnostic)

**What it is:** JSON message protocol with 8 message types. Works over any transport (WebSocket, HTTP/3, gRPC, NATS).

**Prototype:** `prototypes/protocol-spec.py`

**Strengths:**
- Transport-agnostic — works with any messaging layer
- Complete message type coverage (expose, subscribe, read, write, broadcast, swarm, decay, ping/pong)
- Permeability and trust model included
- Protocol handler encapsulates agent behavior
- Easy to extend with new message types

**Weaknesses:**
- In-memory only (no persistence)
- Requires a transport layer to be meaningful
- No built-in consistency model
- Protocol is "best effort" — messages can be lost

**Maturity:** Specification + handler, ~350 lines

## Candidate D: Quorum-Sensing Swarm

**What it is:** Agents emit chemical-like signals. When concentration crosses a threshold, swarm behavior activates automatically. Swarms dissolve when tasks complete.

**Prototype:** `prototypes/swarm-membrane.py`

**Strengths:**
- True emergent coordination — no central orchestrator needed
- Biologically inspired (bacterial quorum sensing, ant colonies)
- Signal decay naturally limits swarm scope
- Capability-based swarm membership
- Self-terminating (swarm dissolves on completion)

**Weaknesses:**
- Hard to tune threshold parameters
- No persistence
- Deterministic simulation, not real-time
- Doesn't handle partial failures well
- Swarm completion is simplified (needs real task tracking)

**Maturity:** Simulation, ~300 lines

## Comparison Matrix

| Feature | A: MCP-Based | B: Blackboard | C: Wire Protocol | D: Swarm |
|---------|:-----------:|:-------------:|:----------------:|:--------:|
| Persistence | ❌ | ✅ SQLite | ❌ | ❌ |
| Distributed | ❌ | ❌ File | ✅ Transport | ❌ |
| Permeability | ✅ 3-tier | ❌ | ✅ 3-tier | ❌ |
| Discovery | ✅ | ❌ | ✅ | ✅ |
| Events | ✅ | ✅ Log | ✅ Callbacks | ✅ Signals |
| Swarm | ❌ | ❌ | ✅ Join/Leave | ✅ Quorum |
| Trust Model | ✅ | ❌ | ✅ | ❌ |
| TTL/Decay | ✅ | ✅ | ✅ | ✅ |
| Cross-framework | ⚠️ MCP only | ✅ | ✅ | ✅ |

## Recommended Path: Hybrid C + B + D

Don't pick one. Combine them:

### Layer 1: Wire Protocol (from C)
The membrane protocol is the API boundary. JSON messages over WebSocket/NATS. Transport-agnostic, extensible.

### Layer 2: Persistent Blackboard (from B)
SQLite or a distributed document store as the shared medium. Event-sourced — every state change is an immutable log entry. Supports replay, audit, and debugging.

### Layer 3: Swarm Coordination (from D)
Quorum-sensing signal system built on top of the protocol layer. Agents emit signals through the protocol, concentration is computed by the blackboard, swarms activate automatically.

### Layer 4: MCP Compatibility (from A)
Expose the membrane as an MCP server. Any MCP-compatible agent can participate without knowing the protocol. Permeability controls what's exposed.

## Architecture Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Agent A    │     │   Agent B    │     │   Agent C    │
│  (Hermes)    │     │  (LangGraph) │     │  (AutoGen)   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │ MCP / Protocol     │ Protocol            │ Protocol
       └───────┬────────────┴──────────┬──────────┘
               │         Message Bus (WebSocket / NATS)
               └──────────┬────────────┘
                          │
            ┌─────────────┴─────────────┐
            │     Membrane Server       │
            │                           │
            │  ┌───────────────────┐    │
            │  │  Wire Protocol    │    │
            │  │  (msg routing)    │    │
            │  └───────────────────┘    │
            │  ┌───────────────────┐    │
            │  │  Blackboard       │    │
            │  │  (persistent)     │    │
            │  └───────────────────┘    │
            │  ┌───────────────────┐    │
            │  │  Swarm Engine     │    │
            │  │  (quorum sensing) │    │
            │  └───────────────────┘    │
            └───────────────────────────┘
```

## Immediate Next Steps

1. **Build the membrane server** — combine C (protocol) + B (SQLite persistence)
2. **Add MCP server wrapper** — expose membrane as MCP resources/tools (from A)
3. **Add swarm engine** — quorum sensing on top (from D)
4. **Test with two Hermes agents** — verify cross-agent communication works
5. **Define the spec** — formal protocol document with versioning

## Open Questions

- Single membrane server or distributed mesh?
- Consistency model: eventual vs strong?
- Authentication between agents?
- How to handle agent crash/recovery?
- Memory limits on the blackboard?
- Protocol versioning strategy?

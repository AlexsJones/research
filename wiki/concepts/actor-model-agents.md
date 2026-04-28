---
title: Actor Model for Agent Systems
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [architecture, pattern, agent-communication, consensus]
sources: []
confidence: medium
---

# Actor Model for Agent Systems

The Actor Model (Carl Hewitt, 1973) is a mathematical model of concurrent computation where "actors" are the fundamental units of computation. Each actor has its own state, can send messages to other actors, and can create new actors. Used in Erlang, Akka, Orleans, and many distributed systems.

## Core Principles

1. **Encapsulation**: Each actor maintains its own state; state is never shared, only communicated via messages
2. **Asynchronous messaging**: Actors communicate through async message passing
3. **Location transparency**: Actors don't need to know where other actors are located
4. **Supervision hierarchies**: Actors can supervise child actors and handle failures
5. **Let it crash**: Failures are handled by supervisors restarting actors, not by defensive coding

## Why Actors for Multi-Agent LLM Systems?

The Actor Model maps naturally to LLM agents:

| Actor Principle | LLM Agent Mapping |
|---|---|
| Encapsulated state | Agent's context window, memory, tools |
| Message passing | Agent-to-agent communication via membrane |
| Location transparency | Agents can be on different machines/services |
| Supervision | Orchestrator agent managing worker agents |
| Let it crash | Failed agents restarted with fresh context |

## Comparison with Other Coordination Patterns

### vs [[blackboard-pattern]] (Shared State)
- Blackboard: agents share a common writable space
- Actors: agents never share state, only messages
- Membrane can support both: membrane IS the message-passing layer, with optional shared-state zones

### vs [[crdt-coordination]] (CRDTs)
- CRDTs: shared state with mathematical convergence guarantees
- Actors: no shared state, pure message passing
- Actors can use CRDTs for the messages themselves (conflict-free message ordering)

### vs [[gossip-protocols]]
- Gossip: epidemic-style broadcast to random peers
- Actors: targeted message delivery to specific addresses
- Can combine: actors use gossip for discovery, direct messaging for coordination

## Actor Model + Membrane Architecture

### Layer 0: Trust & Identity
Each actor has a verifiable identity. Message signatures ensure sender authenticity.

### Layer 1: Permeability
An actor's permeability rules = its message routing table. "I accept messages of type X from agents with reputation > Y."

### Layer 2: Shared Medium
In pure actor model: there is NO shared medium — only messages. The membrane could provide a hybrid: messages pass through the membrane, and the membrane optionally persists certain messages as shared state.

### Layer 3: Coordination
Supervisor actors manage groups of worker actors. The membrane enables supervisors to discover, recruit, and monitor workers.

## Open Questions

- LLM agents have huge context windows — does pure message passing create too much overhead vs shared state?
- Can actors handle the rich semantic communication that LLM agents need?
- How do supervision hierarchies interact with emergent swarm behavior?
- Is the actor model too rigid for the dynamic, fluid coordination that biological membranes enable?

## Related

- [[gossip-protocols]] — transport for actor messages
- [[protocol-design]] — wire format for actor-style membrane messages
- [[membrane-architecture]] — overall architectural framework
- [[crdt-coordination]] — alternative: shared-state approach

[[membrane-architecture]] [[protocol-design]] [[blackboard-pattern]] [[crdt-coordination]] [[best-paths-forwards]]

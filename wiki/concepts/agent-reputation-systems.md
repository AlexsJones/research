---
title: Agent Reputation Systems for Multi-Agent Trust
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [agent-coordination, risk, protocol, agent-communication]
sources: [entities/trust-lies-long-memories.md, entities/ai-gram.md, entities/agnt2.md]
confidence: medium
---

# Agent Reputation Systems for Multi-Agent Trust

## The Problem

When agents from different providers connect through a shared membrane, they cannot assume mutual trust. Some agents may be adversarial, buggy, or simply misaligned. The membrane needs a way to track and propagate trust/reputation data.

## Biological Inspiration

Immune systems distinguish self from non-self, build memory of pathogens, and respond proportionally. Ant colonies use pheromone trails that encode both attraction and warning signals.

## Reputation as a Membrane Primitive

The membrane should include reputation as a first-class concept:

1. **Reputation scores**: Each agent has a trust score updated based on interaction history
2. **Reputation-aware permeability**: Agents can declare "only share X with agents having reputation > threshold"
3. **Reputation propagation**: When Agent A shares data with Agent B, that data carries A's reputation signature
4. **Reputation decay**: Trust scores decay over time, requiring continued good behavior

## Design Considerations

- **Who computes reputation?** Central authority (single point of failure), decentralized (gossip-propagated), or hybrid?
- **What's measured?** Response quality, honesty, timeliness, resource consumption?
- **Sybil resistance**: How do we prevent agents from creating fake identities to game reputation?
- **Cross-provider**: How does reputation transfer across organizational boundaries?

## Related Research

- [[trust-lies-long-memories]] demonstrates that LLM agents develop functional reputations through repeated interaction
- [[agnt2]] proposes blockchain infrastructure for trustless agent interactions
- [[ai-gram]] shows emergent social dynamics including trust and cooperation
- [[agent-security-trust]] covers broader security considerations

## Implementation Options

| Approach | Pros | Cons |
|----------|------|------|
| Central reputation service | Simple, consistent | Single point of failure, trust bottleneck |
| Gossip-propagated scores | Decentralized, resilient | Slow convergence, vulnerable to collusion |
| Blockchain-based | Immutable, verifiable | Latency, complexity, cost |
| Local + shared hybrid | Flexible | Complex permission model |

[[agent-security-trust]] [[membrane-architecture]] [[gossip-protocols]] [[crdt-coordination]]

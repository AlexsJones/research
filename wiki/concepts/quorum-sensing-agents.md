---
title: Quorum Sensing for Agent Swarms
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [swarm, quorum-sensing, agent-coordination, bio-inspiration]
sources: []
confidence: high
---

# Quorum Sensing for Agent Swarms

## Biological Foundation

Bacteria secrete signaling molecules (autoinducers) into their environment. When the concentration of these molecules crosses a threshold — indicating sufficient population density — the bacteria collectively change behavior (bioluminescence, biofilm formation, virulence).

Key properties:
- **No central controller** — behavior emerges from local sensing
- **Threshold-based** — decision triggered by count, not identity
- **Adaptive** — works regardless of exact population size
- **Self-correcting** — if population drops, behavior reverses

## Mapping to AI Agent Swarms

| Biological | Agent System |
|-----------|-------------|
| Autoinducer molecule | Agent heartbeat / presence signal |
| Concentration threshold | Quorum threshold (e.g., 5 agents needed) |
| Behavior change | Swarm activation / task initiation |
| Diffusion through environment | Gossip protocol propagation |
| Receptor specificity | Agent subscription to specific signals |

## Implementation in the Membrane

### Signal Broadcasting
Each agent periodically writes a "presence" signal to the membrane:
```
MEMBRANE.write({
  agent_id: "agent-A",
  signal_type: "presence",
  capability: "code-review",
  confidence: 0.92,
  timestamp: now()
})
```

### Quorum Detection
A quorum sensor monitors the membrane for signal accumulation:
```
quorum = count_signals(membrane, type="presence", capability="code-review", ttl=60s)
if quorum >= THRESHOLD:
    activate_swarm("code-review-squad", agents=quorum_members)
```

### Dynamic Swarm Activation
- Swarm forms when threshold crossed
- Swarm dissolves when task complete or threshold drops
- No pre-defined orchestration needed — **emergent coordination**

## Integration with Existing Concepts

- **CRDTs**: Use G-Counter CRDT for quorum counting — naturally handles concurrent increments from multiple agents
- **Gossip**: Signal propagation via gossip protocol — decentralized, fault-tolerant
- **Permeability**: Agents control what signals they broadcast — privacy-preserving

[[biological-membranes]] [[crdt-coordination]] [[gossip-protocols]] [[membrane-architecture]]

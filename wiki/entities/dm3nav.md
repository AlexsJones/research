---
title: DM³-Nav — Decentralized Multi-Agent Semantic Navigation
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, agent-coordination, architecture, benchmark]
sources: [raw/articles/2604-22014v1.md]
confidence: high
---

# DM³-Nav — Decentralized Multi-Agent Semantic Navigation

Kashiri, Jamsandekar, Yazıcıoğlu (2026-04-23) — [arXiv:2604.22014](https://arxiv.org/abs/2604.22014)

## What It Does

Fully decentralized multi-agent semantic navigation system. Robots operate without a central coordinator, global map aggregation, or shared global state at runtime. Coordination happens through ad-hoc pairwise communication, exchanging local maps, goal status, and navigation intent without synchronization.

## Key Design Principles

1. **No shared state** — Each agent maintains only local state; no global map or shared memory
2. **Ad-hoc pairwise communication** — Agents communicate only when in range, exchanging intent and local maps
3. **Implicit task allocation** — Combines intent broadcasting with distance-weighted frontier selection to reduce redundant exploration
4. **No synchronization** — Agents operate independently; coordination is opportunistic
5. **Centralized vs decentralized** — Matches or exceeds centralized and shared-map baselines while eliminating single points of failure

## Validated In Real World

Deployed on HM3DSem scenes and a real-world office environment using two mobile robots, relying entirely on onboard sensing and computation.

## Relevance to Synthetic Membrane

- **Alternative architecture** — DM³-Nav shows that decentralized coordination without shared state CAN work for specific domains (physical navigation). This is a challenge/counterpoint to the membrane's shared-state approach.
- **Domain-specific validation** — For spatial/physical coordination, ad-hoc communication may be sufficient. For knowledge/intent coordination (the membrane's domain), shared state may still be necessary.
- **Validates quorum sensing** — The "intent broadcasting" mechanism is similar to [[quorum-sensing-agents]]: agents signal presence/intent, coordination emerges from overlap.
- **Informs transport design** — The membrane's transport layer could offer both shared-state mode (for knowledge) and ad-hoc mode (for lightweight coordination).
- **Real-world deployment proof** — Shows that decentralized multi-agent systems can work in production, boosting confidence in the membrane concept.

## Key Insight for Membrane Design

The membrane should NOT always require shared state. Different coordination modes may be appropriate for different interaction patterns:
- **Shared state ([[crdt-coordination]])** for persistent knowledge coordination
- **Ad-hoc pairwise ([[actor-model-agents]])** for lightweight, ephemeral coordination
- **Broadcast ([[gossip-protocols]])** for presence/intent signaling

This suggests a multi-mode membrane architecture where agents choose coordination granularity based on task needs.

## Related

- [[quorum-sensing-agents]] — Intent broadcasting ≈ quorum sensing
- [[actor-model-agents]] — Ad-hoc pairwise messaging
- [[gossip-protocols]] — Broadcast mechanism for intent dissemination
- [[membrane-architecture]] — Suggests multi-mode coordination layer
- [[best-paths-forwards]] — Alternative to shared-state approach

[[quorum-sensing-agents]] [[actor-model-agents]] [[membrane-architecture]] [[best-paths-forwards]]

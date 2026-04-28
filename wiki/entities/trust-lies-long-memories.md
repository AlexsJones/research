---
title: Trust, Lies, and Long Memories — Emergent Reputation in Multi-Agent Games
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-communication, swarm, risk]
sources: [raw/papers/trust-lies-long-memories-2604.20582.md]
confidence: medium
---

# Trust, Lies, and Long Memories — Emergent Social Dynamics and Reputation

Suveen Ellawela (2026). [arXiv:2604.20582](https://arxiv.org/abs/2604.20582)

## What It Does

Studies emergent social dynamics in LLM agents playing repeated rounds of The Resistance: Avalon (hidden-role deception game). Agents retain memory of previous interactions — who played which roles and how they behaved — enabling reputation and trust to emerge.

## Key Findings

- Agents develop reputations based on interaction history
- Memory of past behavior influences future cooperation/defection decisions
- Trust becomes a learnable, dynamic property rather than a static configuration
- Agents can learn to lie strategically and detect deception over repeated interactions

## Relevance to Synthetic Membrane

Critical for the membrane's trust/security model ([[agent-security-trust]]). A membrane connecting agents must handle:

1. **Reputation tracking** — who has been reliable?
2. **Selective trust** — sharing sensitive state only with trusted agents
3. **Deception detection** — identifying agents that provide false signals
4. **Memory of interactions** — the membrane could store trust scores alongside shared state

This suggests the membrane's Layer 2 (shared memory) should include a *trust layer* — reputation data that influences permeability decisions in Layer 1.

[[agent-security-trust]] [[membrane-architecture]] [[ai-gram]] [[collaborative-memory]]

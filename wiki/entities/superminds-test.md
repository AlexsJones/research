---
title: Superminds Test — Evaluating Collective Intelligence in Agent Societies
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, swarm, agent-coordination]
sources: [raw/articles/superminds-test-2604.22452.md]
confidence: high
---

# Superminds Test

**Paper:** [2604.22452](https://arxiv.org/abs/2604.22452) "Superminds Test: Actively Evaluating Collective Intelligence of Agent Society via Probing Agents"
**Authors:** Xirui Li, Ming Li, Yunze Xiao, Ryan Wong, Dianqi Li, Timothy Baldwin, Tianyi Zhou
**Published:** 2026-04-24

## Overview

First empirical evaluation of whether collective intelligence emerges spontaneously from scale in large-scale autonomous agent societies. Studies MoltBook, a platform hosting over two million agents.

## Superminds Test Framework

A hierarchical evaluation framework using controlled Probing Agents across three tiers:

1. **Joint Reasoning:** Can agents collaboratively solve problems beyond individual capability?
2. **Information Synthesis:** Can agents synthesize distributed knowledge across the population?
3. **Basic Interaction:** Can agents even maintain meaningful conversations with each other?

## Key Findings

- **No emergent collective intelligence** — society fails to outperform individual frontier models on complex reasoning
- **Rare information synthesis** — distributed information is rarely synthesized across agents
- **Shallow interactions** — threads rarely extend beyond a single reply; most responses generic or off-topic
- **Coordination failure** — even trivial coordination tasks fail
- **Core thesis:** Collective intelligence does NOT emerge from scale alone

## Implications for Synthetic Membrane

This paper provides the strongest empirical validation yet for the synthetic membrane concept:

- Without structured communication protocols, agent interactions remain shallow and unproductive
- Raw scale (2M+ agents) does not produce intelligence — [[membrane-architecture]] is needed to enable it
- Validates [[gated-permeability]]: uncontrolled communication produces noise, not intelligence
- Supports [[agent-reputation-systems]]: without trust/quality mechanisms, agents can't build on each other's outputs
- The "information synthesis" gap maps directly to the membrane's shared memory ([[structured-shared-memory]]) layer

## Related

- [[membrane-architecture]] — the proposed solution to this exact problem
- [[gated-permeability]] — controlling communication quality
- [[agent-reputation-systems]] — enabling agents to build on each other
- [[collective-intelligence]] — the concept this paper tests
- [[biological-membranes]] — biological systems achieve collective intelligence through structured communication

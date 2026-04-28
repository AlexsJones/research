---
title: Agentic World Modeling — Taxonomy and Survey
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, architecture, agent-coordination]
sources: [raw/articles/agentic-world-modeling-2604.22748.md]
confidence: high
---

# Agentic World Modeling

**Paper:** [2604.22748](https://arxiv.org/abs/2604.22748) "Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond"
**Authors:** Meng Chu, Xuan Billy Zhang, Kevin Qinghong Lin, Lingdong Kong, Jize Zhang, et al. (40+ authors)
**Published:** 2026-04-24

## Overview

Massive survey synthesizing 400+ works and summarizing 100+ representative systems across model-based RL, video generation, web/GUI agents, multi-agent social simulation, and AI-driven scientific discovery. Introduces a "levels x laws" taxonomy for world models.

## Levels x Laws Taxonomy

### Capability Levels

| Level | Name | Description |
|-------|------|-------------|
| L1 | Predictor | Learns one-step local transition operators |
| L2 | Simulator | Composes transitions into multi-step, action-conditioned rollouts respecting domain laws |
| L3 | Evolver | Autonomously revises its own model when predictions fail against new evidence |

### Governing-Law Regimes

| Regime | Domain | Constraints |
|--------|--------|-------------|
| Physical | Robotics, manipulation, navigation | Physical laws, conservation principles |
| Digital | GUI agents, web agents | Software semantics, API contracts |
| Social | Multi-agent societies | Social norms, interaction dynamics, emergent behavior |
| Scientific | AI-driven discovery | Scientific method, hypothesis testing, reproducibility |

## Relevance to Synthetic Membrane

### Social Regime = Membrane Domain

The "Social" regime directly covers multi-agent coordination — the membrane's domain. The taxonomy provides:

1. **A maturity model for membrane capabilities:**
   - **L1 Membrane:** Predicts which agents should communicate (one-step permeability decisions)
   - **L2 Membrane:** Simulates multi-step coordination outcomes (swarm planning, task delegation chains)
   - **L3 Membrane:** Evolves permeability rules and governance based on interaction outcomes

2. **Failure mode analysis:** The paper analyzes failure modes across level-regime pairs, providing a framework for understanding where membranes might fail

3. **Evaluation principles:** Decision-centric evaluation — evaluating world models by how well agents ACT using them, not by prediction accuracy alone

## Key Insight for Membrane Design

The membrane IS a world model — specifically, it's the social component of agents' world model. Agents need to predict:
- What information exists in the membrane
- How other agents will respond to shared information
- What the consequences of communication will be

This reframes the membrane from a passive infrastructure to an active component of agent cognition.

## Related

- [[membrane-architecture]] — the membrane as a world model component
- [[cognitive-digestion]] — agents' interpretation of membrane state
- [[quorum-sensing-agents]] — L3 evolver-like adaptation in swarm formation
- [[best-paths-forwards]] — world modeling as potential new path

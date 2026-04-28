---
title: Selective Memory Sharing in Multi-Agent LLM Teams
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-memory, agent-coordination, optimization]
sources: [raw/articles/selective-memory-sharing.md]
confidence: medium
---

# Selective Memory Sharing in Multi-Agent LLM Teams

## Overview

Jain et al. (2026) study the fundamental tension in multi-agent LLM systems: **if agents share everything, they become inefficient (context overload); if they work in isolation, they lose coordination**. Proposes AgentGym-RL framework for learning what to share and when.

## Key Findings

1. **Full sharing → context bloat** → degraded reasoning quality due to noise
2. **No sharing → siloed knowledge** → missed coordination opportunities
3. **Selective sharing → optimal balance** → but requires learning the right policy

## The AgentGym-RL Approach

Uses reinforcement learning to train agents on *what* context to expose and *when*:
- Agents learn sharing policies through interaction
- Rewards based on team task success, not just individual performance
- The policy determines which context tokens/slices are exposed through the shared medium

## Relevance to Synthetic Membrane

This directly addresses the membrane's **permeability** concept:
- Not everything crosses the membrane — agents control what's exposed
- Permeability is *learnable* and *adaptive*, not statically configured
- Maps to biological selective permeability (ion channels, receptor specificity)

This suggests the membrane's permeability layer should support **dynamic, learnable filtering** rather than static rules.

[[membrane-architecture]] [[biological-membranes]] [[protocol-design]] [[diffmas]]

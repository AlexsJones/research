---
title: DiffMAS — Latent Communication via KV Caches
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-communication, architecture, shared-state]
sources: [raw/articles/diffmas-2604.21794.md]
confidence: high
---

# DiffMAS — Latent Communication via KV Caches

## Overview

DiffMAS (Yu et al., 2026) proposes treating KV cache entries as a learnable communication channel between LLM agents, rather than using text-based message passing. This represents a fundamentally different approach to agent-to-agent communication.

## Key Insight

Current multi-agent systems pass text messages back and forth. DiffMAS instead shares internal representations (KV cache entries) between agents, enabling:
- More information-dense communication (latent vectors > text)
- Joint optimization of communication and reasoning
- Parameter-efficient training over multi-agent latent trajectories

## How It Works

1. Agents exchange KV cache entries (key-value pairs from transformer attention) rather than text
2. These latent messages are trained jointly with the multi-agent reasoning task
3. Uses parameter-efficient fine-tuning (LoRA-style) to adapt communication patterns

## Results

- **AIME24**: 26.7% accuracy (vs single-agent baseline)
- **GPQA-Diamond**: 20.2% accuracy
- Consistent gains across reasoning, QA, code generation, and commonsense benchmarks
- Outperforms text-based multi-agent systems and prior latent communication methods

## Relevance to Synthetic Membrane

This is the closest existing research to the "shared state" layer of the membrane concept. If agents can share KV caches, they effectively have a **shared latent workspace** — a form of perceptual coupling without explicit messaging.

This suggests the membrane's Layer 2 (Shared Medium) could use latent representations rather than structured documents, enabling richer information flow.

[[membrane-architecture]] [[protocol-design]] [[mcp-protocol]]

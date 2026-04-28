---
title: Latent Communication Between LLM Agents
created: 2026-04-26
updated: 2026-04-27
type: concept
tags: [agent-communication, architecture, optimization]
sources: [raw/articles/diffmas-2604.21794.md, entities/abstract-chain-of-thought.md]
confidence: medium
---

# Latent Communication Between LLM Agents

## The Paradigm Shift

Most multi-agent systems pass text messages: Agent A generates text → Agent B reads text. This is:
- **Low bandwidth**: text is a lossy compression of thought
- **Slow**: full generation + parsing cycle per message
- **Fixed format**: limited to what can be expressed in text

**Latent communication** bypasses text entirely: agents share internal representations (KV cache entries, embeddings, hidden states).

## How Transformer KV Caches Work

In transformers, the KV cache stores key-value pairs from attention computation:
- **Keys**: what this token "responds to"
- **Values**: what this token "contributes"

When Agent A computes attention on a prompt, its KV cache represents its "understanding" of that prompt. Sharing this cache with Agent B lets Agent B instantly access Agent A's reasoning context.

## Approaches to Latent Communication

### 1. KV Cache Sharing (DiffMAS)
- Agents exchange attention KV entries
- Receiver uses sender's KV entries as additional context
- Trained jointly for optimal information transfer

### 2. Embedding-Based Sharing
- Agents share embedding vectors for key concepts
- Receiver interprets embeddings in its own space
- Lower bandwidth than full KV cache

### 3. Partial State Sharing
- Agents share specific attention heads or layers
- Selective: only relevant internal representations
- Maps to membrane permeability

### 4. Abstract Chain-of-Thought (New — 2026-04-27)

[[abstract-chain-of-thought]] demonstrates that reasoning itself can be compressed into continuous latent representations, achieving comparable quality to explicit text CoT with much shorter generation lengths. This validates the core premise of latent communication:

- **Continuous representations suffice for reasoning** — text is not necessary for the thought process
- **Dramatic token savings** — if reasoning is in latent space, inter-agent communication can too
- **Hybrid approach** — the membrane could support latent mode (efficient) alongside text mode (auditable)

This provides the strongest evidence yet that the membrane's highest-value communication path may be binary/embedding-based rather than text-based.

## Relevance to Synthetic Membrane

Latent communication is the **highest-bandwidth, lowest-latency** form of agent-to-agent information transfer:
- Not constrained by text serialization/deserialization
- Preserves nuance of agent reasoning
- Can be selective (share specific layers/heads)

The membrane's Layer 2 (Shared Medium) could support latent representations alongside structured data:
- Structured data: facts, task states, decisions
- Latent data: reasoning traces, intuition, partial understanding

## Challenges

- **Cross-model compatibility**: KV caches differ between models
- **Training requirement**: DiffMAS requires fine-tuning agents for latent communication
- **Security**: latent representations may encode more than intended
- **Interpretability**: harder to audit/debug latent messages than text

[[diffmas]] [[membrane-architecture]] [[selective-memory-sharing]] [[protocol-design]] [[abstract-chain-of-thought]]

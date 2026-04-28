---
title: Letta — Persistent Memory Agent Framework
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, agent-memory, architecture]
sources: []
confidence: medium
---

# Letta — Persistent Memory Agent Framework

Letta (formerly MemGPT) is an open-source framework for building LLM agents with persistent, cross-session memory. Developed by Chen et al. and released in 2023-2024.

## What It Is

Letta provides a memory management system for LLM agents that mimics human memory architecture:
- **Core memory**: Small, always-in-context window (like working memory)
- **Archival memory**: Large, retrievable long-term storage
- **Episodic memory**: Timeline of past interactions
- **Auto-summarization**: Compresses long conversations into memory-efficient summaries

## Key Features

- **Infinite context**: Agents can maintain memory across arbitrarily long interactions
- **Memory operations**: Agents can explicitly read/write/search their own memory
- **Self-reflection**: Agents are prompted to reflect on and update their memories
- **Multi-agent capable**: Can run multiple Letta agents that interact
- **Open-source**: Available under MIT license, large community

## Relevance to Synthetic Membrane

### Strengths for Membrane Design
- **Memory architecture inspiration**: The core/archival split mirrors the membrane's permeability layers — some state is always accessible, other state requires retrieval
- **Cross-session persistence**: Membrane needs agents that retain identity and relationships across interactions
- **Memory as first-class**: Letta treats memory as a primary agent capability, not an afterthought
- **Self-reflective memory**: Agents that can reason about what to remember/forget — maps to [[cognitive-digestion]]

### Limitations for Membrane Design
- **Single-agent focus**: Primarily designed for individual agent memory, not shared memory between agents
- **No coordination primitives**: No concept of agent-to-agent communication protocols
- **Retrieval-based, not shared**: Memory is retrieved from a personal store, not shared in real-time
- **No permeability model**: Binary access (own memory = full access) vs. graded permeability

### Membrane Gap Analysis

Letta's memory architecture is valuable as a **single-agent memory layer** that could sit inside each agent, while the membrane handles the inter-agent communication. The membrane would be the "gap junction" connecting Letta-style agents.

## Related

- [[structmem]] — Graph-structured memory; complementary approach to memory organization
- [[collaborative-memory]] — Multi-user memory sharing; closer to membrane's shared-state goal
- [[cognitive-digestion]] — Storing interpretations, not raw signals
- [[framework-integration]] — Letta as a target for membrane compatibility layer

[[structmem]] [[collaborative-memory]] [[cognitive-digestion]] [[framework-integration]]

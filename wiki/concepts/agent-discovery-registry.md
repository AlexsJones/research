---
title: Agent Discovery and Registry — Finding Agents in the Ecosystem
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [architecture, multi-agent, agent-communication, protocol]
sources: [entities/agentsearchbench.md, entities/ans.md]
confidence: medium
---

# Agent Discovery and Registry — Finding Agents in the Ecosystem

## The Problem

Before agents can coordinate through the membrane, they need to find each other. This is a prerequisite layer: discovery precedes communication.

## Key Findings from Research

### Description-Based Discovery Fails ([[agentsearchbench]])

AgentSearchBench benchmarks nearly 10,000 real-world agents and shows:
- Semantic similarity of agent descriptions ≠ actual agent performance
- Description-based retrieval and reranking consistently underperform
- **Execution-grounded signals** (what agents actually do) are necessary for reliable matching

### Behavioral Discovery Works

- Lightweight execution-aware probing substantially improves ranking quality
- Agents should be indexed by demonstrated capabilities, not self-reported descriptions
- Capabilities are compositional — context matters

## Implications for Membrane Design

### Layer 0: Discovery/Registry

The membrane needs a discovery layer that:
1. **Indexes agents by behavior** — Execution traces, cost profiles, success rates
2. **Supports semantic + behavioral query** — "Find agents that can do X" uses both description similarity and execution history
3. **Handles cross-provider lookup** — Agents from different frameworks/providers are discoverable ([[framework-integration]])
4. **Verifies identity** — Discovery includes authentication ([[ans]], [[agent-security-trust]])
5. **Updates dynamically** — Agent capabilities change over time; registry must reflect current state

### Registry Design Principles

| Principle | Source | Implementation |
|-----------|--------|----------------|
| Behavioral indexing | [[agentsearchbench]] | Index by execution traces, not descriptions |
| Identity verification | [[ans]] | Cryptographic agent IDs |
| Capability composition | [[agentsearchbench]] | Support compositional queries |
| Cross-framework | [[framework-integration]] | Unified registry for MCP, A2A, LangGraph, AutoGen agents |
| Dynamic update | [[agent-reputation-systems]] | Reputation/capability scores updated per interaction |

## Open Questions

- Should discovery be centralized (single registry) or decentralized (gossip-based)?
- How do agents prove capabilities without executing the full task (probing overhead)?
- What's the privacy tradeoff: behavioral indexing vs. agent capability leakage?
- How does discovery interact with [[gated-permeability]] — do agents only discover relevant peers?

## Related

- [[ans]] — Agent naming and discovery
- [[agentsearchbench]] — Benchmark proving behavioral discovery is essential
- [[framework-integration]] — Cross-framework discovery
- [[agent-security-trust]] — Authentication as part of discovery
- [[membrane-architecture]] — Discovery as Layer 0
- [[best-paths-forwards]] — Discovery as prerequisite for membrane operation

[[ans]] [[agentsearchbench]] [[framework-integration]] [[membrane-architecture]] [[best-paths-forwards]]

---
title: AgentSearchBench — Agent Discovery Benchmark
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, benchmark, agent-communication, architecture]
sources: [raw/articles/2604-22436v1.md]
confidence: high
---

# AgentSearchBench — Agent Discovery Benchmark

Wu, Mammadli, Zhang, Yilmaz (2026-04-24) — [arXiv:2604.22436](https://arxiv.org/abs/2604.22436)

## What It Does

Large-scale benchmark for agent discovery/search in the wild, built from nearly 10,000 real-world agents across multiple providers. Formalizes agent search as retrieval and reranking under both executable task queries and high-level task descriptions.

## Key Findings

1. **Semantic similarity ≠ actual performance** — Description-based retrieval fails to predict which agents actually perform well on tasks
2. **Execution-grounded evaluation** — Only actual execution signals reliably assess agent capability
3. **Behavioral probing works** — Lightweight execution-aware probing substantially improves ranking quality
4. **Agent capabilities are compositional** — Unlike tools, agent capabilities depend on execution context and composition

## Relevance to Synthetic Membrane

- **Discovery is a membrane primitive** — Before agents can coordinate through the membrane, they need to find each other. AgentSearchBench validates that discovery is hard and description-based approaches fail.
- **Validates [[ans]] (Agent Name Service)** — The membrane needs a discovery/lookup layer. The benchmark shows that behavioral signals (what agents actually do) matter more than self-reported capabilities.
- **Informs membrane registry design** — A membrane registry should index agents by demonstrated capabilities (execution traces), not just descriptions.
- **Execution-aware matching** — The membrane could use execution signals to route tasks to the right agents, not just match on keywords.

## Related

- [[ans]] — Agent discovery and naming service; membrane Layer 0
- [[agent-token-economics]] — Execution signals include cost profiles, relevant to matching
- [[framework-integration]] — Cross-provider agent matching is the multi-framework problem
- [[best-paths-forwards]] — Agent discovery as prerequisite for membrane operation
- [[gated-permeability]] — Discovery informs gating: only connect to relevant agents

[[ans]] [[framework-integration]] [[best-paths-forwards]] [[gated-permeability]]

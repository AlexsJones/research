---
title: Failure Attribution Benchmark for LLM Multi-Agent Systems
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, benchmark, agent-communication, risk]
sources: [raw/articles/failure-attribution-benchmark-2604.22708.md]
confidence: high
---

# Failure Attribution Benchmark for LLM Multi-Agent Systems

Chen, Wang, Mu, Wang, Liu, Feng, Wang (2026-04-24) — [arXiv:2604.22708](https://arxiv.org/abs/2604.22708)

## What It Does

Provides the first benchmark specifically for failure attribution in LLM-based multi-agent systems. Addresses the challenge of identifying which agent and which step caused a system failure when natural-language reasoning and complex interactions create ambiguous causal chains.

## Key Findings

- Attribution is hard even with ground-truth access in 3-7 agent systems
- Last-action bias is a common failure mode of naive attribution
- Shared state complicates attribution — requires full provenance tracking

## Relevance to Synthetic Membrane

Validates the membrane's observability requirements: full event provenance, coordination traces, and the membrane as an observability surface. Could serve as a test suite for membrane implementations.

## Related

- [[agent-observability]] — Direct application: observability enables attribution
- [[event-sourcing]] — Provenance tracking enables precise attribution
- [[agent-security-trust]] — Attribution supports trust assessment
- [[membrane-architecture]] — Membrane as observability surface

[[agent-observability]] [[event-sourcing]] [[membrane-architecture]] [[best-paths-forwards]]

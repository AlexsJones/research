---
title: CHIEF — Causal Hierarchical Failure Attribution Framework
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [benchmark, multi-agent, risk, architecture]
sources: [raw/articles/chief-framework-2602.23701.md]
confidence: medium
---

# CHIEF

A framework for hierarchical failure attribution using **causal graphs** instead of flat logs.

**Paper:** 2602.23701 — "From Flat Logs to Causal Graphs"
**Authors:** Yawen Wang, Wenjie Wu, Junjie Wang, Qing Wang

## Key Innovation

Transforms chaotic execution trajectories into structured **hierarchical causal graphs**, then uses:

1. **Oracle-guided backtracking** — synthesized virtual oracles prune the search space
2. **Counterfactual attribution** — progressive causal screening distinguishes root causes from propagated symptoms
3. **Causal screening** — separates true failures from side effects

## Results

Outperforms 8 strong baselines on Who&When benchmark for both agent-level and step-level accuracy.

## Relevance to Synthetic Membrane

The membrane's event sourcing layer naturally produces causal graph structure:
- Events have timestamps (temporal ordering)
- Messages reference other messages (`in_response_to`, `depends_on`)
- The membrane IS the causal substrate

CHIEF builds causal graphs on top of flat logs. The membrane provides them natively — making failure attribution a membrane primitive rather than a post-hoc analysis.

[[traceelephant]] [[whoandwhen]] [[event-sourcing]] [[agent-observability]] [[membrane-architecture]] [[best-paths-forwards]]

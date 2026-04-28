---
title: DoVer — Intervention-Driven Auto Debugging for Multi-Agent Systems
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, risk, agent-coordination]
sources: [raw/articles/dover-2512.06749.md]
confidence: medium
---

# DoVer

An **intervention-driven debugging framework** for LLM multi-agent systems by Microsoft Research.

**Paper:** 2512.06749 — "DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems"
**Authors:** Ming-Jie Ma, Jue Zhang, Fangkai Yang, Yu Kang, Qingwei Lin, S. Rajmohan, Dongmei Zhang
**Repo:** https://aka.ms/DoVer

## Key Innovation

Moves beyond "attribution" (identifying the culprit) to **active verification** through intervention:

1. **Hypothesis generation:** LLM proposes what went wrong
2. **Active intervention:** System edits messages, alters plans, re-runs
3. **Verification:** Does the intervention actually fix the failure?
4. **Outcome-oriented:** Measures success by task completion, not attribution accuracy

## Results

- Flips **18-28%** of failed trials into successes
- Achieves up to **16%** milestone progress
- Validates/refutes **30-60%** of failure hypotheses
- Works across frameworks (Magnetic-One, AG2)

## Relevance to Synthetic Membrane

The membrane enables active debugging by being the intervention surface:
- Modify shared state entries
- Alter permeability rules
- Change message routing
- Replay scenarios with modified parameters
- Observe counterfactual outcomes

This elevates the membrane from passive observability to **active debugging infrastructure**.

[[traceelephant]] [[whoandwhen]] [[chief-framework]] [[agent-observability]] [[event-sourcing]] [[membrane-architecture]] [[best-paths-forwards]]

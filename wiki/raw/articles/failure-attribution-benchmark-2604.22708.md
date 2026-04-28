---
source_url: https://arxiv.org/abs/2604.22708
ingested: 2026-04-27
---

# Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems

Chen, Wang, Mu, Wang, Liu, Feng, Wang (2026-04-24) — cs.MA

## Summary

Failure attribution — identifying the responsible agent and decisive step of a failure — is particularly challenging in LLM-based multi-agent systems due to natural-language reasoning, nondeterministic outputs, and intricate interaction dynamics.

The paper proposes a benchmark for evaluating failure attribution techniques. Existing benchmarks rely on partially observable environments or toy tasks; this work provides realistic multi-agent scenarios where failures emerge from complex interactions.

## Key Findings

1. **Attribution is hard** — In multi-agent systems with 3-7 agents, even ground-truth access doesn't guarantee accurate attribution. The interaction graph makes causal chains ambiguous.

2. **Last-action bias** — Naive attribution (blaming the last agent to act) is inaccurate. The real cause often lies in earlier interactions or shared state corruption.

3. **Shared state complicates attribution** — When agents write to shared memory, determining which write caused a downstream failure requires full provenance tracking.

## Relevance to Synthetic Membrane

This paper directly validates the membrane's need for:
- Full event provenance (event sourcing + signed writes)
- Coordination traces for debugging emergent failures
- The membrane as an observability surface — it sees all interactions

The benchmark could serve as a test suite for membrane implementations: can a membrane-traced system achieve accurate failure attribution?

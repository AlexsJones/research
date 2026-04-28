---
title: Probably Approximately Consensus (PAC) — Learning Theory of Finding Common Ground
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, agent-coordination, optimization, benchmark]
sources: [raw/articles/2604-21811v1.md]
confidence: medium
---

# Probably Approximately Consensus (PAC) — Learning Theory of Finding Common Ground

Blair, Armstrong, Alouf-Heffetz, Talmon, Grossi (2026-04-23) — [arXiv:2604.21811](https://arxiv.org/abs/2604.21811)

## What It Does

Formal learning-theoretic framework for consensus elicitation. Models consensus as an interval in a one-dimensional opinion space derived from high-dimensional data via embedding and dimensionality reduction. Defines an objective that maximizes expected agreement within a hypothesis interval, accounting for topic salience. Provides PAC-learning guarantees and an efficient ERM algorithm.

## Key Findings

1. **Consensus as an interval** — Rather than a single point, consensus is a region of opinion space where most agents agree
2. **Salience-weighted** — Topics that matter more to more agents carry more weight in consensus determination
3. **PAC guarantees** — The approach has formal generalization bounds (Probably Approximately Correct)
4. **Query efficiency** — Selective querying of users on existing samples reduces required queries to practical levels

## Relevance to Synthetic Membrane

- **Consensus mechanism design** — The membrane needs ways to determine when agents "agree" enough to act collectively. PAC provides a formal model for this.
- **Connects to [[multi-agent-consensus-bias]]** — While that paper shows consensus ≠ correctness for humans, PAC provides a principled way to find consensus regions. Together they suggest: find consensus formally (PAC), but present it with dissent to humans (consensus bias mitigation).
- **Opinion space embedding** — The dimensionality reduction approach maps to the membrane's shared state: agents' positions can be embedded into a common space where consensus is computable.
- **Adaptive deliberation** — Selective querying maps to [[gated-permeability]]: only solicit input from agents whose opinions matter most for the current topic.

## Related

- [[multi-agent-consensus-bias]] — Humans over-trust agent consensus; PAC provides formal consensus computation
- [[gated-permeability]] — Selective querying ≈ cost-aware gating
- [[agentic-world-models]] — Opinion space embedding relates to shared world models
- [[best-paths-forwards]] — Consensus as a coordination primitive

[[multi-agent-consensus-bias]] [[gated-permeability]] [[best-paths-forwards]]

---
source_url: https://arxiv.org/abs/2602.23701
ingested: 2026-04-27
sha256:
---

# From Flat Logs to Causal Graphs: Hierarchical Failure Attribution for LLM-based Multi-Agent Systems (CHIEF)

**Authors:** Yawen Wang, Wenjie Wu, Junjie Wang, Qing Wang
**Published:** 2026-02 (Semantic Scholar)
**Citations:** 0 (very new)

## Abstract

LLM-powered Multi-Agent Systems have demonstrated remarkable capabilities in complex domains but suffer from inherent fragility and opaque failure mechanisms. Existing failure attribution methods, whether relying on direct prompting, costly replays, or supervised fine-tuning, typically treat execution logs as flat sequences. This linear perspective fails to disentangle the intricate causal links inherent to MAS, leading to weak observability and ambiguous responsibility boundaries. We propose CHIEF, a novel framework that transforms chaotic trajectories into a structured hierarchical causal graph. It then employs hierarchical oracle-guided backtracking to efficiently prune the search space via synthesized virtual oracles. Finally, it implements counterfactual attribution via a progressive causal screening strategy to rigorously distinguish true root causes from propagated symptoms. Experiments on Who&When benchmark show that CHIEF outperforms eight strong and state-of-the-art baselines on both agent- and step-level accuracy.

## Key Innovation: Causal Graphs for Failure Attribution

- **Problem:** Flat logs lose causal structure — they show what happened but not WHY it happened
- **Solution:** Transform trajectories into hierarchical causal graphs
- **Method:** Counterfactual attribution + causal screening to separate root causes from symptoms
- **Result:** Outperforms 8 baselines on both agent-level and step-level attribution

## Implication for Membrane

The membrane's event sourcing layer naturally produces a causal graph structure:
- Events have timestamps (temporal ordering)
- Events reference other events (causal links via `in_response_to`, `depends_on`)
- The membrane IS the causal substrate that CHIEF needs to build its graphs

This suggests the membrane doesn't need a separate debugging layer — its core architecture already provides the causal structure that CHIEF builds on top of.

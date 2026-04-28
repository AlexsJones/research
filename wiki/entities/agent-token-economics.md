---
title: Agent Token Economics — Token Consumption Patterns in Agentic Tasks
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, architecture, optimization]
sources: [raw/articles/agent-token-consumption-2604.22750.md]
confidence: high
---

# Agent Token Economics

**Paper:** [2604.22750](https://arxiv.org/abs/2604.22750) "How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks"
**Authors:** Longju Bai, Zhemin Huang, Xingyao Wang, Jiao Sun, Rada Mihalcea, Erik Brynjolfsson, Alex Pentland, Jiaxin Pei
**Published:** 2026-04-24

## Key Findings

1. **1000x token overhead:** Agentic tasks consume 1000x more tokens than code reasoning/chat
2. **Input tokens dominate cost:** Not output tokens — context accumulation is the cost driver
3. **30x variance:** Same task, wildly different costs; more tokens ≠ better accuracy
4. **Accuracy peaks at intermediate cost:** Diminishing returns then saturation
5. **Models differ enormously:** Kimi-K2/Claude-Sonnet-4.5 vs GPT-5 can differ by 1.5M+ tokens
6. **Poor self-prediction:** Models systematically underestimate their own costs (r ≤ 0.39)

## Implications for Synthetic Membrane

### Token Efficiency as Design Constraint

The membrane must be designed with token efficiency as a first-class concern:

1. **Compact wire formats:** Since input tokens dominate cost, membrane messages must be compact
2. **Gated permeability justified:** More communication ≠ better results; default-deny saves tokens
3. **Lazy loading:** Load only needed schema/state — connects to [[mcp-efficiency-optimizations]]
4. **Cost-aware routing:** [[rcr-router]] pattern — route communication through most efficient paths
5. **Digestion over raw data:** [[cognitive-digestion]] — agents share compressed interpretations, not raw data

### Token Budgeting for Multi-Agent Systems

- Each agent should have a communication budget
- The membrane should track and report token costs of interactions
- Gating decisions should factor in token cost-benefit analysis
- Swarm coordination ([[quorum-sensing-agents]]) should include cost-aware dissolution

## Related

- [[gated-permeability]] — default-deny justified by token economics
- [[mcp-efficiency-optimizations]] — lazy loading to reduce input token overhead
- [[cognitive-digestion]] — compressed sharing reduces token cost
- [[tool-attention]] — dynamic gating reduces schema overhead
- [[protocol-design]] — wire format design must prioritize compactness

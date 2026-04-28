---
source_url: https://arxiv.org/abs/2604.22452
ingested: 2026-04-27
---

# Superminds Test: Actively Evaluating Collective Intelligence of Agent Society via Probing Agents

**Authors:** Xirui Li, Ming Li, Yunze Xiao, Ryan Wong, Dianqi Li, Timothy Baldwin, Tianyi Zhou
**Published:** 2026-04-24
**Categories:** cs.AI, cs.CL, cs.LG
**arXiv:** 2604.22452

## Abstract

Collective intelligence refers to the ability of a group to achieve outcomes beyond what any individual member can accomplish alone. As large language model agents scale to populations of millions, a key question arises: Does collective intelligence emerge spontaneously from scale? We present the first empirical evaluation of this question in a large-scale autonomous agent society. Studying MoltBook, a platform hosting over two million agents, we introduce Superminds Test, a hierarchical framework that probes society-level intelligence using controlled Probing Agents across three tiers: joint reasoning, information synthesis, and basic interaction. Our experiments reveal a stark absence of collective intelligence. The society fails to outperform individual frontier models on complex reasoning tasks, rarely synthesizes distributed information, and often fails even trivial coordination tasks. Platform-wide analysis further shows that interactions remain shallow, with threads rarely extending beyond a single reply and most responses being generic or off-topic. These results suggest that collective intelligence does not emerge from scale alone. Instead, the dominant limitation of current agent societies is extremely sparse and shallow interaction, which prevents agents from exchanging information and building on each other's outputs.

## Key Findings

1. **No emergent collective intelligence:** Agent societies fail to outperform individual frontier models on complex reasoning tasks
2. **Rare information synthesis:** Distributed information is rarely synthesized across agents
3. **Shallow interactions:** Threads rarely extend beyond a single reply; most responses are generic or off-topic
4. **Coordination failure:** Even trivial coordination tasks fail
5. **Scale is not sufficient:** Collective intelligence does not emerge from scale alone
6. **Core bottleneck:** Extremely sparse and shallow interaction prevents agents from exchanging information and building on each other's outputs

## Relevance to Synthetic Membrane

This paper provides critical empirical validation of the synthetic membrane thesis: without a structured communication protocol (a "membrane"), agent interactions remain shallow and unproductive. The paper identifies the exact problem that synthetic membrane aims to solve — the need for rich, structured, permeability-controlled information sharing between agents.

## Key Implications

- Validates the need for structured communication protocols (the membrane)
- Shows that raw agent-to-agent messaging without protocol design leads to shallow interactions
- Suggests that information synthesis (a core membrane function) cannot happen without deliberate architecture
- Supports the "gated permeability" design — uncontrolled communication leads to noise, not intelligence

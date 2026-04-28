---
source_url: https://arxiv.org/abs/2604.20183
ingested: 2026-04-27
sha256: placeholder
---

# Dual-Cluster Memory Agent: Resolving Multi-Paradigm Ambiguity in Optimization Problem Solving

**Authors:** Xinyu Zhang, Yuchen Wan, Boxuan Zhang, Zesheng Yang, Lingling Zhang, Bifan Wei, Jun Liu
**Published:** 2026-04-22
**arXiv:** 2604.20183
**Categories:** cs.CL

## Abstract

LLMs often struggle with structural ambiguity in optimization problems, where a single problem admits multiple related but conflicting modeling paradigms.

The paper proposes **Dual-Cluster Memory Agent (DCM-Agent)** which enhances performance by leveraging historical solutions in a training-free manner:
- Dual-Cluster Memory maintains two parallel memory streams: one for each paradigm
- When ambiguity is detected, the agent can consult both clusters
- Enables resolution of conflicting approaches without committing to a single paradigm early

## Key Observations

- The dual-cluster approach is relevant to how shared memory might handle contradictory information from different agents
- Training-free memory augmentation is attractive for membrane systems that shouldn't require fine-tuning
- Shows value in maintaining multiple perspectives in memory — relevant for membranes connecting diverse agents

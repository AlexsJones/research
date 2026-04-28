---
source_url: https://arxiv.org/abs/2604.21794
ingested: 2026-04-26
---

# Learning to Communicate: Toward End-to-End Optimization of Multi-Agent Language Systems

**Authors**: Ye Yu, Heming Liu, Haibo Jin, Xiaopeng Yuan, Peng Kuang, Haohan Wang
**Published**: 2026-04-23
**arXiv**: 2604.21794v1
**Category**: cs.CL

## Abstract

Multi-agent systems built on large language models have shown strong performance on complex reasoning tasks, yet most work focuses on agent roles and orchestration while treating inter-agent communication as a fixed interface. Latent communication through internal representations such as key-value caches offers a promising alternative to text-based protocols, but existing approaches do not jointly optimize communication with multi-agent reasoning.

Therefore we propose DiffMAS, a training framework that treats latent communication as a learnable component of multi-agent systems. DiffMAS performs parameter-efficient supervised training over multi-agent latent trajectories, enabling agents to jointly learn how information should be encoded and interpreted across interactions.

Experiments on mathematical reasoning, scientific QA, code generation, and commonsense benchmarks show that DiffMAS consistently improves reasoning accuracy and decoding stability over single-agent inference, text-based multi-agent systems, and prior latent communication methods, achieving 26.7% on AIME24, 20.2% on GPQA-Diamond, and consistent gains across reasoning benchmarks.

## Key Points
- KV cache sharing as communication channel (not text messages)
- Joint optimization of communication + reasoning
- Parameter-efficient training (LoRA-style)
- Outperforms text-based multi-agent systems across benchmarks

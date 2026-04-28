---
title: "Learning to Communicate — End-to-End Optimization of Multi-Agent Language Systems"
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-communication, latent-communication, optimization]
sources: [raw/papers/learning-to-communicate-2604.21794.md]
confidence: medium
---

# Learning to Communicate — End-to-End Optimization of Multi-Agent Language Systems

Yu et al. (2026). [arXiv:2604.21794](https://arxiv.org/abs/2604.21794)

## What It Does

Extends the [[diffmas]] approach of latent communication through KV-caches by making the communication *learnable*. Instead of treating inter-agent communication as a fixed interface, this work proposes end-to-end optimization where agents learn *how* to communicate through their internal representations.

## Key Insights

- Multi-agent LLM systems currently treat communication as a fixed text-based channel
- This work argues communication itself should be an optimizable parameter
- Agents learn to encode the most useful signals in their shared latent space
- Builds directly on DiffMAS's demonstration that KV-cache sharing enables efficient inter-agent communication

## Relevance to Synthetic Membrane

This directly validates Path 3 ([[best-paths-forwards]]) — latent communication membranes. The key advance over DiffMAS is making communication learnable rather than hardcoded, which maps to the membrane's permeability concept: agents learn *what* to share, not just *how* to share.

## Open Questions

- How does this integrate with the membrane's three-layer architecture?
- Can permeability rules be learned rather than specified?
- Does end-to-end training conflict with the modular design philosophy?

[[diffmas]] [[latent-communication]] [[membrane-architecture]] [[best-paths-forwards]]

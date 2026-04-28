---
title: pAI/MSc — ML Theory Research with Humans-in-the-Loop
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [multi-agent, orchestration, agent-communication]
sources: []
confidence: medium
---

# pAI/MSc — ML Theory Research with Humans-in-the-Loop

Abdelmoneum, Beneventano, Poggio (2604.20622) — "pAI/MSc: ML Theory Research with Humans on the Loop"

## What It Is

An open-source, customizable, modular multi-agent system for academic research workflows. The goal is not autonomous scientific ideation or fully automated research, but rather reducing the friction of academic research workflows by orders of magnitude.

## Architecture

Modular multi-agent system where different agents handle different research tasks (literature review, experiment design, result analysis, writing). Key design choices:

- **Human-in-the-loop**: Humans curate and approve critical steps; agents handle the grind
- **Modular**: Each agent has a specific role; the system coordinates between them
- **Customizable**: Researchers can add/modify agents for their specific domain
- **Practical focus**: Optimized for real research workflows, not theoretical autonomy

## Relevance to Synthetic Membrane

- Demonstrates a **practical multi-agent coordination pattern** for knowledge work
- Shows that **scoped agent roles with clear handoffs** work well for complex workflows
- The coordination mechanism between agents is essentially a membrane: agents need to share intermediate results and context
- Validates the idea that **not all agent communication needs to be general-purpose** — domain-specific coordination can be more effective

## Key Insight for Membrane Design

The pAI/MSc approach suggests that membranes might work best when:
1. Agents have clearly defined roles and capabilities
2. Communication is structured around workflow stages, not free-form messaging
3. Humans remain as first-class participants (not just supervisors)
4. The shared state is domain-specific (research artifacts) rather than generic

This contrasts with fully open membranes where any agent communicates with any other agent about any topic.

[[autogen]] [[langgraph]] [[membrane-architecture]] [[best-paths-forwards]]

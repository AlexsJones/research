---
title: AutoGen
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: ["architecture", "orchestration", "multi-agent"]
sources: []
confidence: medium
---

# AutoGen (Microsoft)

Multi-agent conversation framework.

## What It Does
- Agents chat with each other
- Flexible conversation patterns
- Human-in-the-loop
- Code execution agents

## Relevance to Synthetic Membrane
AutoGen agents communicate via messages, not shared state. Each agent has its own context window. No concept of permeable boundaries or selective state sharing.

## Key Gap
AutoGen shows that conversation-based coordination works for many tasks, but it lacks the "shared understanding" that a membrane would provide. Agents in AutoGen can't perceive each other's internal state.


---
title: Tool Attention — Dynamic Tool Gating for MCP Efficiency
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [MCP, architecture, optimization, multi-agent]
sources: [raw/papers/tool-attention-2604.21816.md]
confidence: medium
---

# Tool Attention — Dynamic Tool Gating and Lazy Schema Loading for MCP

Sadani & Kumar (2026). [arXiv:2604.21816](https://arxiv.org/abs/2604.21816)

## What It Does

Addresses the "MCP Tax" — the hidden per-turn overhead (10K-100K tokens) of stateless, eager schema injection in MCP-based tool interfaces. Proposes dynamic tool gating and lazy schema loading to eliminate this overhead in scalable agentic workflows.

## Key Findings

- MCP's current design injects full tool schemas into every LLM turn, regardless of whether tools are used
- This "MCP Tax" scales poorly with the number of available tools
- Solution: only load schemas for tools relevant to the current context (dynamic gating)
- Reduces token overhead from O(n) to O(1) in typical usage

## Relevance to Synthetic Membrane

If the membrane uses MCP as its transport layer (Path 2 in [[best-paths-forwards]]), this efficiency improvement is essential:

1. **MCP as membrane transport**: The membrane's expose/subscribe/read/write operations would be MCP tools
2. **Schema explosion**: As more agents join the membrane, the number of available operations grows — the MCP Tax would compound
3. **Lazy discovery**: Dynamic gating means agents only see membrane operations relevant to their current task
4. **Validates MCP path**: With lazy loading, MCP becomes viable as a membrane transport even for large-scale deployments

This strengthens the case for Path 2 (MCP extension) as the membrane's transport layer, provided lazy schema loading is implemented.

[[mcp-protocol]] [[protocol-design]] [[best-paths-forwards]] [[membrane-architecture]]

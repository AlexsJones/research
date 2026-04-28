---
title: MCP Efficiency Optimizations for Membrane Transport
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [MCP, architecture, optimization, protocol]
sources: [entities/tool-attention.md, entities/mcp-protocol.md]
confidence: medium
---

# MCP Efficiency Optimizations for Membrane Transport

## The MCP Tax Problem

[[tool-attention]] identifies a critical issue: MCP's stateless, eager schema injection imposes a per-turn overhead of 10K-100K tokens. For a membrane connecting many agents, this overhead compounds rapidly.

## Why This Matters for the Membrane

If the membrane uses MCP as its transport layer (Path 2 in [[best-paths-forwards]]):

- Every membrane interaction (expose, subscribe, read, write) becomes an MCP tool call
- As more agents join, more operations become available
- Naive schema injection makes the membrane unusable beyond ~5-10 agents

## Solutions

### 1. Lazy Schema Loading
Only inject schemas for tools relevant to the current context. [[tool-attention]] shows this reduces overhead from O(n) to O(1).

### 2. Schema Caching
Cache schemas across turns rather than re-injecting every time. MCP doesn't support this natively but can be implemented at the client level.

### 3. Hierarchical Tool Registry
Group tools by category; inject category-level schemas first, drill down only when needed.

### 4. Streaming Schema Updates
Instead of full schema re-injection, send deltas when tools are added/removed.

## Implications for Protocol Design

The membrane protocol ([[protocol-design]]) should account for:

- **Discovery phase**: Agent initially learns available membrane operations
- **Incremental updates**: Only new/changed operations trigger schema updates
- **Contextual filtering**: Agent sees only operations matching its declared capabilities

This optimization doesn't just make MCP viable as membrane transport — it shapes the membrane's discovery and negotiation phases.

[[mcp-protocol]] [[protocol-design]] [[best-paths-forwards]] [[membrane-architecture]]

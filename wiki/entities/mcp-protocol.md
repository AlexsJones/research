---
title: MCP (Model Context Protocol)
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: ["protocol", "interface", "agent-communication"]
sources: []
confidence: medium
---

# MCP (Model Context Protocol)

Anthropic's standard for connecting LLMs to tools and data sources.

## What It Does
- Tool discovery and invocation
- Resource access (read/write)
- Prompt templates
- Sampling (server-initiated LLM calls)

## Relevance to Synthetic Membrane
MCP solves agent-to-tool communication beautifully. For inter-agent communication:
- Could be extended: an agent exposes its capabilities as MCP tools
- Resources could represent shared state
- Sampling could enable agent-to-agent LLM delegation
- But MCP is fundamentally client-server, not peer-to-peer

## Key Insight
MCP's "resources" concept is the closest thing to shared memory. An MCP resource is a URI-addressable piece of data. If agents expose their state as MCP resources, you get a form of shared memory.


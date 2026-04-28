---
title: AgentLeak — Privacy Leakage in Multi-Agent Systems
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [risk, security, multi-agent, shared-state]
sources: [raw/papers/agentleak-2602.11510.md]
confidence: high
---

# AgentLeak: Full-Stack Benchmark for Privacy Leakage in Multi-Agent LLM Systems

By Faouzi El Yagoubi, Godwin Badu-Marfo, Ranwa Al Mallah (2026-02). 4 citations.

## The Problem

Multi-agent LLM systems create **privacy risks that current benchmarks cannot measure**. When agents coordinate on tasks, sensitive data passes through:
- Inter-agent messages
- Shared memory
- Tool arguments

All pathways that output-only audits never inspect.

## What AgentLeak Does

- **First full-stack benchmark** for privacy leakage covering internal channels
- 1,000 scenarios across healthcare, finance, legal, and corporate domains
- Paired scenarios testing sensitive vs. non-sensitive data flow
- Measures leakage across all three pathways (messages, memory, tools)

## Key Finding for Synthetic Membrane

> "When agents coordinate on tasks, sensitive data passes through inter-agent messages, shared memory, and tool arguments, all pathways that output-only audits never inspect"

This directly validates the synthetic membrane's core challenge: **shared memory IS a privacy vector**. Any membrane implementation must address:

1. **Selective exposure** — agents control what they share (permeability)
2. **Audit trails** — track what data flows through shared memory
3. **Domain isolation** — healthcare data shouldn't leak to finance agents

## Security Implications

This paper confirms that trust/security cannot be an afterthought in multi-agent design. The membrane must bake in:
- Per-agent encryption of shared state
- Access control at the memory layer
- Leakage monitoring and alerting

## Related

- [[trust-models]] — Direct security concerns
- [[membrane-architecture]] — Permeability layer must prevent leakage
- [[blocka2a]] — Blockchain-based verification could help
- [[mcp-security]] — Related: MCP protocol security analysis

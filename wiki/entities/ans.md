---
title: Agent Name Service (ANS)
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [protocol, agent-communication, architecture]
sources: [raw/papers/ans-2505.10609.md]
confidence: high
---

# Agent Name Service (ANS)

A DNS-based universal directory for secure AI agent discovery and interoperability. Proposed by Ken Huang et al. (2025).

## What It Does

- **Agent Discovery**: DNS-based public registry where agents can be discovered by name
- **Protocol-Agnostic**: Registry mechanism works across different agent protocols (MCP, A2A, custom)
- **PKI Identity**: Uses Public Key Infrastructure certificates for verifiable agent identity
- **Trust Chains**: Enables trust verification between previously unknown agents

## Relevance to Synthetic Membrane

ANS solves a foundational problem for the membrane: **how do agents discover each other?** In biological systems, cells detect neighbors through chemical signaling and membrane receptors. ANS provides a similar discovery layer for AI agents.

For the synthetic membrane, ANS could serve as the discovery mechanism — agents register their presence, capabilities, and permeability settings. Other agents can query ANS to find collaborators.

## Key Architecture

- DNS-based addressing system
- PKI certificate infrastructure for identity
- Protocol-agnostic registry layer
- Supports both public and private registries

## Limitations

- DNS-based approach may have latency issues for real-time coordination
- Requires PKI infrastructure setup
- Discovery ≠ communication — still needs a transport protocol
- Privacy implications: public registration reveals agent existence and capabilities

## Related

- [[mcp-protocol]] — ANS could discover MCP servers
- [[a2a-protocol]] — ANS could discover A2A-capable agents
- [[trust-models]] — PKI-based identity is foundational for trust
- [[blocka2a]] — Complementary blockchain-based approach

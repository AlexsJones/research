---
title: AIP — Agent Identity Protocol for Verifiable Delegation
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [protocol, architecture, multi-agent, interface]
sources: [raw/articles/2603-24775.md]
confidence: high
---

# AIP — Agent Identity Protocol for Verifiable Delegation Across MCP and A2A

## Overview

**AIP** (Agent Identity Protocol), by Sunil Prakash, addresses a critical gap: neither MCP nor A2A verify agent identity. A scan of ~2,000 MCP servers found **all lacked authentication**.

## Key Innovation: Invocation-Bound Capability Tokens (IBCTs)

IBCTs fuse identity, attenuated authorization, and provenance binding into a single append-only token chain:

- **Compact mode**: Signed JWT for single-hop cases (0.049ms verification in Rust, 0.189ms in Python)
- **Chained mode**: Biscuit token with Datalog policies for multi-hop delegation

## Key Properties

- **Zero prior implementation found** that jointly combines: public-key verifiable delegation, holder-side attenuation, expressive chained policy, transport bindings across MCP/A2A/HTTP, and provenance-oriented completion records
- **Performance**: 0.22ms overhead over no-auth in real MCP-over-HTTP; 2.35ms total in multi-agent Gemini deployment (0.086% of end-to-end latency)
- **Security**: 600 adversarial attacks attempted, **100% rejection rate**; two attack categories uniquely caught by chained delegation (delegation depth violation, audit evasion)
- **Reference implementations** in Python and Rust with cross-language interoperability

## Membrane Relevance

AIP is the missing authentication layer for the membrane's Layer 0 (Identity). It provides:

- **Verifiable identity** across MCP and A2A transports — agents prove who they are
- **Attenuated delegation** — principal grants agent specific capabilities, not full access
- **Provenance chains** — every delegation step is recorded, enabling [[failure-attribution]]
- **Multi-hop safety** — chained tokens prevent unauthorized deep delegation

This directly enables the membrane's identity-gated permeability ([[gated-permeability]]) and reputation systems ([[agent-reputation-systems]]).

## Relationship to Existing Standards

| Standard | Identity? | Delegation? | Provenance? |
|----------|-----------|-------------|-------------|
| MCP | ❌ No | ❌ No | ❌ No |
| A2A | ❌ No | ⚠️ Partial | ❌ No |
| [[erc-8004]] | ✅ On-chain | ⚠️ Transfer | ⚠️ On-chain |
| [[ans]] | ✅ PKI | ❌ No | ❌ No |
| **AIP** | ✅ PKI+JWT | ✅ Attenuated | ✅ Chain |

AIP fills the intersection that no other protocol covers: identity + delegation + provenance, transport-agnostic.

## Open Questions

- How does AIP integrate with blockchain-based identity ([[erc-8004]])?
- Can AIP's IBCTs serve as the membrane's Layer 0 primitive?
- How does delegation depth scale in large swarms?

## Related

- [[agent-identity-cryptography]] — Trust foundations, now with AIP as key component
- [[mcp-protocol]] — MCP lacks auth; AIP extends it
- [[a2a-protocol]] — A2A lacks auth; AIP extends it
- [[framework-integration]] — Cross-framework identity is prerequisite
- [[event-sourcing]] — IBCT chains are naturally event-sourced
- [[agent-security-trust]] — Authentication is the first line of defense

[[agent-identity-cryptography]] [[mcp-protocol]] [[a2a-protocol]] [[erc-8004]] [[event-sourcing]] [[agent-security-trust]]

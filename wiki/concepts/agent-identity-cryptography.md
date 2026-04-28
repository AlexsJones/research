---
title: Agent Identity and Cryptography — Trust Foundations for Membranes
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [architecture, protocol, risk, multi-agent]
sources: [entities/erc-8004.md, entities/ans.md, entities/pass-ai-wallets.md, entities/aip-protocol.md]
confidence: high
---

# Agent Identity and Cryptography — Trust Foundations for Membranes

## The Problem

For agents to coordinate through a membrane, they must answer fundamental questions:
1. **Who are you?** — Agent identity and authentication
2. **Are you who you claim?** — Identity verification
3. **Can I trust your state writes?** — Provenance and non-repudiation
4. **Can I control what you access?** — Fine-grained delegation and revocation

This is Layer 0 of the membrane — sitting below permeability, memory, and coordination.

## Approaches to Agent Identity

### 1. PKI-Based ([[ans]])

**How it works**: DNS-based registry with PKI certificates
- Strong identity verification via certificate chains
- Trust anchors enable cross-agent trust
- **Tradeoff**: Requires PKI infrastructure; centralized trust roots

### 2. Blockchain-Based ([[erc-8004]])

**How it works**: On-chain tokens as agent identity (ERC-8004 standard)
- Decentralized, verifiable identity without central authority
- On-chain reputation tracking
- Transferable ownership while maintaining identity
- **Tradeoff**: Blockchain overhead; privacy concerns; gas costs
- **New data**: [[erc-8004-dataset]] — 10,000 agents registered on Ethereum mainnet

### 3. Resource Delegation ([[pass-ai-wallets]])

**How it works**: Provenanced subaccounts for fine-grained access delegation (PASS)
- Fine-grained delegation of wallet capabilities
- Audit trail of every access grant
- Revocation without key rotation
- **Tradeoff**: Primarily designed for financial resources, not general capabilities

### 4. AIP: Verifiable Delegation ([[aip-protocol]]) ⭐ NEW

**How it works**: Invocation-Bound Capability Tokens (IBCTs) fuse identity, attenuated authorization, and provenance into a single token chain
- Compact mode: signed JWT for single-hop (0.049ms verification)
- Chained mode: Biscuit token with Datalog policies for multi-hop delegation
- **Critical gap filled**: Scan of 2,000 MCP servers — ALL lacked authentication
- 100% attack rejection rate across 600 adversarial attempts
- 2.35ms overhead (0.086% of total latency) in multi-agent deployment
- Reference implementations in Python and Rust
- **Best option for membrane Layer 0**: combines identity + delegation + provenance

## Protocol Comparison Matrix

| Standard | Identity? | Delegation? | Provenance? | Authenticated? |
|----------|-----------|-------------|-------------|----------------|
| MCP | ❌ No | ❌ No | ❌ No | ❌ No |
| A2A | ❌ No | ⚠️ Partial | ❌ No | ❌ No |
| [[erc-8004]] | ✅ On-chain | ⚠️ Transfer | ⚠️ On-chain | ✅ On-chain |
| [[ans]] | ✅ PKI | ❌ No | ❌ No | ✅ PKI |
| **[[aip-protocol]]** | ✅ PKI+JWT | ✅ Attenuated | ✅ Chain | ✅ Yes |

AIP fills the intersection that no other protocol covers: identity + delegation + provenance, transport-agnostic, with sub-millisecond overhead.

## Design Principles for Membrane Identity

| Principle | Rationale | Implementation |
|-----------|-----------|----------------|
| **Self/non-self distinction** | Immune system analog: recognize legitimate vs. malicious | Cryptographic identity verification |
| **Non-repudiation** | Agents can't deny their state writes | Signed state changes via [[event-sourcing]] |
| **Capability attestation** | Verify what an agent can actually do | Behavioral signals ([[agentsearchbench]]) |
| **Dynamic revocation** | Remove access without destroying identity | Per-credential revocation lists |
| **Privacy-preserving** | Identity ≠ full capability disclosure | Selective disclosure via [[gated-permeability]] |

## Integration with Membrane Layers

### Layer 0: Trust & Identity
- Agent registration and verification
- Identity format (PKI, blockchain, or hybrid)
- Reputation initialization

### Layer 1: Permeability + Identity
- Access control based on identity
- Per-agent permeability rules
- Identity-gated communication channels

### Layer 2: Shared Memory + Provenance
- All writes signed with agent identity
- Full audit trail of who wrote what
- Enables [[failure-attribution]]

### Layer 3: Coordination + Reputation
- Reputation-weighted consensus ([[quorum-sensing-agents]])
- Identity-based routing ([[gossip-protocols]])
- Adaptive trust ([[agent-reputation-systems]])

## Open Questions

- Should the membrane define its own identity format or compose existing standards?
- PKI vs. blockchain vs. hybrid — what's the right tradeoff?
- How do agents prove capabilities without leaking implementation?
- Can identity be privacy-preserving while still verifiable (e.g., zero-knowledge proofs)?
- How does identity interact with agent evolution (an agent that changes its model)?

## Related

- [[agent-security-trust]] — Security model requiring identity as foundation
- [[aip-protocol]] — Agent Identity Protocol: best candidate for Layer 0 implementation
- [[ans]] — PKI-based agent naming and discovery
- [[erc-8004]] — Blockchain-based agent identity
- [[erc-8004-dataset]] — Empirical data on 10K blockchain-registered agents
- [[pass-ai-wallets]] — Fine-grained resource delegation
- [[immune-inspired-defense]] — Self/non-self distinction
- [[event-sourcing]] — Provenance through signed writes
- [[runtime-governance]] — Path-dependent policy evaluation uses agent identity

[[agent-security-trust]] [[aip-protocol]] [[ans]] [[erc-8004]] [[immune-inspired-defense]] [[event-sourcing]] [[runtime-governance]]

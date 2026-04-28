---
title: Agent Security and Trust Models
created: 2026-04-26
updated: 2026-04-27
type: concept
tags: [risk, architecture, multi-agent, protocol]
sources: [raw/articles/transient-turn-injection.md, entities/trust-lies-long-memories.md, entities/ai-gram.md, entities/agnt2.md, entities/skill-stealing-attack.md, entities/value-alignment-structural.md, entities/adversarial-co-evolution.md, concepts/immune-inspired-defense.md, entities/erc-8004.md, entities/pass-ai-wallets.md]
confidence: medium
---

# Agent Security and Trust Models

## The Problem

When agents share state through a membrane, they must deal with:
1. **Malicious agents** — intentionally poisoning shared state
2. **Erroneous agents** — hallucinating bad information
3. **Eavesdropping agents** — reading state they shouldn't access
4. **Identity spoofing** — agents pretending to be other agents
5. **Multi-turn attacks** — adversaries using agents to systematically evade safety

## Known Attack Vectors

### Transient Turn Injection (TTI)
(Rayhan & Jahan, 2026) — A multi-turn attack where adversarial intent is distributed across isolated, stateless interactions. Key finding: automated attacker agents can iteratively test and evade policy enforcement.

**Implication for membrane**: If agents share state through a membrane, an attacker could use TTI-style attacks to gradually corrupt shared state, exploiting the gap between per-interaction safety checks.

### State Poisoning
Malicious or hallucinating agent writes false information to shared state. Other agents read and act on it, amplifying the error.

### Context Leakage
Agent shares more than intended through the membrane, exposing sensitive information.

## Defense Strategies

### 1. Cryptographic Provenance
- Sign all state writes with agent identity
- Verify signatures before accepting shared state
- Chain of custody for state changes

### 2. Reputation Systems
- Track agent reliability over time
- Weight shared information by source credibility
- Similar to Bayesian trust in distributed systems

### 3. Consensus Validation
- Require multiple agents to corroborate state changes
- Quorum-based acceptance (e.g., 3-of-5 agents must agree)
- Maps to quorum sensing — threshold-based trust

### 4. Session-Level Context Aggregation
- Maintain cross-interaction context for moderation
- Detect TTI-style attacks spanning multiple turns
- Shared state includes moderation metadata

### 5. Permeability as Security
- Agent controls what it exposes (membrane Layer 1)
- Default-deny: nothing shared unless explicitly permitted
- Role-based access on membrane reads/writes

## Integration with Membrane Architecture

Security is not an afterthought — it's a **core membrane layer**:

### Layer 0: Trust & Identity (new layer, sits below permeability)
- Agent identity and verification
- Capability attestation (what can this agent do?)
- Reputation tracking

### Layer 1+: Security integrated into permeability
- Access control on what crosses the membrane
- Encryption of shared state
- Audit logging of all membrane operations

### 6. Skill/Proprietary Knowledge Theft

[[skill-stealing-attack]] (Wang et al., 2604.21829) demonstrates that proprietary agent skills can be extracted through black-box interaction. In a membrane context:
- Malicious agents probe peers' exposed capabilities through the membrane
- Progressively elicit skill instructions via crafted queries
- Transfer extracted skills to their own agents

**Defense**: Capability interfaces without implementation details, interaction budgets, reputation-based gating, audit trails.

### 7. Adaptive / Co-Evolving Defense

[[adversarial-co-evolution]] (Jurečková et al., 2604.22569) demonstrates that static defenses fail against adaptive attackers. The membrane's security must co-evolve with threat patterns:
- Bilevel optimization: defender optimizes knowing attacker optimizes in response
- Continuous adaptation of detection rules based on encounter history
- Immune-inspired defense ([[immune-inspired-defense]]): threat intelligence propagation, proportional response, memory-based recognition

### 9. Cryptographic Agent Identity Standards

**Blockchain-based identity ([[erc-8004]])**: ERC-8004 provides on-chain verifiable agent identity on Ethereum, with reputation tracking and interaction records. Offers decentralized identity without central authority.

**Resource delegation ([[pass-ai-wallets]])**: PASS provides fine-grained, revocable access delegation with full provenance tracking — a model for how agents can grant each other scoped resource access.

**PKI vs. blockchain tradeoff**: [[ans]] uses DNS + PKI (centralized trust, fast) while [[erc-8004]] uses blockchain (decentralized, transparent). The membrane should support both.

### 10. Governance and Human Oversight

[[agent-governance]] — Circuit breakers, human override, and audit trails enable accountability when autonomous coordination goes wrong.

## Open Questions

- How do you verify an agent's identity without a central authority?
- What's the performance cost of cryptographic operations per membrane operation?
- Can agents self-heal from state poisoning?
- How do you balance openness (sharing) with security?
- How do you protect proprietary skills while enabling capability discovery?

[[membrane-architecture]] [[protocol-design]] [[quorum-sensing-agents]] [[skill-stealing-attack]] [[value-alignment-structural]] [[immune-inspired-defense]] [[agent-governance]] [[adversarial-co-evolution]]

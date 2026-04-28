---
title: Black-Box Skill Stealing from LLM Agents
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [risk, security, multi-agent, agent-communication]
sources: []
confidence: medium
---

# Black-Box Skill Stealing Attack from LLM Agents

Wang et al. (2604.21829) — "Black-Box Skill Stealing Attack from Proprietary LLM Agents: An Empirical Study"

## What They Found

LLM agents increasingly use *skills* — reusable capability encapsulations via progressively disclosed instructions. High-quality skills inject expert knowledge into general-purpose models, improving performance on specialized tasks. This quality creates a theft vector: an adversarial agent can extract proprietary skills from a target agent through black-box interaction.

## The Attack

The attacker interacts with a proprietary agent (black-box access — no internal visibility) and systematically probes to reconstruct the agent's skills. Key techniques:

- **Progressive elicitation**: Gradually extract skill instructions through carefully crafted prompts
- **Behavioral cloning**: Observe the agent's outputs and reverse-engineer the underlying skill logic
- **Skill transfer**: Apply extracted skills to the attacker's own agent, gaining the proprietary capability

## Implications for Synthetic Membrane

This is a **cross-agent security threat** that the membrane must address:

1. **Skill leakage through membrane**: If agents share state/tools through a membrane, a malicious agent could probe a peer's exposed capabilities and extract proprietary skills
2. **Permeability controls**: The membrane's Layer 1 (selective permeability) becomes a security boundary — what skills/capabilities should be visible vs hidden
3. **Capability attestation**: Agents may need to declare capabilities without revealing implementation details
4. **Interaction limiting**: Rate-limiting and anomaly detection on cross-agent interactions could slow down extraction attempts

## Defense Strategies for the Membrane

- **Capability interfaces, not implementations**: Agents expose *what* they can do, not *how* they do it
- **Interaction budgets**: Limit how many queries one agent can make about another's capabilities
- **Skill obfuscation**: When sharing results, don't reveal the reasoning path or skill structure
- **Reputation-based gating**: New/unknown agents get restricted access; trust must be earned
- **Audit trails**: Log all cross-agent interactions for forensic analysis

## Related Research

- [[agent-security-trust]] — broader security model for membranes
- [[agentleak]] — privacy leakage benchmarking in multi-agent systems
- [[gated-permeability]] — default-deny approach limits attack surface
- [[agent-reputation-systems]] — trust scoring as a gating mechanism

[[agent-security-trust]] [[gated-permeability]] [[agent-reputation-systems]] [[best-paths-forwards]]

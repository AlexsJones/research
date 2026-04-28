---
title: Gated Permeability — Default-Deny Agent Communication
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [architecture, agent-communication, optimization, proposal]
sources: [entities/gated-coordination.md]
confidence: medium
---

# Gated Permeability

The principle that agent-to-agent communication should be opt-in rather than default — agents work locally by default and cross the membrane only when genuinely necessary.

## Origin

[[gated-coordination]] demonstrates that treating every local anomaly as an automatic communication trigger introduces:
- **Coordination noise**: unnecessary broadcasts that distract other agents
- **Token waste**: each inter-agent message consumes LLM tokens
- **Execution disruption**: interrupting local reasoning for marginal gains
- **Public overuse**: using shared channels for issues solvable privately

## The Gating Mechanism

Before crossing the membrane, an agent evaluates:
1. Can this be resolved with my own knowledge and tools?
2. Does the cost of communication exceed the expected benefit?
3. Is this information genuinely valuable to other agents, or just my local noise?

Only when the answer is "needs external input" does the agent broadcast.

## Design Implications for Synthetic Membrane

This fundamentally changes how we think about the membrane's Layer 1 (Permeability):

### Default-Deny Permeability
- **Current design**: agents expose state and subscribe to events
- **Gated refinement**: agents also have a *cost model* — they only expose when the information has cross-agent value
- The membrane could include a *gatekeeper function* that evaluates whether a contribution should enter the shared space

### Selective Broadcasting
- Instead of broadcasting all state changes, agents use the gate to filter
- The membrane could provide a *cost-benefit API*: "evaluate whether to broadcast this"
- This API could use learned heuristics or explicit rules

### Connection to Existing Concepts
- [[quorum-sensing-agents]] already uses thresholds — gated permeability adds cost evaluation to the threshold
- [[mcp-efficiency-optimizations]] lazy loading reduces schema overhead — gating reduces message overhead
- [[agent-security-trust]] — gated permeability naturally limits attack surface (less broadcast = less to intercept)

## Implementation Approaches

1. **Rule-based gating**: explicit thresholds and cost functions per agent type
2. **Learned gating**: train a small model to predict when communication is beneficial
3. **Reinforcement gating**: agents learn optimal communication policies through trial/error
4. **Hybrid**: rule-based defaults that agents can override with learned refinements

[[membrane-architecture]] [[protocol-design]] [[gated-coordination]] [[quorum-sensing-agents]] [[mcp-efficiency-optimizations]] [[best-paths-forwards]]

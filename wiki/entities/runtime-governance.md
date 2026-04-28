---
title: Runtime Governance for AI Agents — Policies on Paths
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [architecture, risk, proposal, multi-agent]
sources: [raw/articles/2603-16586.md]
confidence: high
---

# Runtime Governance for AI Agents: Policies on Paths

## Overview

By Maurits Kaptein, Vassilis-Javed Khan, Andriy Podstavnychy (2603.16586).

Addresses the fundamental challenge: AI agents produce non-deterministic, path-dependent behavior that cannot be fully governed at design time. Proposes that the **execution path** is the central object for runtime governance.

## Key Framework

Compliance policies formalized as deterministic functions mapping:
- **Agent identity** → who is acting
- **Partial path** → what has happened so far
- **Proposed next action** → what the agent wants to do next
- **Organizational state** → current context/rules

→ **Policy violation probability**

## Key Insight: Runtime Evaluation Is The General Case

- **Prompt-level instructions** (system prompts) shape the distribution over paths without evaluating them — they influence but cannot constrain
- **Static access control** evaluates deterministic policies that ignore the path — can only handle a subset of possible behaviors
- **Runtime evaluation** is the general case, necessary for any path-dependent policy

This framework subsumes both prompt engineering and static ACLs as special cases.

## Policy Examples

Inspired by the EU AI Act, with concrete examples of runtime policies that depend on execution history and organizational context.

## Membrane Relevance

This is the formal foundation for the membrane's **Layer -1: Governance**:

- **Path-dependent policies**: The membrane's [[event-sourcing]] layer provides the full execution history (partial path) needed for runtime policy evaluation
- **Identity integration**: Maps directly to [[agent-identity-cryptography]] — agent identity is a policy input
- **Provenance**: The membrane's event log is the "partial path" that runtime governance evaluates
- **Circuit breakers**: Runtime policies can trigger membrane circuit breakers when violation probability exceeds thresholds
- **Formal framework**: Provides mathematical grounding for governance that was previously informal

## Open Problems Identified

- Risk calibration — how to set acceptable violation thresholds
- Limits of enforced compliance — some policies may be unverifiable at runtime
- Performance overhead — evaluating policies on every action step

## Related

- [[agent-governance]] — Governance as Layer -1; this paper provides the formal framework
- [[event-sourcing]] — Provides the partial path for runtime evaluation
- [[agent-identity-cryptography]] — Identity as policy input
- [[distributed-legal-infrastructure]] — Legal framework for the agentic web
- [[best-paths-forwards]] — Governance as prerequisite for production

[[agent-governance]] [[event-sourcing]] [[agent-identity-cryptography]] [[best-paths-forwards]]

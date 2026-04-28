---
source_url: https://arxiv.org/abs/2604.19540
ingested: 2026-04-27
sha256: placeholder
---

# Mesh Memory Protocol: Semantic Infrastructure for Multi-Agent LLM Systems

**Authors:** Hongwei Xu
**Published:** 2026-04-21
**arXiv:** 2604.19540
**Categories:** cs.MA, cs.AI
**Citations (Semantic Scholar):** 0 (very new)

## Abstract

Teams of LLM agents increasingly collaborate on tasks spanning days or weeks: multi-day data-generation sprints where generator, reviewer, and auditor agents coordinate in real time on overlapping batches; specialists carrying findings forward across session restarts; product decisions compounding over many review rounds. This requires agents to share, evaluate, and combine each other's cognitive state in real time across sessions. We call this cross-session agent-to-agent cognitive collaboration, distinct from parallel agent execution.

To enable it, three problems must be solved together:
- (P1) Each agent decides field by field what to accept from peers, not accept or reject whole messages.
- (P2) Every claim is traceable to source, so returning claims are recognised as echoes of the receiver's own prior thinking.
- (P3) Memory that survives session restarts is relevant because of how it was stored, not how it is retrieved.

These are protocol-level properties at the semantic layer of agent communication, distinct from tool-access and task-delegation protocols at lower layers. The paper calls this missing protocol layer "semantic infrastructure," and the Mesh Memory Protocol (MMP) specifies it.

Four composable primitives work together:
1. **CAT7** — a fixed seven-field schema for every Cognitive Memory Block (CMB)
2. **SVAF** — evaluates each field against the receiver's role-indexed anchors (realises P1: selective field-level acceptance)
3. **Inter-agent lineage** — carried as parents and ancestors of content-hash keys (realises P2: source traceability)
4. **Remix** — stores only the receiver's own role-evaluated understanding of each accepted CMB, never the raw peer signal (realises P3: session-persistent memory)

MMP is specified, shipped, and running in production across three reference deployments, where each session runs an autonomous agent as a mesh peer with its own identity and memory, collaborating with other agents across the network for collective intelligence.

## Key Observations

- Distinguishes "cross-session cognitive collaboration" from parallel agent execution — a key insight
- The "semantic layer" is distinct from tool-access protocols (MCP) and task-delegation protocols (A2A)
- Field-level selectivity (P1) is more granular than typical message-level accept/reject
- Lineage tracking prevents echo chambers and circular reasoning
- The "remix" concept — storing the receiver's interpretation, not the raw signal — is a form of cognitive digestion
- Already in production use across three deployments

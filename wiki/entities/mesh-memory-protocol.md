---
title: Mesh Memory Protocol (MMP)
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [protocol, shared-state, multi-agent, agent-communication, architecture]
sources: [raw/articles/mesh-memory-protocol-2604.19540.md]
confidence: high
---

# Mesh Memory Protocol (MMP)

Hongwei Xu's proposal for "semantic infrastructure" — a protocol layer for cross-session, agent-to-agent cognitive collaboration.

## What It Is

MMP defines a protocol for LLM agents to share, evaluate, and combine each other's cognitive state across sessions. It's positioned as distinct from tool-access protocols (like [[mcp-protocol]]) and task-delegation protocols (like [[a2a-protocol]]) — it's the *semantic layer* between agents.

## Four Composable Primitives

1. **CAT7** — Fixed seven-field schema for every Cognitive Memory Block (CMB). Standardizes the structure of shared cognitive content.

2. **SVAF** — Selective Field Acceptance Filter. Each agent evaluates incoming CMBs field-by-field against its role-indexed anchors. Enables granular, field-level permeability rather than whole-message accept/reject.

3. **Inter-Agent Lineage** — Content-hash keys carry parents and ancestors. Every claim is traceable to source, preventing echo-chamber effects where agents re-echo each other's own prior thinking.

4. **Remix** — When accepting a peer's CMB, the agent stores only its own role-evaluated interpretation, never the raw peer signal. This "cognitive digestion" ensures session-persistent memory is relevant because of *how* it was stored, not how it was retrieved.

## Three Design Problems Addressed

- **P1** (Selectivity): Field-by-field acceptance, not whole-message
- **P2** (Traceability): Every claim traceable to source
- **P3** (Persistence): Memory survives session restarts through proper encoding

## Production Status

Already shipped and running in production across three reference deployments. Each session runs an autonomous agent as a mesh peer with its own identity and memory, collaborating for collective intelligence.

## Relevance to Synthetic Membrane

MMP is the closest existing work to the synthetic membrane concept. It directly addresses:
- The membrane's Layer 1 (permeability): SVAF implements field-level selectivity
- The membrane's Layer 2 (shared medium): CMBs with CAT7 schema are the shared cognitive units
- Source traceability: lineage tracking prevents pollution of shared state
- Session persistence: remix ensures durable, meaningful memory

Key difference from our membrane proposal: MMP focuses on *semantic/cognitive* sharing while our membrane also emphasizes *coordination/swarm* primitives. MMP could be integrated as the shared-state protocol layer atop our coordination architecture.

## Comparison with Other Approaches

- vs [[mcp-protocol]]: MMP is semantic/cognitive; MCP is tool access
- vs [[a2a-protocol]]: MMP is state-oriented; A2A is message/delegation-oriented
- vs [[diffmas]]: MMP uses structured semantic blocks; DiffMAS uses raw KV caches
- vs [[codecrdt]]: MMP has explicit lineage; CRDTs handle conflict resolution

[[membrane-architecture]] [[protocol-design]] [[mcp-protocol]] [[a2a-protocol]] [[diffmas]] [[best-paths-forwards]]

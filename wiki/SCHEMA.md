# Wiki Schema — Synthetic Membrane

## Domain
Research into "synthetic membrane" — a protocol/abstraction enabling AI agents to share information, coordinate, and swarm. Covers: multi-agent communication protocols, shared memory architectures, agent-to-agent interfaces (MCP, skills, custom protocols), orchestration patterns, swarm intelligence, and biological inspiration (cell membranes, gap junctions, quorum sensing).

## Conventions
- File names: lowercase, hyphens, no spaces
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md`
- Every action appended to `log.md`

## Tag Taxonomy
- Core: protocol, architecture, interface, shared-state, swarm, orchestration
- Agent: multi-agent, agent-communication, agent-coordination, agent-memory
- Pattern: pubsub, event-sourcing, gossip, consensus, blackboard,黑板
- Bio-inspiration: cell-membrane, gap-junction, quorum-sensing, neural
- Tech: MCP, skills, gRPC, websocket, NATS, Redis, Kafka, protobuf
- Meta: comparison, timeline, proposal, open-question, risk

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
---
```

## Page Thresholds
- Create a page when concept appears in 2+ sources OR is central to one source
- Split pages over 200 lines
- Archive when fully superseded

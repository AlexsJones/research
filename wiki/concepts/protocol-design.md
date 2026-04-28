---
title: Protocol Design Considerations
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["protocol", "architecture", "open-question"]
sources: []
confidence: medium
---

# Protocol Design Considerations

## What Would a Membrane Protocol Look Like?

### Message Types
1. **EXPOSE** — "I'm making this state/capability available"
2. **SUBSCRIBE** — "Notify me when this changes"
3. **READ** — "I want to see this agent's exposed state"
4. **WRITE** — "I'm contributing to shared state"
5. **BROADCAST** — "Attention, I need help with this"
6. **SWARM** — "I'm claiming/dropping this task"
7. **DECAY** — "This information is expiring"

### Permeability Rules
Each agent defines:
- `expose: [state_keys]` — what it shares
- `subscribe: [patterns]` — what triggers it
- `trust: [agent_ids]` — whose state it trusts
- `swarm_threshold: N` — when to activate swarm mode

### Wire Format
Candidates:
- Protobuf (efficient, typed)
- JSON (flexible, debuggable)
- CBOR (binary JSON, compact)
- Cap'n Proto (zero-copy, fastest)

### Transport
- gRPC for structured RPC
- WebSockets for bidirectional streaming
- NATS for pub/sub at scale
- HTTP/3 for simplicity

## Integration Points
- MCP: membrane as an MCP server exposing shared state
- A2A: membrane as the transport for A2A messages
- LangGraph: membrane as the shared state backend
- AutoGen: membrane as inter-agent communication layer


---
title: Framework Integration Strategies for Membranes
created: 2026-04-27
updated: 2026-04-27
type: concept
tags: [architecture, protocol, multi-agent, agent-communication]
sources: [entities/mcp-protocol.md, entities/langgraph.md, entities/autogen.md, entities/a2a-protocol.md, entities/mesh-memory-protocol.md, entities/openai-swarm.md, entities/letta.md]
confidence: medium
---

# Framework Integration Strategies for Membranes

The synthetic membrane needs to work with existing agent frameworks to be practical. Each framework has different primitives, and the membrane must adapt.

## Existing Frameworks

### [[mcp-protocol]] — Model Context Protocol (Anthropic)
- **Strength**: Rapidly becoming the standard for agent interfaces
- **Integration**: Membrane as an MCP server exposing shared-state operations
- **Path**: Fastest to ship — agents already speak MCP, just need new tool definitions
- **Limitation**: MCP is tool-oriented, not agent-to-agent oriented

### [[a2a-protocol]] — Agent-to-Agent Protocol (C4AI)
- **Strength**: Designed specifically for agent-to-agent communication
- **Integration**: Membrane extends A2A with shared-state operations
- **Path**: Natural fit for Layer 1 (permeability protocol)
- **Limitation**: Lacks shared-memory primitives; message-based only

### [[langgraph]] — LangChain's State Machine Orchestration
- **Strength**: Explicit state management, good for structured workflows
- **Integration**: Membrane as an external state node in LangGraph workflows
- **Path**: Membrane provides inter-workflow state sharing
- **Limitation**: Tied to LangChain ecosystem

### [[autogen]] — Microsoft's Multi-Agent Conversations
- **Strength**: Already multi-agent, good conversation patterns
- **Integration**: Membrane as a shared memory backend for AutoGen agents
- **Path**: Replace or augment AutoGen's internal group chat with membrane
- **Limitation**: AutoGen's coordination is conversation-based, not state-based

### [[openai-swarm]] — OpenAI Swarm (Lightweight Handoff)
- **Strength**: Minimal overhead, simple handoff pattern, OpenAI-native
- **Integration**: Membrane wraps Swarm's handoff mechanism, adding shared state
- **Path**: Easiest to wrap due to simplicity — membrane adds the state layer Swarm lacks
- **Limitation**: No shared state, single-provider, no discovery or swarm intelligence

### [[letta]] — Persistent Memory Agent Framework
- **Strength**: Sophisticated memory architecture (core/archival/episodic)
- **Integration**: Membrane connects Letta agents' personal memories into a shared space
- **Path**: Membrane acts as the "gap junction" between Letta-style agents
- **Limitation**: Single-agent focused; no inter-agent coordination primitives

## Integration Strategies

### Strategy 1: Membrane as Service (Recommended)
Build membrane as a standalone service. Each framework connects via its native protocol (MCP, REST, gRPC). The membrane translates between protocols internally.

### Strategy 2: Membrane as Library
Ship membrane as a library each framework can import. Framework-specific adapters handle protocol translation.

### Strategy 3: Membrane as Protocol Standard
Define membrane as a protocol specification. Each framework implements it natively.

## Recommended Approach

**Hybrid**: Start with Strategy 1 (service) for rapid prototyping. Define the protocol spec (Strategy 3) in parallel. As frameworks adopt the spec, migrate to Strategy 2 (library) for lower overhead.

## Cross-Framework Compatibility

The membrane should enable agents from different frameworks to coordinate:
- An MCP-speaking agent can share state with a LangGraph agent
- An AutoGen conversation can read from membrane shared memory
- The membrane translates protocol-specific messages into its internal format

## Open Questions

- How do we handle different consistency models across frameworks?
- What's the overhead of protocol translation?
- Can we define a minimal membrane protocol that all frameworks can implement?
- How do we handle framework-specific security models?

[[membrane-architecture]] [[protocol-design]] [[best-paths-forwards]] [[mcp-protocol]] [[a2a-protocol]]

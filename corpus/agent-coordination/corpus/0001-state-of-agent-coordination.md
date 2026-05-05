# The State of Agent Coordination: Frameworks, Protocols, and Gaps

**Date:** 2026-05-05
**Researcher:** Claude Code (delegated via `claude -p`)

## Context

This survey maps the current landscape of agent coordination frameworks and protocols against the synthetic membrane thesis. The central claim: production-scale systems converge on the same symptoms — disconnected agents, separate contexts, broken governance at scale — that a permeable shared boundary would address.

## Current Frameworks and Their Coordination Models

### Orchestration-Based: LangGraph
- **How it works:** Directed graph with conditional edges over a centralized state object. Supports scatter-gather, pipeline parallelism, and subgraphs.
- **Coordination primitives:** Centralized state passing, graph-defined flow control.
- **Limitations:** Coordination is *top-down* — the graph author decides flow; agents don't sense each other. Token efficiency comes from passing state deltas, not full histories. Debugging distributed runs and human-in-the-loop bottlenecks are recurring issues.
- **Gap:** No ambient sensing. Agents are graph nodes, not autonomous participants.

### Orchestration-Based: CrewAI
- **How it works:** Role-based crews under a manager-worker pattern.
- **Coordination primitives:** Static memory, role-based task assignment.
- **Limitations:** The manager doesn't actually coordinate — execution collapses to sequential task chaining, producing wrong tool calls and high latency. Memory is static and doesn't evolve across sessions. CrewAI's own postmortem on 1.7B workflows says the gap "isn't intelligence, it's architecture."
- **Gap:** No dynamic coordination; rigid role assignment.

### Conversation-Based: AutoGen → Microsoft Agent Framework
- **How it works:** AutoGen merged with Semantic Kernel into Microsoft Agent Framework (GA Oct 2025). Async event-driven core with five named patterns: sequential, concurrent, handoff, group chat, and Magentic-One. Native A2A and MCP support.
- **Coordination primitives:** Pattern-based communication, event-driven messaging.
- **Limitations:** AutoGen itself is in maintenance mode. The new framework is more capable but still fundamentally message-passing.
- **Gap:** Pattern-based coordination is still explicit messaging, not ambient sharing.

### Protocol-Based: Google A2A (Agent2Agent)
- **How it works:** Donated to the Linux Foundation; v0.3 adds gRPC, signed agent cards, async push. JSON-RPC 2.0 over HTTP with "Agent Cards" for discovery and a task object with a lifecycle.
- **Coordination primitives:** Agent cards for discovery, task lifecycle management.
- **Limitations:** Still **RPC-style** request/response/streaming — interop for message passing, not a shared medium.
- **Gap:** Protocol for messaging, not for state sharing.

### Tool Access: Anthropic MCP (Model Context Protocol)
- **How it works:** Donated to the Agentic AI Foundation (Anthropic, Block, OpenAI; backed by Google, MS, AWS, Cloudflare, Bloomberg). Adopted by OpenAI/ChatGPT. Nov 2025 spec adds async ops, statelessness, server identity.
- **Coordination primitives:** Tool standardization, server identity.
- **Limitations:** MCP is **agent-to-tool**, not **agent-to-agent**. It does not provide coordination between agents.
- **Gap:** Foundational for tool access but orthogonal to coordination.

## Academic Perspectives on Multi-Agent Coordination

### Survey Thread (Jan–Feb 2025)
1. **Tran et al.** *Multi-Agent Collaboration Mechanisms* (arXiv:2501.06322) — decomposes coordination into actors/types/structures/strategies/protocols.
2. **Beyond Self-Talk** (arXiv:2502.14321) — argues prior surveys ignored communication as the central object.
3. **Multi-Agent Coordination across Diverse Applications** (arXiv:2502.14743) — frames four questions: what/why/who/how to coordinate.

### Failure Taxonomy — Directly Supports the "Missing Layer" Claim
**Cemri et al. — *Why Do Multi-Agent LLM Systems Fail?*** (arXiv:2503.13657, ICLR 2025)
- Built MAST from 1,600+ annotated traces across 7 frameworks.
- Three failure clusters: system design, **inter-agent misalignment**, task verification.
- Specific rates: reasoning-action mismatch 13.2%, task derailment 7.4%, wrong-assumption 6.8%, ignoring other agents 1.9%, info withholding 0.85%.
- **Root cause:** Agents fail at *theory of mind* — they don't model what other agents need to know — and unstructured text ambiguity.
- **This is the gap, named and measured.**

### Blackboard Architectures Returning
- arXiv:2510.01285 (Oct 2025) and arXiv:2507.01701 (Jul 2025) revive the 1980s blackboard pattern for LLM MAS.
- Agents *autonomously decide* whether to contribute to a posted task rather than being assigned.
- Reported 13–57% improvement over RAG and master-slave on data-discovery tasks.
- **Closest published prior art to the "shared permeable medium" concept.**

## Identified Gaps (Mapped to Membrane Layers)

| Membrane Layer | Status in 2026 Frameworks |
|---|---|
| **Governance (L-1)** | Single-agent policies fail under multi-agent access; no shared policy substrate |
| **Discovery (L0)** | Partial — A2A Agent Cards, MCP registry — but only at *connection* time, not ambient |
| **Permeability (L1)** | **Absent.** Agents have walled contexts; no controlled diffusion |
| **Shared Medium (L2)** | Nearest prior art is LLM blackboard work; LangGraph's central state is closest in production but is orchestrator-owned, not ambient |
| **Coordination (L3)** | All frameworks reduce to message passing or graph orchestration; no ambient sensing |
| **Immune (cross-cutting)** | **Absent.** MAST shows misalignment goes undetected at runtime |

## Relevance to Synthetic Membrane

The strongest evidence for the thesis: production-scale critiques converge on "disconnected agents maintain separate contexts; governance for one agent breaks for many; debugging grows exponentially" — exactly the symptoms a permeable shared boundary would address.

The blackboard architecture papers (2025) are the closest published work to the membrane thesis. They demonstrate that when agents can autonomously choose to contribute to shared knowledge (rather than being assigned tasks), coordination improves 13–57%. The membrane extends this from a single blackboard to a multi-layer permeable medium with governance, discovery, and immune layers.

## Relevance to Sympozium

Sympozium's Kubernetes-based orchestration is positioned to implement the membrane's coordination layer. Key implications:
1. Sympozium should provide ambient discovery (not just explicit A2A handoffs)
2. Task routing should be capability-based, not just graph-defined
3. The orchestration layer should maintain shared state that agents can sense (not just pass)
4. Incident response scenarios are ideal test cases — they require exactly the coordination primitives the membrane provides

## Open Questions

1. How do we measure "coordination quality" — is there a benchmark analogous to MAST but for coordination specifically?
2. What are the token economics of a shared medium vs. message passing? Does the membrane reduce or increase token overhead?
3. How does the blackboard pattern scale beyond small agent teams (10-50 agents)?
4. What incident management scenarios would best validate the membrane approach?
5. How do we handle conflicting hypotheses from different agents in the shared medium?

## References

- [LangGraph Multi-Agent Orchestration Guide 2025 — Latenode](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-multi-agent-orchestration-complete-framework-guide-architecture-analysis-2025)
- [Why CrewAI's Manager-Worker Architecture Fails — Towards Data Science](https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/)
- [How to build Agentic Systems: The Missing Architecture — CrewAI Blog](https://www.crewai.com/blog/how-to-build-agentic-systems-the-missing-architecture-for-production-ai-agents)
- [Microsoft Agent Framework v1.0 — DevBlogs](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Announcing the Agent2Agent Protocol — Google Developers](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [Donating MCP to the Agentic AI Foundation — Anthropic](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [Multi-Agent Collaboration Mechanisms: A Survey of LLMs (arXiv:2501.06322)](https://arxiv.org/abs/2501.06322)
- [Beyond Self-Talk: A Communication-Centric Survey (arXiv:2502.14321)](https://arxiv.org/pdf/2502.14321)
- [Multi-Agent Coordination across Diverse Applications (arXiv:2502.14743)](https://arxiv.org/html/2502.14743v2)
- [Why Do Multi-Agent LLM Systems Fail? MAST (arXiv:2503.13657)](https://arxiv.org/abs/2503.13657)
- [LLM-Based Multi-Agent Blackboard System (arXiv:2510.01285)](https://arxiv.org/abs/2510.01285)
- [Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture (arXiv:2507.01701)](https://arxiv.org/abs/2507.01701)
- [AI Agent Orchestration Frameworks in 2026 — Catalyst & Code](https://www.catalystandcode.com/blog/ai-agent-orchestration-frameworks)
- [Multi-Agent Systems & AI Orchestration Guide 2026 — Codebridge](https://www.codebridge.tech/articles/mastering-multi-agent-orchestration-coordination-is-the-new-scale-frontier)

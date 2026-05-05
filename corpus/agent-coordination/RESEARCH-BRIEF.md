# Research Brief: Agent-to-Agent Operational Coordination

## Project Context

This research builds on the **Synthetic Membrane** position paper (April 2026) by AlexsJones, which argues that multi-agent AI systems lack a shared, permeable boundary for coordination. The synthetic membrane proposes six layers (Governance, Discovery, Permeability, Shared Medium, Coordination, Immune) as the missing substrate.

**Sympozium** (sympozium-ai/sympozium) is a Kubernetes-based AI agent orchestration platform that aims to fill this gap.

## Research Focus

**Operational Coordination**: How agents can be used in incident management to follow hypotheses and work together.

### Core Theory
There is a **missing coordination layer** that doesn't exist in current agent frameworks. Current approaches rely on:
- Message passing (A2A, ANP)
- Orchestration graphs (LangGraph, CrewAI)
- Central planners
- Tool delegation (MCP)

None provides ambient, persistent, structured coordination that enables agents to:
1. Sense each other's presence and intent
2. Share hypotheses and evidence incrementally
3. Coordinate hypotheses without central control
4. Follow operational procedures together in incident management
5. Self-organize around incidents that emerge

### Key Research Questions

1. **What does "operational coordination" mean in practice?**
   - Incident management workflows (ITOps, security response, disaster response)
   - How do humans coordinate incidents? How should agents?
   - What are the primitives of operational coordination?

2. **What do current agent frameworks offer, and where do they fail?**
   - LangGraph: stateful graphs, but top-down orchestration
   - CrewAI: role-based collaboration, but rigid
   - AutoGen: conversation patterns, but no shared state
   - Anthropic A2A / ANP: message protocols, not state protocols
   - MCP: tool access, not inter-agent coordination
   - Others: OpenHands, AutoGPT, BabyAGI, etc.

3. **What are the flaws in current approaches?**
   - Token overhead of message shuffling (1000x non-agentic)
   - No ambient sensing between agents
   - Fragile coordination (breaks when agents change models/frameworks)
   - No shared medium for hypotheses/evidence
   - No persistence across agent sessions
   - No mechanism for emergent coordination

4. **What does incident management teach us about coordination?**
   - ICS (Incident Command System) structure
   - NIMS (National Incident Management System)
   - How multi-agency incident response works
   - Hypothesis-driven investigation (security incident triage)
   - Operational procedures and runbooks

5. **What would a coordination layer look like?**
   - Building on synthetic membrane architecture
   - Hypothesis sharing and testing between agents
   - Swarm coordination for incident response
   - Capability-based task routing
   - Quorum sensing for coordination triggers

## Research Methodology

For each research cycle, focus on:
1. **Survey current state**: What frameworks/tools exist for agent coordination?
2. **Identify gaps**: What specific coordination problems remain unsolved?
3. **Cross-domain analysis**: What can we learn from other fields? (ICS, distributed systems, swarm intelligence, biology)
4. **Case studies**: Real incident management scenarios where agent coordination matters
5. **Literature review**: Academic papers on multi-agent coordination, operational coordination

## Output Format

Each research cycle produces:
1. **Corpus entry** in `corpus/` — structured research notes on a specific topic
2. **Updated analysis** in `analysis/` — evolving synthesis of findings
3. **Key references** in `references/` — papers, articles, tools found

## Deliverables

- **Website article** for axjns.dev — accessible, well-illustrated explanation
- **Research paper** — academic contribution to multi-agent coordination literature

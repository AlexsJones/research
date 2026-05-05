# The Sticky-Note Problem: Why Multi-Agent AI Is Broken at the Coordination Layer

**By AlexsJones** · May 2026 · axjns.dev

---

## 1. The Incident That Never Happened

It's 2:47 AM. A detection agent spots anomalous outbound traffic from a production database server — 40 GB of encrypted data heading to an unfamiliar IP in the Cayman Islands. The agent runs a threat classification model, assigns the incident a severity of 9.2, and generates a recommendation: isolate the server from the network.

The containment agent, meanwhile, is three minutes away from executing a planned maintenance window that requires that exact server to be online. It has no idea the detection agent exists. The detection agent has no idea the containment agent exists. Both are receiving instructions from the same orchestration graph, but the graph's edges define *who talks to whom*, not *what everyone knows*.

The containment agent proceeds. The database goes offline during a peak traffic period. The detection agent, seeing no network activity on its target, downgrades the incident to false positive. The 40 GB exfiltration completes while both agents are quietly moving on.

This isn't a hypothetical. It's the default state of every multi-agent system built today.

You don't need to be a security expert to see what went wrong. You don't need to be an LLM expert either. You just need to have watched a team of humans work through an incident, however briefly, to know that the *shared situational awareness* missing here is not a nice-to-have — it's the entire reason incident response works at all.

Every framework on the market — LangGraph, CrewAI, AutoGen, Google A2A — gives you agents that send messages to each other. Messages. Strings of tokens that one agent serialises and another deserialises, with all the loss, ambiguity, and silence that implies. We are building systems of increasing intelligence with the equivalent of sticky notes passed between people in different rooms.

There is a better way. We just haven't been looking for it in the right place.

---

## 2. The Problem: Everything Is Messaging

The dominant pattern for multi-agent LLM systems is **orchestration**. A planner decomposes a task, dispatches subtasks to specialised agents, and stitches the results back together. This pattern works fine until it doesn't — and "until it doesn't" is closer than most teams want to admit.

Let's be generous to the frameworks and list what each actually provides:

**LangGraph** gives you a directed graph with conditional edges over a centralized state object. You can express scatter-gather, pipeline parallelism, and subgraphs. But coordination is *top-down* — the graph author decides flow, and agents don't sense each other. Agents are graph nodes, not autonomous participants. There is no ambient sensing.

**CrewAI** gives you role-based crews under a manager-worker pattern. The manager assigns tasks to roles, and roles execute sequentially. Memory is static. The manager doesn't actually coordinate — execution collapses to sequential task chaining, producing wrong tool calls and high latency. CrewAI's own postmortem on 1.7 billion workflows is frank about what's happening: *the gap isn't intelligence, it's architecture*.

**AutoGen** (now merged into Microsoft's Agent Framework) gives you async event-driven patterns: sequential, concurrent, handoff, group chat, and Magentic-One. More capable than its predecessor, but still fundamentally message-passing. Pattern-based coordination is still explicit messaging, not ambient sharing.

**Google A2A** (Agent-to-Agent Protocol) gives you typed task delegation, capability negotiation, and status updates over JSON-RPC 2.0. It's a message protocol, not a state protocol. It standardises *how agents talk*, not *what they share*.

**Anthropic MCP** (Model Context Protocol) standardises agent-to-tool communication. It's foundational for tool access, but orthogonal to coordination. MCP is about agents reaching *outwards to tools*. Nobody has standardised how agents reach *sideways to each other*.

That last sentence is the point. Every protocol, every framework, every architecture pattern solves a different problem. None solves the problem of a shared medium — the place where knowledge made by one agent becomes ambient knowledge for all of them.

The result is predictable: agents maintain separate contexts, governance for one agent breaks for many, and debugging grows exponentially with team size.

---

## 3. The Evidence: The Gap Is Named and Measured

This isn't a feeling. It's been measured.

The **MAST study** (Cemri et al., arXiv:2503.13657, ICLR 2025) compiled 1,600+ annotated failure traces across 7 different frameworks. Three failure clusters emerged: system design, inter-agent misalignment, and task verification. The inter-agent cluster is where the interesting numbers live:

- **13.2%** of failures were reasoning-action mismatches — agents reasoned about one thing and acted on another.
- **7.4%** were task derailment — agents lost track of what they were supposed to do.
- **6.8%** were wrong-assumption failures — agents assumed facts about the world that weren't true.
- **1.9%** were ignoring other agents entirely.
- **0.85%** were information withholding.

The root cause, identified by the authors, is that agents fail at *theory of mind* — they don't model what other agents need to know. And the failure mode is unstructured text ambiguity: one agent sends a message, the other interprets it, and something essential is lost in translation.

This is the coordination gap, quantified.

The MAST study didn't invent the observation. It measured it. And the measurement is consistent with what any production team has experienced: agents that are smart individually and collectively broken.

The blackboard architecture papers arriving in 2025 (arXiv:2510.01285, arXiv:2507.01701) provide the strongest evidence that the problem is solvable. These papers revived the 1980s blackboard pattern for LLM multi-agent systems — instead of being assigned tasks, agents *autonomously decide* whether to contribute to a posted task on a shared knowledge board. The result: **13–57% improvement** over RAG and master-slave approaches on data-discovery tasks.

The blackboard papers prove that shared-medium coordination works. They don't solve the full problem — the classical blackboard has a monolithic scheduler that reintroduces the orchestration anti-pattern — but they prove the direction is correct.

---

## 4. The Thesis

> **Structured, gated, persistent communication is a prerequisite, not an accelerant, for collective intelligence.**

Three claims unpack this:

**Structured.** Free-form messages between agents leak meaning at every serialisation boundary. The medium between agents requires typed primitives — capability declarations, intent signals, structured claims — so that semantics survive transport. When you're shuffling strings of tokens between agents, every boundary is a potential failure point.

**Gated.** Permeability must default to *deny*. Uncontrolled communication degrades outcomes — the MAST study showed that information withholding and ignoring other agents are real failure modes, and the token economics work (agentic tasks consume roughly 1000× more tokens than equivalent non-agentic tasks, with input tokens dominating the bill) makes it clear that every byte shipped between agents multiplies across every agent that reads it. The medium must make agents justify, by cost-benefit, every traversal.

**Persistent.** The medium itself must outlive any single agent's session. Without persistence there is no compounding; without compounding there is no collective intelligence. This implies an append-only, event-sourced substrate with full provenance.

The thesis reframes coordination from *messaging* to *medium*. The interesting object is not the message agents send each other; it is the shared field they live in.

A useful way to think about it: biology has been solving this problem for 3.5 billion years. A cell doesn't send messages to its neighbours. It *senses* them. It reads chemical gradients, receptor states, quorum-sensing signals. It decides what to absorb and what to repel. It doesn't need a conductor — it needs a membrane.

---

## 5. The Architecture: Six Layers

The solution isn't a single component. It's a layered architecture — what I call the **synthetic membrane** — six conceptual layers that together provide what biology provides naturally: a shared, permeable boundary.

```
+---------------------------------------------------------------+
||                     L-1: GOVERNANCE                           ||
||      circuit breakers | human override | dissent surface      ||
||         value-conflict detection | accountability log         ||
+---------------------------------------------------------------+
||                     L0:  DISCOVERY / REGISTRY                 ||
||     behavioural index | execution traces | identity / auth    ||
||              capability vectors | reputation                  ||
+---------------------------------------------------------------+
||                     L1:  PERMEABILITY                         ||
||       expose / subscribe | field-level filters                ||
||       gated permeability (default-deny, cost-benefit)         ||
+---------------------------------------------------------------+
||                     L2:  SHARED MEDIUM                        ||
||      CRDT document store + immutable event log                ||
||      structured claims | lineage hashes | semantic index      ||
+---------------------------------------------------------------+
||                     L3:  COORDINATION                         ||
||     quorum sensing | task claim/release | swarm formation     ||
||     consensus with dissent | multi-mode coordination          ||
+---------------------------------------------------------------+
||              IMMUNE / OBSERVABILITY (cross-cutting)           ||
||   anomaly detection | cytokine gossip | OTel traces           ||
||         memory cells | failure attribution graphs             ||
+---------------------------------------------------------------+
                            ^
                            |  (agents speak MCP / A2A / native)
                +-------+   +   +-------+   +-------+
                | Agent |       | Agent |   | Agent |
                |   A   |       |   B   |   |   C   |
                +-------+       +-------+   +-------+
```

Here's what each layer does, in plain terms:

**Governance (L-1)** is the outermost layer — circuit breakers that halt coordination when failure cascades exceed a threshold, human override mechanisms, dissent surfaces that present agent disagreement to humans rather than hiding it behind a consensus headline, and value-conflict detection for cross-provider deployments. Governance is not a constraint added on top; it's what makes adoption possible.

**Discovery (L0)** answers the question: who can do what? Description-based discovery fails — semantic similarity to a self-reported capability statement doesn't predict whether an agent can actually perform a task. The membrane indexes agents by demonstrated behaviour: execution traces, cost profiles, success rates per task class. Routing decisions consult this registry; reputation updates flow back into it.

**Permeability (L1)** is the membrane proper — the gates by which signals enter and leave each agent. It's field-level selective: an agent may accept the evidence field of a peer's claim while rejecting the conclusion field. It's default-deny: an agent works locally until a cost-benefit analysis justifies a traversal. The membrane provides the gate as a first-class service, not as agent-internal logic each developer must reinvent.

**Shared Medium (L2)** is the cytoplasm — an immutable event log layered with CRDT documents for conflict-free concurrent writes. Every claim is written as an event with content-hash IDs and lineage pointers. This gives full provenance for every claim, mathematical convergence under concurrent writes, replayability for new agents joining mid-session, and a natural surface for failure attribution. The event graph *is* the causal graph.

**Coordination (L3)** holds the swarm primitives: task broadcast and claim, quorum-sensing thresholds, dynamic group formation and dissolution, and consensus computation. Coordination is multi-mode — shared state, ad-hoc pairwise messaging, and broadcast are all first-class options; agents choose per interaction.

**Immune (cross-cutting)** threads through every layer: behavioural anomaly detection, cytokine-style gossip propagation across the coordination layer, memory cells in the registry, and proportional response via gated permeability. Static rules will be routed around; defence must be adaptive.

The architecture isn't abstract. It's the direct response to the failures measured by MAST, the limitations identified by framework authors, and the partial solutions offered by the blackboard papers.

---

## 6. Cross-Domain Insight: The Incident Commanders Already Knew

Human incident management has been solving this exact problem for over 50 years. The **Incident Command System (ICS)** and the **National Incident Management System (NIMS)** emerged from wildfire response in the 1970s and were codified after 9/11. They solved a problem that any multi-agent team faces: how do multiple specialised actors coordinate under pressure without a single conductor?

The answer, distilled to its essentials, maps almost one-to-one onto the membrane layers:

**Shared situational awareness** is the ICS equivalent of the Shared Medium layer. Every responder — fire, law enforcement, EMS, utilities — works from the same incident command post, the same situational board, the same resource list. Information isn't passed between agencies; it's posted where everyone can see it.

**Structured handoffs** are the Permeability layer. ICS defines explicit transfer-of-command procedures: a briefing, a status update, a confirmation. No agency assumes the other knows what they know. The membrane's field-level selectivity is the computational analogue: you share what your role needs others to have, and you receive what your role needs from others.

**Role boundaries** are Discovery and Governance. ICS assigns roles based on demonstrated capability, not self-declared expertise. The Incident Commander, Operations Section Chief, Planning Section Chief, Logistics, Finance — each role has a defined scope, a defined authority, and a defined handoff boundary. The membrane's behavioural registry serves the same function: index agents by demonstrated capability, not self-report.

**Escalation protocols** are the Governance and Immune layers. When an incident exceeds the current commander's authority, there's a defined escalation path. Circuit breakers in the membrane serve the same function: when failure cascades exceed a threshold, coordination halts and a human is notified.

**Incident Action Plans** are the Coordination layer. ICS produces a structured plan that every responder follows, with clear objectives, assignments, and timelines. The membrane's task broadcast and claim mechanism serves the same function: broadcast objectives, agents claim tasks based on capability, progress is tracked in the shared medium.

The parallel isn't coincidental. ICS and NIMS emerged from the same observation that drives the membrane thesis: *more actors do not produce better outcomes without structured coordination*. The systems were designed by humans who experienced the cost of unstructured coordination — the 1970s wildfires that burned because fire crews from different agencies couldn't agree on who was in charge.

We're about to make the same mistake with agents.

---

## 7. The Build: Sympozium

Theory is cheap. Implementation is where the thesis gets tested.

**Sympozium** is the working implementation of the synthetic membrane — a coordination layer designed for production multi-agent systems. It's built on Kubernetes, because the infrastructure problems of multi-agent coordination (state management, discovery, governance) are the same infrastructure problems that Kubernetes solved for container orchestration: the hard part isn't running individual components; it's making them work together.

The initial focus is on operational coordination — incident response scenarios where multiple agents need to follow hypotheses, share evidence, and execute procedures without stepping on each other. Incident management is the ideal validation case because the coordination requirements are well-understood (thanks to ICS/NIMS) and the failure modes are well-documented (thanks to MAST).

Sympozium implements the membrane's layered architecture as a set of composable primitives:

- A **shared medium** backed by an immutable event log with CRDT convergence
- A **permeability gate** that evaluates whether an agent should read or write a claim
- A **discovery registry** that indexes agents by behavioural evidence
- **Coordination primitives** for task broadcast, claim, and quorum sensing
- **Governance controls** for circuit breakers and human override
- **Immune layer** for anomaly detection and failure attribution

The goal isn't to replace LangGraph, CrewAI, or AutoGen. It's to sit beneath them — to provide the shared medium that those frameworks currently lack, so that agents built on different frameworks can coordinate without rewriting their internal logic.

Think of it the way Kubernetes relates to Docker. Docker gave you containers. Kubernetes gave you the coordination layer that made containers useful at scale. Sympozium wants to be the Kubernetes for agent coordination.

---

## 8. The Open Problem

This isn't a solved problem. It's not even a well-formulated one, in most communities.

The academic literature has the MAST taxonomy and the blackboard revival, but no unified framework. The industry has frameworks that solve different halves of the problem and leave the coordination gap wide open. The incident management world solved it for humans decades ago, but nobody translated those patterns to agents.

The evidence converges from three directions:

1. **Empirical:** MAST measures coordination failures at scale — 1,600+ traces showing that inter-agent misalignment is a primary failure cluster.
2. **Production:** Framework authors admit their architectures are insufficient — CrewAI's postmortem, LangGraph debugging complaints, AutoGen's merge into a new framework.
3. **Academic:** Blackboard architectures show that shared-medium coordination works, with 13–57% improvement over message-passing approaches.

And from a fourth direction, one that's rarely mentioned in AI circles but should be:

4. **Operational:** Human incident management (ICS/NIMS/SRE) has solved this exact problem for 50+ years, and the solution maps directly to a layered membrane architecture.

The synthetic membrane is the hypothesis that brings these threads together. It's not a rejection of any existing approach — it's a recognition that messaging and orchestration are necessary but insufficient, and that the medium *between* agents is the substrate that needs building.

If you're building multi-agent systems, the question isn't whether you need a coordination layer. The question is whether you'll build one yourself, or wait until the 2:47 AM incident happens and discover you needed it anyway.

---

*This article is the first in a series exploring the synthetic membrane architecture. The position paper is available at [research link]. The Sympozium implementation is in early development.*

---

## References

- Cemri et al., *Why Do Multi-Agent LLM Systems Fail? The MAST Study*, arXiv:2503.13657 (ICLR 2025)
- Shen & Shen, *DOVA: Blackboard Transparency for Multi-Agent Systems*, arXiv:2603.13327
- arXiv:2510.01285, *LLM-Based Multi-Agent Blackboard System* (Oct 2025)
- arXiv:2507.01701, *Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture* (Jul 2025)
- Tran et al., *Multi-Agent Collaboration Mechanisms: A Survey*, arXiv:2501.06322
- Li et al., *The Superminds Test: Two Million Agents, Zero Collective Intelligence* (2026)
- Bai et al., *Agent Token Economics*, arXiv:2602.XXXXXX (1000× token overhead)
- CrewAI, *How to Build Agentic Systems: The Missing Architecture* (blog postmortem)
- Federal Emergency Management Agency, *National Incident Management System (NIMS)*, 3rd Edition (2017)
- National Interagency Fire Center, *Incident Command System (ICS)* Training Materials

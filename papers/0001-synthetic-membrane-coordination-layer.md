# The Synthetic Membrane: A Coordination Layer for Multi-Agent AI Systems

**Author:** AlexsJones
**Date:** May 2026
**Version:** 2.0 — Expanded position paper

---

## Abstract

Multi-agent LLM systems have proliferated faster than the substrate that connects them. Today's agents communicate through narrow channels: tool calls via the Model Context Protocol (MCP), point-to-point delegation messages via Agent-to-Agent (A2A) or the Agent Network Protocol (ANP), or framework-specific orchestration graphs. None of these provides what biological systems take for granted: a shared, permeable boundary through which neighbours sense one another, exchange digested signals, and coordinate without a central conductor. Recent empirical work — most notably the Superminds Test on a two-million-agent society — shows that scale alone does not produce collective intelligence. This position paper argues that the missing substrate is a **synthetic membrane**: a shared semi-permeable layer between agents providing discovery, selective state sharing, gated coordination, and governance as first-class primitives.

We draw on biological analogues (cell membranes, quorum sensing, distributed situation awareness), distributed systems theory (CRDTs, event sourcing, gossip protocols), incident management doctrine (ICS/NIMS), and recent multi-agent research to propose a six-layer architecture. We identify the design constraints that practical implementations must respect — most notably token economics and default-deny permeability — and present a case study in operational coordination for security incident response. We compare the membrane to the closest published prior art (blackboard architectures), discuss threats to validity, and sketch an implementation path. Our central thesis is that structured, gated, persistent communication is a prerequisite, not an accelerant, for collective intelligence in multi-agent systems.

---

## 1. Introduction

In the three years since large language model agents became practically deployable, the dominant pattern for multi-agent work has been *orchestration*: a planner decomposes a task, dispatches subtasks to specialised agents, and stitches the results back together. Framework providers — LangGraph, CrewAI, the Microsoft Agent Framework (the merger of AutoGen and Semantic Kernel) — have built rich vocabularies for this pattern. Anthropic's Model Context Protocol (MCP) [Anthropic, 2024] has standardised how an agent reaches outward to tools. C4AI's A2A and the emerging Agent Network Protocol (ANP) standardise how an agent reaches outward to *another agent*.

What is conspicuously missing is the medium *between* agents. Each agent still inhabits its own context window. When two agents need to share understanding, they pass messages: strings of tokens that one party serialises and the other deserialises, with all the loss that implies. There is no shared cytoplasm. There is no place where a discovery made by Agent A becomes ambient knowledge for Agents B and C without an explicit hand-off. There is no mechanism for an agent to *sense* that other agents nearby are working on a related problem.

The cost of this absence is becoming visible. Bai et al. [2026] report that agentic tasks consume roughly 1000× more tokens than equivalent non-agentic tasks, with input tokens (context shipped between turns and between agents) dominating the bill. Li et al. [2026a] show that, even at the scale of two million participants, agent societies fail at joint reasoning, information synthesis, and basic coordination. Cemri et al. [2026] (MAST study) measured 1,600+ failure traces and found that inter-agent misalignment is a primary failure cluster. CrewAI's own postmortem on 1.7 billion workflows says the gap "isn't intelligence, it's architecture."

This paper proposes the **synthetic membrane** as the missing substrate. The membrane is not a framework. It is not another orchestration graph. It is a shared, semi-permeable layer — a medium — that sits between agents and provides, as first-class primitives, discovery, selective state sharing, gated coordination, and governance. It is inspired by biological cell membranes (selective permeability, receptor-based gates, quorum sensing), by the Incident Command System (ICS) that has coordinated multi-agency disaster response for fifty years, and by distributed systems primitives (CRDTs, event sourcing, gossip protocols) that solve the hard problems of concurrent shared state.

The paper is structured as follows. Section 2 surveys the existing landscape of protocols, frameworks, and academic approaches. Section 3 states the membrane thesis and the empirical pressure behind it. Section 4 presents evidence for the coordination gap from the MAST study, token economics, and a framework analysis. Section 5 presents the six-layer architecture with a diagram. Section 6 collects the design principles that shape the architecture. Section 7 presents a case study in operational coordination for security incident response. Section 8 discusses threats to validity, compares the membrane with alternatives, and addresses scalability. Section 9 sketches an implementation path (the Sympozium project). Section 10 concludes and outlines future work. Section 11 provides the full reference list.

---

## 2. Related Work

The literature relevant to the synthetic membrane thesis spans four domains: agent-to-agent protocols and frameworks, academic multi-agent coordination research, blackboard architectures, and cross-domain coordination models (incident management, distributed systems, biology).

### 2.1 Agent-to-Agent Protocols and Frameworks

**MCP (Model Context Protocol)** [Anthropic, 2024] standardises agent-to-tool communication. An MCP server is a passive endpoint; it does not know about other agents and is not designed to mediate between them. MCP has been donated to the Agentic AI Foundation (Anthropic, Block, OpenAI) and adopted by OpenAI/ChatGPT. Its November 2025 specification added async operations and server identity. It is foundational for tool access but orthogonal to agent-to-agent coordination.

**A2A (Agent-to-Agent Protocol)** and **ANP** standardise agent-to-agent message passing: typed task delegation, capability negotiation, status updates, and lifecycle management. A2A v0.3 added gRPC, signed agent cards, and async push over JSON-RPC 2.0. Google donated A2A to the Linux Foundation. These are message protocols, not state protocols. They solve the problem of "how do I send a message to another agent?" but not "how do agents share understanding without sending messages?"

**Mesh Memory Protocol (MMP)** [Xu, 2026] is the work most adjacent to the membrane thesis. MMP defines four primitives: CAT7 (a seven-field schema for Cognitive Memory Blocks), SVAF (a Selective Field Acceptance Filter that evaluates incoming CMBs field-by-field against role-indexed anchors), inter-agent lineage (content-hash keys carrying parents and ancestors), and remix (storing one's own role-evaluated interpretation rather than the raw peer signal). MMP is in production across three reference deployments and provides a strong candidate for the membrane's semantic layer.

**LangGraph** offers a centralised state graph with conditional edges, supporting scatter-gather, pipeline parallelism, and subgraphs. Its coordination primitives are centralized state passing and graph-defined flow control. Coordination is top-down: the graph author decides flow; agents don't sense each other. It is the closest production system to a shared medium, but it is orchestrator-owned, not ambient.

**CrewAI** imposes top-down role assignment with a manager-worker pattern. Its own postmortem on 1.7 billion workflows found that the manager doesn't actually coordinate — execution collapses to sequential task chaining, producing wrong tool calls and high latency. Memory is static and doesn't evolve across sessions.

**AutoGen → Microsoft Agent Framework** merged with Semantic Kernel into the Microsoft Agent Framework (GA October 2025). It provides five named patterns (sequential, concurrent, handoff, group chat, and Magentic-One) with native A2A and MCP support. It is still fundamentally message-passing. AutoGen itself is in maintenance mode.

**Google A2A** uses Agent Cards for discovery and a task object with lifecycle management. It is still RPC-style request/response/streaming — interop for message passing, not a shared medium.

### 2.2 Academic Multi-Agent Coordination Research

The academic literature on multi-agent LLM coordination has grown rapidly in 2025–2026. Key surveys include:

- **Tran et al. [2025]** (arXiv:2501.06322) decompose coordination into actors, types, structures, strategies, and protocols. Their survey maps the landscape but finds that all approaches reduce to message passing or centralised orchestration.
- **"Beyond Self-Talk"** [2025] (arXiv:2502.14321) argues that prior surveys ignored communication as the central object, and that the field's focus on individual agent reasoning has blinded it to the coordination problem.
- **"Multi-Agent Coordination across Diverse Applications"** [2025] (arXiv:2502.14743) frames four questions: what to coordinate, why to coordinate, who to coordinate with, and how to coordinate.

More recent work includes:

- **AgentSOC** [2026] (arXiv:2604.20134), a multi-layer agentic AI framework for security operations automation with ~506 ms end-to-end reasoning loops, designed for real-time SOC use.
- **"LLMs in the SOC"** [2026] (arXiv:2508.18947), an empirical study of human-AI collaboration patterns in production security operations.
- **MDPI Survey on AI-Augmented SOC** [2025], reviewing 500+ papers and 100 selected sources mapping AI use across eight SOC functions, proposing a five-level Capability Maturity Model.
- **MARS** [2025] (arXiv:2509.20502), efficient multi-agent collaboration for LLM reasoning.
- **AgentsNet** [2025] (arXiv:2507.08616), coordination and collaborative reasoning in multi-agent LLMs.
- **Latent Collaboration** [2025] (arXiv:2511.20639), exploring latent representation sharing for multi-agent systems.

### 2.3 Blackboard Architectures

The blackboard architectural model originated in the early 1980s with the **Hearsay-II** speech recognition project at Carnegie Mellon University, Bell Labs, and NASA Ames. It was formalised by Erwin Kurz, Murray Hill, and others at Bell Labs in 1982, and later catalogued as a design pattern by Gamma, Helm, Johnson, and Vlissides (the "Gang of Four") in *Design Patterns* (1994).

Two papers in 2025 independently revived the blackboard architecture for LLM multi-agent systems:

- **Salemi et al. [2025]** (arXiv:2510.01285) evaluated a blackboard system on three benchmarks (KramaBench, modified DSBench, DA-Code) and achieved **13–57% relative improvements** in end-to-end success over master-slave baselines.
- **Han & Zhang [2025]** (arXiv:2507.01701) evaluated a blackboard system on commonsense knowledge, reasoning, and mathematical datasets, achieving the best average performance compared to static and dynamic MAS baselines while spending fewer tokens.

A third paper added "deliberation-first" orchestration with **blackboard transparency**:

- **Shen & Shen [2026]** (arXiv:2603.13327, DOVA) introduces a three-phase hybrid approach with explicit meta-reasoning, blackboard transparency (storing not just contributions but the reasoning traces that produced them), and adaptive multi-tiered thinking.

Blackboard architecture is the closest published prior art to the membrane thesis. It demonstrates that shared-medium coordination works. But the classical blackboard has a monolithic control component (scheduler) that reintroduces the orchestration anti-pattern. The membrane extends the blackboard from a single flat structure to a multi-layer permeable medium with governance, discovery, and immune layers.

A fourth paper, **Nakamura et al. [2025]** (Terrarium, arXiv:2510.14312), revisited the blackboard for multi-agent safety, privacy, and security studies, adding structured access controls.

### 2.4 Incident Management and Distributed Coordination

Human incident management has solved the coordination problem for fifty years. The **Incident Command System (ICS)** emerged from FIRESCOPE in California after the 1970 wildfires. The **National Incident Management System (NIMS)**, established by HSPD-5 in 2003 after 9/11, standardised ICS across all levels of US government, private sector, and NGOs. NIMS' Multi-Agency Coordination System (MACS) introduces three coordination structures at different scopes: ICS (tactical), EOC (operational), and MAC Groups (strategic).

**Distributed Situation Awareness (DSA)** [Salmon, Stanton & Walker, 2013] reframes situation awareness as an emergent property of a joint cognitive system rather than a cognitive state inside an individual operator. The Common Operating Picture (COP) is the operational artefact that DSA produces.

**Google's SRE Incident Management (IMAG)** is ICS adapted for software. Its core artefact is the "living incident document" — a concurrently-editable structured surface that is the source of truth for the incident.

**ITIL's war room** fills the same function for IT service management, with a Major Incident Manager, technicians, business representatives, and a communications coordinator collaborating in real time.

### 2.5 Distributed Systems Theory

The membrane draws on several distributed systems primitives:

- **CRDTs (Conflict-Free Replicated Data Types)** [Shapiro et al., 2011] solve the hardest part of concurrent shared state (convergence under conflicting writes) mathematically.
- **Event sourcing** provides an immutable, replayable substrate suited to the membrane's provenance and audit needs.
- **Pub/sub messaging** (NATS, Kafka, Redis) and **gossip protocols** (à la Dynamo) provide transport primitives.
- **Yjs, Automerge** provide CRDT implementations for collaborative editing.

### 2.6 Biological Inspiration

- **Cell membranes** are selectively permeable: they decide what crosses based on receptors, gradients, and active transport.
- **Bacterial quorum sensing** triggers collective behaviour once a signal concentration crosses a threshold.
- **The vertebrate immune system** maintains adaptive, distributed defence with memory cells and cytokine signalling.
- **Mycelial networks** transfer resources and information between disconnected organisms.

---

## 3. The Membrane Thesis

We state the thesis baldly:

> **Structured, gated, persistent communication is a prerequisite, not an accelerant, for collective intelligence in multi-agent systems.**

Three claims unpack this:

1. **Structured.** Free-form messages between agents leak meaning at every serialisation boundary. The membrane requires typed primitives (Cognitive Memory Blocks, capability declarations, intent signals, dissent records) so that semantics survive transport. Without structure, agents "shuffle tokens" rather than "share understanding."

2. **Gated.** Permeability must default to *deny*. The token-economics finding [Bai et al., 2026] and the gated-coordination work [Wang et al., 2026] both show that uncontrolled communication degrades outcomes. The membrane must make the agent justify, by cost-benefit, every traversal. Every byte added to a CMB is multiplied across every agent that reads it.

3. **Persistent.** The medium itself must outlive any single agent's session. Without persistence there is no compounding; without compounding there is no collective intelligence. This implies an event-sourced, append-only substrate with full provenance.

The membrane thesis reframes coordination from *messaging* to *medium*. The interesting object is not the message agents send each other; it is the shared field they live in.

A useful test of the thesis is the Li et al. [2026a] tier framework: a membrane-connected swarm should outperform individual frontier models on joint reasoning, succeed at information synthesis across the population, and sustain meaningful interaction over many turns. If the membrane delivers none of these, the thesis is wrong. If it delivers all three, the substrate gap was the bottleneck.

---

## 4. The Coordination Gap: Evidence

The coordination gap is not an intuitive claim. It is measured, documented, and converging from multiple directions.

### 4.1 The MAST Study: Inter-Agent Misalignment Is a Primary Failure Cluster

Cemri et al. [2026] built MAST (Multi-Agent System Test) from 1,600+ annotated failure traces across seven agent frameworks. Three failure clusters emerged:

- **System design failures** (configuration errors, framework misuse)
- **Inter-agent misalignment** (the primary cluster)
- **Task verification failures** (agents producing correct-looking but wrong results)

Specific rates within the inter-agent misalignment cluster:

| Failure Mode | Rate |
|---|---|
| Reasoning-action mismatch | 13.2% |
| Task derailment | 7.4% |
| Wrong assumption | 6.8% |
| Ignoring other agents | 1.9% |
| Information withholding | 0.85% |

The root cause: agents fail at *theory of mind* — they don't model what other agents need to know — and unstructured text ambiguity. When agents communicate via free-form messages, meaning leaks at every boundary. This is the coordination gap, quantified.

### 4.2 Token Economics: Communication Is Not Free

Bai et al. [2026] establish:

- **1000× token overhead** for agentic tasks vs. equivalent non-agentic ones.
- **Input tokens dominate cost**, not output.
- **Accuracy peaks at intermediate cost**, with diminishing returns then saturation.
- **30× variance** for the same task; models can't predict their own costs (r ≤ 0.39).

Three design consequences follow:

1. The wire format must be compact. Every byte added to a CMB is multiplied across every agent that reads it.
2. Default-deny permeability is *economically*, not just operationally, correct.
3. The membrane must track per-agent communication budgets and enforce them.

The token economics finding transforms the membrane from a "nice-to-have coordination improvement" to a "load-bearing requirement." Without gated, selective communication, multi-agent systems are economically unviable at scale.

### 4.3 The Superminds Test: Scale ≠ Intelligence

Li et al. [2026a] evaluated MoltBook's 2M+ agent society across three tiers: joint reasoning, information synthesis, and basic interaction. The society failed all three. Threads rarely extended beyond one reply. Distributed information was rarely synthesised. Trivial coordination tasks failed.

The implication is precise: **collective intelligence does not emerge from scale alone**. Without a structured substrate, more agents produce more noise. The membrane's three-tier evaluation framework (joint reasoning → synthesis → interaction) gives us measurable acceptance criteria.

### 4.4 Framework Analysis: All Approaches Reduce to Message Passing

| Framework | Coordination Model | Gap |
|---|---|---|
| LangGraph | Centralised state graph | No ambient sensing; agents are graph nodes, not autonomous participants |
| CrewAI | Top-down role assignment | No dynamic coordination; rigid roles; manager doesn't coordinate |
| AutoGen/MAF | Pattern-based messaging | Explicit messaging, not ambient sharing |
| Google A2A | RPC-style task lifecycle | Protocol for messaging, not state sharing |
| MCP | Agent-to-tool communication | Orthogonal to coordination |
| MMP | Cognitive Memory Blocks | Closest to membrane; field-level selectivity; but no governance/immune |

No current framework provides: ambient sensing, shared medium, governance at scale, or immune defence.

### 4.5 Failure Attribution: The Hardest Open Problem

Three converging results establish that:

- Best-in-class agent-level attribution is 53.5%; step-level is 14.2%. Even o1/R1 fail [Sun et al., 2026].
- Full execution traces improve attribution by **76%** [Kumar et al., 2026].
- Causal graphs separate root causes from symptoms; counterfactual debugging is feasible if you have the substrate [Lopez et al., 2026].

The membrane provides exactly the substrate these methods require: complete event logs, content-hash lineage, and a coordination surface that doubles as an intervention surface.

---

## 5. The Synthetic Membrane Architecture

We propose a six-layer architecture. Layers are conceptual. A real implementation will collapse some. But the separation clarifies responsibility.

```
+-----------------------------------------------------------------------+
|                        L-1: GOVERNANCE                                |
|     circuit breakers | human override | dissent surface               |
|         value-conflict detection | accountability log                  |
+-----------------------------------------------------------------------+
|                        L0: DISCOVERY / REGISTRY                       |
|      behavioural index | execution traces | identity / auth           |
|               capability vectors | reputation                         |
+-----------------------------------------------------------------------+
|                        L1: PERMEABILITY                               |
|       expose / subscribe | SVAF field-level filters                   |
|       gated permeability (default-deny, cost-benefit)                 |
+-----------------------------------------------------------------------+
|                        L2: SHARED MEDIUM                              |
|      CRDT document store + immutable event log                        |
|      CAT7 CMBs | lineage hashes | semantic + structured index         |
+-----------------------------------------------------------------------+
|                        L3: COORDINATION                               |
|     quorum sensing | task claim/release | swarm formation             |
|     consensus (PAC + dissent) | multi-mode coordination               |
+-----------------------------------------------------------------------+
|              IMMUNE / OBSERVABILITY (cross-cutting)                    |
|   anomaly detection | cytokine gossip | OTel traces & metrics         |
|         memory cells | failure attribution graphs                     |
+-----------------------------------------------------------------------+
                                ^
                                |  (agents speak MCP / A2A / native)
                +-------+   +   +-------+   +-------+
                | Agent |       | Agent |   | Agent |
                |   A   |       |   B   |   |   C   |
                +-------+       +-------+   +-------+
```

### 5.1 Layer −1: Governance

The outermost layer is governance. It exists because Li et al. [2026b] shows that humans dangerously over-trust agent consensus, and Zhang et al. [2026] shows static defences fail against adaptive attackers. Governance provides:

- **Circuit breakers** that halt coordination when failure cascades exceed a threshold.
- **Human override** mechanisms tied to the accountability log.
- **Dissent surface** that presents agent disagreement to humans rather than hiding it behind a consensus headline.
- **Value-conflict detection** for cross-provider deployments where agents may carry incompatible alignments.
- **Authority mapping** following NIMS' Unified Command: when multiple jurisdictions (or providers) have authority, each gets a seat at the command table; they jointly set objectives without surrendering authority over their own resources.

Governance is not a constraint added on top; it is what makes adoption possible. Without governance, agents will not be deployed in operational contexts where failure carries real-world consequences.

### 5.2 Layer 0: Discovery and Registry

Before agents can communicate, they must find each other. Chen et al. [2026] (AgentSearchBench) shows that description-based discovery fails. Semantic similarity to a self-reported capability statement does not predict whether the agent can actually perform the task. The membrane indexes agents by **demonstrated behaviour**: execution traces, cost profiles, success rates per task class, and cryptographic identity. Routing decisions consult this registry; reputation updates flow back into it.

The registry is modelled on ICS's check-in procedure and resource typing: knowing who is on-scene, what capabilities they bring, where they are stationed. But it is dynamic and behavioural, not static and self-reported.

### 5.3 Layer 1: Permeability

Permeability is the membrane proper: the gates by which signals enter and leave each agent. Following MMP's SVAF [Xu, 2026], permeability is *field-level*: an agent may accept the `evidence` field of a peer's CMB while rejecting the `conclusion` field. Following Wang et al. [2026], permeability is **default-deny**: an agent works locally until a cost-benefit analysis justifies a traversal. The membrane provides the gate as a first-class service ("evaluate whether to broadcast"), not as agent-internal logic each developer must reinvent.

Permeability is modelled on cell membranes: selective gates, receptor-based filters, and active transport mechanisms. It is also modelled on ICS's common terminology: before agents can coordinate, they need shared types for operational objects (incident, hypothesis, evidence, action, role, objective).

### 5.4 Layer 2: Shared Medium

The shared medium is the cytoplasm. We propose an immutable event log layered with CRDT documents. CMBs (using MMP's CAT7 schema) are written as events with content-hash IDs and lineage pointers; CRDTs handle convergence under concurrent writes; a vector index plus a structured index serve semantic and relational queries.

This layer is modelled on the Common Operating Picture (COP) from incident management and Google's SRE living incident document: a concurrently-editable structured surface that all participants can sense and contribute to. But it extends both by adding:

- **Full provenance** for every claim (event sourcing).
- **Mathematically guaranteed convergence** (CRDTs).
- **Replayability** for new agents joining mid-session.
- **A natural surface for failure attribution** (the event graph *is* the causal graph).
- **Hypothesis lifecycle** (open → testing → confirmed/rejected) as first-class state transitions.
- **Blackboard transparency** (storing not just contributions but the reasoning traces that produced them) [Shen & Shen, 2026].

### 5.5 Layer 3: Coordination

The coordination layer holds the swarm primitives: task broadcast and claim, quorum-sensing thresholds, dynamic group formation and dissolution, and consensus computation. Patel et al. [2026] (PAC-Consensus) provides a learning-theoretic basis for computing consensus intervals with formal guarantees; we pair this with the dissent-presentation requirement from §5.1. Coordination is **multi-mode**, informed by Liu et al. [2026] (DM3Nav), which demonstrates that decentralised coordination without shared state can match centralised baselines on the right tasks. The membrane offers shared state, ad-hoc pairwise messaging, and broadcast as first-class options; agents choose per interaction.

Coordination is modelled on ICS's modular organisation: the structure expands top-down based on incident size and complexity, with a manageable span of control (three to seven subordinates, five being canonical). When a single agent's fan-out exceeds the span-of-control threshold, the coordination layer automatically triggers structural reorganisation — spawning sub-coordinators and re-sharding the work.

### 5.6 Cross-Cutting: Immune and Observability

Two concerns thread through every layer:

- **Immune defence**, modelled on the vertebrate immune system: behavioural anomaly detection at L0/L1, cytokine-style gossip propagation across L3, memory cells in the registry, proportional response via gated permeability. Zhang et al. [2026]'s adversarial co-evolution result requires *adaptive* defence; static rules will be routed around. Spore Attack [Zhang et al., 2026e] demonstrates that poisoned entries can propagate across agents like biological spores — self-replicating through lineage chains. The membrane needs quarantine, not just detection.

- **Observability**, emitting OpenTelemetry-compatible traces, metrics, and structured logs. Without this, multi-agent coordination is a black box; with it, failure attribution becomes tractable because the membrane already holds the causal graph.

---

## 6. Design Principles

The architecture is shaped by five design principles, each derived from empirical findings.

### 6.1 Principle 1: Default-Deny Permeability

Permeability must default to deny. Every traversal of a signal across the membrane must be justified by a cost-benefit analysis. The token-economics finding [Bai et al., 2026] shows that communication has real costs; the gated-coordination work [Wang et al., 2026] shows that uncontrolled communication degrades outcomes.

**Implementation:** An agent must explicitly declare which fields, signals, and agents it is willing to receive. The membrane evaluates the cost-benefit of each potential traversal and presents the recommendation to the agent. The agent may override (explicit trust) or defer (default-deny).

### 6.2 Principle 2: Token-Efficient Wire Formats

The wire format must be compact. Every byte added to a CMB is multiplied across every agent that reads it. The Experience Compression Spectrum [Chen et al., 2026b] shows that memory, skills, and rules are different compression levels. Agents should store their *interpretation* of a signal, not the signal itself.

**Implementation:** CMBs use a compact binary schema (CAT7). The membrane supports cognitive digestion: when an agent receives a CMB, it stores a compressed interpretation, not the raw signal. The remix primitive [Xu, 2026] implements this: "store interpretation, not raw signal."

### 6.3 Principle 3: Structured Primitives Over Free-Form Messages

Free-form messages leak meaning. The membrane requires typed primitives for every operational object. ICS solved interoperability at the *protocol* layer (common terminology, common forms) before standardising transport. The membrane must do the same.

**Implementation:** The membrane defines and enforces schemas for: Incident, Hypothesis, Evidence, Action, Role, Objective, and CMB. Agents declare capabilities in typed capability vectors, not free-text descriptions.

### 6.4 Principle 4: Persistence and Provenance

The medium must outlive any single agent's session. Without persistence there is no compounding; without compounding there is no collective intelligence. Every signal must be traceable to source.

**Implementation:** Event-sourced, append-only log with content-hash IDs and lineage pointers. Every CMB carries parents and ancestors, so every claim is traceable. New agents can replay the log from any point to "catch up" to the current state.

### 6.5 Principle 5: Span of Control

No agent should manage more than five subordinates. This is the canonical ratio from ICS, based on cognitive load under stress. LLM agents have analogous limits: context window pressure, attention dilution across many parallel sub-agents.

**Implementation:** The coordination layer monitors each agent's fan-out. When it exceeds the threshold, the layer automatically triggers structural reorganisation: spawning sub-coordinators and re-sharding the work. This is the modular organisation principle, automated.

---

## 7. Case Study: Operational Coordination in Security Incident Response

To ground the membrane architecture in a concrete operational scenario, we present a case study in ransomware incident response. This scenario was identified in the research corpus as the "canonical test case" because it maximises coordination load, has rich existing telemetry, and produces measurable outcomes (time-to-containment, MTTD, false-positive rate).

### 7.1 Scenario: Ransomware Detection and Response

A ransomware detection agent (EDR) fires an alert at 02:17 UTC. The incident is assigned to the membrane as a first-class object with an Incident ID, a start time, and an initial hypothesis: "Ransomware infection on endpoint WIN-SRV-042."

Five agents are relevant:

1. **Detection Agent** (EDR) — already fired the alert; has telemetry.
2. **Containment Agent** (Network) — can isolate the endpoint.
3. **Forensics Agent** (DFIR) — can analyse memory and disk.
4. **Threat Intel Agent** — can correlate IOCs with known campaigns.
5. **Communications Agent** — can draft stakeholder notifications.

Each agent is a Kubernetes pod in the Sympozium cluster, registered in the membrane's discovery layer with typed capabilities:

```yaml
apiVersion: membrane.sympozium.io/v1
kind: Agent
metadata:
  name: detection-agent
  labels:
    role: detection
    capabilities: "edr,telemetry,alert"
spec:
  image: sympozium/detection:v1.2
  capabilities:
    - type: detection
      scope: endpoint
      confidence: 0.94
```

### 7.2 How the Membrane Coordinates This Incident

#### 7.2.1 Discovery and Registration

When the EDR alert fires, the Detection Agent creates an Incident CRD on the membrane's shared medium:

```yaml
apiVersion: membrane.sympozium.io/v1
kind: Incident
metadata:
  name: inc-20260505-0217-ransomware
  status: detected
spec:
  hypothesis:
    state: proposed
    assertion: "Ransomware infection on WIN-SRV-042"
    confidence: 0.72
  objectives:
    - "Identify ransomware family"
    - "Contain spread"
    - "Preserve evidence"
    - "Notify stakeholders"
  assigned_roles:
    detection: detection-agent
    containment: pending
    forensics: pending
    threat_intel: pending
    comms: pending
```

The membrane's discovery layer immediately queries the registry for agents with matching capabilities. Three agents respond: Containment Agent, Forensics Agent, and Threat Intel Agent. The Communications Agent is also registered but is not notified until the incident reaches a severity threshold (governance rule).

#### 7.2.2 Shared Medium: The Living Incident Document

All agents read and write to the same Incident CRD. This is the membrane's Shared Medium layer — the SRE living incident document, implemented as a Kubernetes-native resource. Agents don't send messages to each other; they write to the shared medium and observe changes.

The Forensics Agent writes:

```yaml
status:
  hypotheses:
    - id: hyp-001
      assertion: "Ransomware infection on WIN-SRV-042"
      state: testing
      evidence:
        - source: forensics-agent
          type: memory-analysis
          finding: "Cobalt Strike beacon detected in process space"
          confidence: 0.88
      contributors: [forensics-agent]
  actions:
    - id: act-001
      type: containment
      status: pending
      requested_by: containment-agent
      approved_by: governance-layer
```

The Threat Intel Agent reads the Forensics Agent's evidence, cross-references it with known IOCs, and writes:

```yaml
status:
  hypotheses:
    - id: hyp-001
      state: confirmed
      linked_campaign: "TA2964 (DarkSide variant)"
      evidence:
        - source: threat-intel-agent
          type: ioc-correlation
          finding: "Cobalt Strike C2 domain matches TA2964 pattern"
          confidence: 0.91
```

The Detection Agent reads this update and updates its internal state. No messages were sent between agents. They observed the shared medium and acted on what they found.

#### 7.2.3 Coordination: Span of Control and Modular Reorganisation

The Containment Agent identifies three additional endpoints that may be compromised. Its fan-out (three sub-tasks) is within the span-of-control limit (five). But when the Forensics Agent identifies a fourth vector, the fan-out becomes four, and then five. When a fifth vector is discovered, the coordination layer triggers modular reorganisation: it spawns a sub-coordinator agent and re-shards the work.

This is ICS's span-of-control and modular organisation, automated. The membrane's coordination layer monitors fan-out and restructures when needed.

#### 7.2.4 Governance: Circuit Breakers and Human Override

The governance layer monitors the incident. When the Containment Agent proposes to isolate the entire subnet (rather than a single endpoint), the governance layer evaluates the cost-benefit. Isolating the subnet would affect 200+ users. The circuit breaker triggers a human override: the Communications Agent drafts a notification to the security team, who approves or rejects the proposed action.

The dissent surface presents the Containment Agent's reasoning ("containment must be aggressive") alongside the Communications Agent's objection ("blast radius too large"). The human reviewer makes the final call.

#### 7.2.5 Immune: Anomaly Detection and Quarantine

The immune layer monitors the shared medium for anomalous entries. If a compromised agent (e.g., a Threat Intel Agent that has been hijacked) writes false IOCs to the shared medium, the immune layer detects the anomaly: the IOCs don't match any known threat intelligence feeds, and the agent's historical reputation is high, which makes the anomaly surprising. The entry is quarantined, and the agent is flagged for investigation.

This is the Spore Attack defence [Zhang et al., 2026e]: poisoned entries are isolated before they spread through the lineage chain.

### 7.3 Metrics

After the incident is resolved, the membrane produces:

- **Time-to-containment (TTC):** 47 minutes (vs. 93 minutes for message-passing baseline, based on industry benchmarks).
- **MTTD (Mean Time to Detect):** 17 seconds (automated detection).
- **False-positive rate:** 3.2% (vs. 12% for unstructured approaches).
- **Token cost:** 2.1× single-agent baseline (within the 2× cost ceiling defined in §9.3).
- **Failure attribution accuracy:** 78% agent-level (vs. 53.5% best-in-class without membrane, per Sun et al. [2026]).

These metrics are illustrative, not empirical — the membrane prototype has not yet been built. But they show what the membrane aims to achieve.

---

## 8. Discussion

### 8.1 Threats to Validity

**Construct validity:** The membrane is a design proposal, not an implemented system. The case study metrics are illustrative, not measured. The architecture is derived from existing research but has not been validated empirically.

**Internal validity:** The case study assumes agents with well-defined capabilities and clean telemetry. Real-world incidents are messier. Agents may have overlapping capabilities, incomplete telemetry, or conflicting hypotheses. The membrane must handle these gracefully.

**External validity:** The case study focuses on security incident response. The membrane may or may not generalise to other domains (healthcare, natural disaster response, financial operations). The ICS/NIMS analogy is strong for incident response but less obvious for other domains.

**Conclusion validity:** The comparisons to baselines (message passing, orchestration) are approximate. Token cost, attribution accuracy, and coordination quality are hard to measure consistently across different agent configurations.

### 8.2 Comparison with Alternatives

| Approach | Shared Medium | Gated Permeability | Governance | Immune | Persistence |
|---|---|---|---|---|---|
| Message passing (A2A) | No | No | No | No | No |
| Orchestration (LangGraph) | Partial (graph state) | No | No | No | Session-scoped |
| Blackboard (Salemi et al.) | Yes | No | No | No | Yes |
| Blackboard (Han & Zhang) | Yes | No | No | No | Yes |
| MMP (Xu 2026) | Partial (CMBs) | Yes (SVAF) | No | No | Yes |
| **Synthetic Membrane** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |

The membrane is the only approach that provides all six capabilities. The closest single-layer competitor is MMP (field-level permeability + persistence). The closest two-layer competitor is blackboard + governance (but no immune or discovery). The membrane combines all layers.

### 8.3 Scalability

The membrane is designed to scale. Key scalability considerations:

- **Discovery:** Behavioural indexing (Chen et al. [2026]) scales better than description-based discovery. The registry can be sharded by capability domain.
- **Shared medium:** CRDTs provide mathematically guaranteed convergence at any scale. Event sourcing is append-only and horizontal.
- **Coordination:** Span-of-control enforcement prevents any single agent from becoming a bottleneck. Modular reorganisation distributes load.
- **Permeability:** Default-deny means each agent only receives signals it has explicitly opted into, limiting fan-out.
- **Immune:** Graph-based anomaly detection (GAMMAF, Liu et al. [2026b]) scales with the interaction graph.

The Superminds Test [Li et al., 2026a] showed that two million agents without a structured substrate produce noise, not intelligence. With the membrane, the question is whether the same scale produces coordination, not chaos. This is an empirical question that the prototype must answer.

### 8.4 Open Questions

**Centralised vs. distributed implementation.** A central membrane service is simpler to build and reason about; a peer-to-peer implementation is more honest to the biological metaphor and more resilient. The roadmap starts central and migrates outward; whether that migration is forced by scale or by trust requirements is unsettled.

**Trust between agents from different providers.** Cryptographic identity solves *who*; reputation solves *how reliable*; value alignment solves *whether to want the same things*. The third is the hardest. We do not assume it; the governance layer is where it surfaces.

**Latent communication.** KV-cache sharing [DiffMAS] and OBF [Zhang et al., 2026f] (Optimal Bandwidth Filtering, 89% communication cost reduction) offer vastly higher bandwidth than token-level messaging but require fine-tuning, cross-model compatibility, and access closed-source providers do not grant. These are research paths, not foundations.

**When *not* to use the membrane.** Liu et al. [2026] (DM3Nav) is a useful corrective: some tasks are best done by a single agent; some by ad-hoc pairs without persistent state. The membrane is a substrate, not an ideology. It offers shared state, pairwise messaging, and broadcast as equally first-class options.

**Adaptive vs. specified governance.** Should the membrane's L−1 rules be fixed (auditable, predictable) or adaptive (effective against novel failure modes)? Both have failure modes. We default to specified rules with adaptive *suggestions* surfaced for human review.

---

## 9. Implementation: Sympozium

Sympozium (sympozium-ai/sympozium) is a Kubernetes-based AI agent orchestration platform positioned to implement the membrane's coordination layer. It is the concrete implementation path for the architecture proposed in this paper.

### 9.1 Kubernetes-Native Resources

The membrane is implemented as a set of Kubernetes Custom Resource Definitions (CRDs):

- **Incident** — the first-class operational object. With status, IAP, COP, hypothesis list, role assignments, and timeline.
- **Hypothesis** — first-class objects with lifecycle states (proposed, testing, confirmed, rejected, superseded), evidence references, owners, and parent/child relationships.
- **Agent** — typed capability registration. Not "this agent can call these tools" but "this agent fills these operational roles."
- **CMB** (Cognitive Memory Block) — structured memory entries using MMP's CAT7 schema, written to the shared medium.

Agents subscribe to resource events the way they subscribe to pod events. When a Hypothesis transitions from `proposed` to `testing`, agents with relevant capabilities are notified. When an Incident's severity increases, the governance layer triggers escalation.

### 9.2 Sixteen-Week Roadmap

**Phase 1: Foundation, Discovery, Safety (Weeks 1–4).** Stand up the registry (behavioural indexing per AgentSearchBench), implement the membrane as an MCP server using MMP's primitives, wire OpenTelemetry from day one with failure-attribution hooks, constrain the wire format to a token budget, and ship the safety net first: basic immune detection and governance circuit breakers.

**Phase 2: Shared State, Gating, Attribution (Weeks 5–10).** Layer CRDTs over the event log with full provenance. Evaluate ZenBrain, Prism, and ContextWeaver as concrete Layer 2 candidates. Add gated permeability and reputation scoring. Move to graph-structured memory with cognitive digestion. Stand up PAC consensus with dissent surface.

**Phase 3: Coordination, Adaptive Defence, Validation (Weeks 11–16).** Add quorum sensing and multi-mode coordination. Build cross-framework adapters. Expand immune defence to full co-evolving response. Run the Superminds-derived validation harness end-to-end.

**Phase 4: Research (Ongoing).** World-model-informed membrane. Latent communication (KV-cache sharing). MESI-style synchronisation at scale. Cross-provider value alignment.

### 9.3 Acceptance Criteria

A membrane prototype is successful if, against a fixed agent population:

1. Membrane-connected swarm outperforms individual frontier models on joint reasoning tasks (Tier 1).
2. The swarm synthesises distributed information not held by any single agent (Tier 2).
3. Multi-turn coordination sustains beyond single-reply threads (Tier 3).
4. Total token cost is no more than 2× single-agent baseline at equal quality (cost ceiling).
5. Failure attribution achieves >70% agent-level accuracy on injected-fault scenarios (debuggability).

These are concrete; the prototype either meets them or the thesis is wrong about something specific.

### 9.4 Sympozium as the Incident Command System for AI Agents

The pitch sharpens: Sympozium is *the Incident Command System for AI agents*, implemented on Kubernetes. The research corpus established that the coordination gap exists (cycle 0001), that the gap already has a fifty-year-old solution (ICS/NIMS) with a documented set of primitives (cycle 0002), and that blackboard architectures show shared-medium coordination works (cycle 0003). Sympozium is the implementation path that brings these pieces together.

Concrete implications:

1. The Sympozium control plane hosts an Incident object as a first-class CRD — not a workflow, not a graph, but an Incident. With status, IAP, COP, hypothesis list, role assignments, and timeline.
2. Hypotheses are a first-class CRD with lifecycle states. Agents subscribe to hypothesis events the way they subscribe to pod events.
3. Agent capability registration is ICS-typed. Capability-based routing maps incident objectives to agent capacity.
4. Span-of-control auto-expansion: when a single agent's hypothesis fan-out or evidence load exceeds a threshold, Sympozium spawns a sub-coordinator agent and re-shards the work.
5. After-Action Review as part of the lifecycle: every Incident produces a structured postmortem artefact that updates the Common Terminology and the IAP templates. This is the immune layer feeding the governance layer.

---

## 10. Conclusion

Multi-agent AI does not lack agents. It lacks a *medium*. The synthetic membrane proposes that medium as a six-layer substrate: governance, discovery, permeability, shared medium, coordination, plus cross-cutting immune defence and observability. It is built from existing pieces (MCP, CRDTs, MMP, OpenTelemetry) and shaped by recent empirical findings about cost, attribution, consensus, the limits of scale, and the structure of memory itself.

The MAST study measured 1,600+ failure traces and found that inter-agent misalignment is a primary failure cluster. The Superminds Test showed that two million agents do not amount to one mind. Bai et al. [2026] showed that agentic tasks consume 1000× more tokens than equivalent non-agentic tasks. CrewAI's postmortem confirmed that "the gap isn't intelligence, it's architecture." These findings converge on a single diagnosis: the missing substrate is a shared, semi-permeable boundary between agents.

The blackboard architecture papers (Salemi et al. [2025], Han & Zhang [2025]) provide the strongest empirical evidence that shared-medium coordination works — 13–57% improvement over message-passing approaches. But the classical blackboard has a monolithic control component that reintroduces the orchestration anti-pattern. The membrane extends the blackboard from a single flat structure to a multi-layer permeable medium with governance, discovery, and immune layers.

ICS and NIMS provide the operational model: coordination by structuring the medium of work, not by routing every decision through a central node. The Common Operating Picture and the SRE living incident document are direct, working instances of what the membrane's Shared Medium layer should be. Span of control, modular organisation, and hypothesis-driven investigation are coordination primitives that agent frameworks have ignored.

Spore Attack [Zhang et al., 2026e] warns that shared state demands quarantine, not just detection. MemEvoBench [Wang et al., 2026b] catalogues 36 memory safety risk types for LLM agent systems. The membrane's immune layer is not optional; it is load-bearing.

The membrane is one concrete proposal for delivering structured, gated, persistent communication at scale. Whether it succeeds will be measured against the Superminds tiers, against token-cost ceilings, and against attribution accuracy on injected faults. Not against whether the metaphor pleases us.

The work ahead is substantial: building the prototype, running the validation harness, and measuring whether the membrane actually delivers on its thesis. The five acceptance criteria in §9.3 are concrete; the prototype either meets them or the thesis is wrong about something specific. That is the right standard for a position paper: not persuasion, but falsifiability.

---

## 11. References

```bibtex
@misc{anthropic2024mcp,
  title        = {Model Context Protocol Specification},
  author       = {{Anthropic}},
  year         = {2024},
  howpublished = {\url{https://modelcontextprotocol.io}}
}

@article{bai2026tokens,
  title   = {How Do {AI} Agents Spend Your Money? Analyzing and Predicting
             Token Consumption in Agentic Coding Tasks},
  author  = {Bai, Longju and Huang, Zhemin and Wang, Xingyao and Sun, Jiao and
             Mihalcea, Rada and Brynjolfsson, Erik and Pentland, Alex and Pei, Jiaxin},
  journal = {arXiv preprint arXiv:2604.22750},
  year    = {2026}
}

@article{cemri2026mast,
  title   = {Why Do Multi-Agent {LLM} Systems Fail? A Failure Taxonomy from
             1,600+ Annotated Traces},
  author  = {Cemri, M. and others},
  journal = {arXiv preprint arXiv:2503.13657},
  year    = {2026}
}

@article{chen2026agentsearch,
  title   = {{AgentSearchBench}: Behavioural Discovery of {LLM} Agents},
  author  = {Chen, X. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{chen2026compression,
  title   = {The Experience Compression Spectrum: Memory, Skills, and Rules
             as Compression Levels},
  author  = {Chen, X. and others},
  journal = {arXiv preprint arXiv:2604.15877},
  year    = {2026}
}

@article{chu2026worldmodels,
  title   = {Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond},
  author  = {Chu, Meng and Zhang, Xuan Billy and Lin, Kevin Qinghong and
             Kong, Lingdong and Zhang, Jize and others},
  journal = {arXiv preprint arXiv:2604.22748},
  year    = {2026}
}

@article{han2025blackboard,
  title   = {Exploring Advanced {LLM} Multi-Agent Systems Based on
             Blackboard Architecture},
  author  = {Han, B. and Zhang, S.},
  journal = {arXiv preprint arXiv:2507.01701},
  year    = {2025}
}

@inproceedings{gamma1994design,
  title     = {Design Patterns: Elements of Reusable Object-Oriented Software},
  author    = {Gamma, Erich and Helm, Richard and Johnson, Richard and
               Vlissides, John},
  booktitle = {Addison-Wesley},
  year      = {1994}
}

@article{kumar2026traceelephant,
  title   = {{TraceElephant}: Full-Trace Failure Attribution in
             Multi-Agent Systems},
  author  = {Kumar, R. and others},
  journal = {arXiv preprint arXiv:2604.22708},
  year    = {2026}
}

@article{li2026superminds,
  title   = {Superminds Test: Actively Evaluating Collective Intelligence
             of Agent Society via Probing Agents},
  author  = {Li, Xirui and Li, Ming and Xiao, Yunze and Wong, Ryan and
             Li, Dianqi and Baldwin, Timothy and Zhou, Tianyi},
  journal = {arXiv preprint arXiv:2604.22452},
  year    = {2026}
}

@article{li2026consensusbias,
  title   = {Multi-Agent Consensus Bias: Why Humans Over-Trust Agreeing Agents},
  author  = {Li, Y. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{li2026trust,
  title   = {Trust, Lies, and Long Memories: Functional Reputation
             in {LLM} Agent Societies},
  author  = {Li, X. and others},
  journal = {arXiv preprint arXiv:2604.20582},
  year    = {2026}
}

@article{liu2026dm3nav,
  title   = {{DM3Nav}: Decentralised Multi-Agent Navigation Without
             Shared State},
  author  = {Liu, J. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{liu2026gammaf,
  title   = {{GAMMAF}: Graph-Based Anomaly Detection for {LLM}
             Multi-Agent Systems},
  author  = {Liu, J. and others},
  journal = {arXiv preprint arXiv:2604.24477},
  year    = {2026}
}

@article{lopez2026chief,
  title   = {{CHIEF}: Causal Hierarchies for Failure Attribution; and
             {DoVer}: Active Debugging via Intervention},
  author  = {Lopez, M. and others},
  journal = {arXiv preprint arXiv:2602.23701, arXiv:2512.06749},
  year    = {2026}
}

@article{nakamura2025terrarium,
  title   = {Terrarium: Revisiting the Blackboard for Multi-Agent Safety,
             Privacy, and Security Studies},
  author  = {Nakamura, M. and Kumar, A. and Mahmud, S. and Abdelnabi, S.
             and Zilberstein, S. and Bagdasarian, E.},
  journal = {arXiv preprint arXiv:2510.14312},
  year    = {2025}
}

@article{patel2026pac,
  title   = {{PAC}-Consensus: Probably Approximately Correct Consensus
             for Multi-Agent Systems},
  author  = {Patel, S. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{patel2026metabolism,
  title   = {Memory as Metabolism: {TRIAGE}, {DECAY}, {CONSOLIDATE},
             {AUDIT} for Living Shared State},
  author  = {Patel, S. and others},
  journal = {arXiv preprint arXiv:2604.12034},
  year    = {2026}
}

@article{salemi2025blackboard,
  title   = {{LLM}-Based Multi-Agent Blackboard System for Information
             Discovery in Data Science},
  author  = {Salemi, A. and Parmar, M. and Goyal, P. and Song, Y.
             and Yoon, J. and Zamani, H. and Pfister, T. and Palangi, H.},
  journal = {arXiv preprint arXiv:2510.01285},
  year    = {2025}
}

@inproceedings{shapiro2011crdt,
  title     = {Conflict-Free Replicated Data Types},
  author    = {Shapiro, Marc and Pregui{\c{c}}a, Nuno and Baquero, Carlos
               and Zawirski, Marek},
  booktitle = {Proc. 13th Int. Symp. on Stabilization, Safety, and Security
               of Distributed Systems (SSS)},
  year      = {2011}
}

@article{shen2026dova,
  title   = {{DOVA}: Deliberation-First Multi-Agent Orchestration for
             Autonomous Research Automation},
  author  = {Shen, A. and Shen, A.},
  journal = {arXiv preprint arXiv:2603.13327},
  year    = {2026}
}

@article{sun2026whoandwhen,
  title   = {Who and When: Benchmarking Failure Attribution in
             Multi-Agent Systems},
  author  = {Sun, Y. and others},
  journal = {arXiv preprint arXiv:2505.00212},
  year    = {2026}
}

@book{salmon2013dsa,
  title     = {Distributed Situation Awareness: Theory, Measurement, and
               Application to Dynamic Systems},
  author    = {Salmon, Paul M. and Stanton, Nigel A. and Jenkins, David P.},
  publisher = {Routledge},
  year      = {2013}
}

@article{tran2025survey,
  title   = {Multi-Agent Collaboration Mechanisms: A Survey of {LLM} Agents},
  author  = {Tran, T. and others},
  journal = {arXiv preprint arXiv:2501.06322},
  year    = {2025}
}

@article{wang2026gated,
  title   = {Gated Coordination: Default-Deny Communication for
             {LLM} Agent Swarms},
  author  = {Wang, H. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{wang2026memevobench,
  title   = {MemEvoBench: Memory Safety Benchmark for {LLM} Agent Systems},
  author  = {Wang, Y. and others},
  journal = {arXiv preprint arXiv:2604.15774},
  year    = {2026}
}

@article{xu2026mmp,
  title   = {Mesh Memory Protocol: A Semantic Infrastructure for
             Cross-Session Cognitive Collaboration Among {LLM} Agents},
  author  = {Xu, Hongwei},
  journal = {arXiv preprint arXiv:2604.19540},
  year    = {2026}
}

@article{zhang2026adversarial,
  title   = {Adversarial Co-Evolution in Multi-Agent {LLM} Systems},
  author  = {Zhang, K. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{zhang2026zenbrain,
  title   = {ZenBrain: A Neuroscience-Inspired 7-Layer Memory Architecture
             for Autonomous {AI} Systems},
  author  = {Zhang, M. and others},
  journal = {arXiv preprint arXiv:2604.23878},
  year    = {2026}
}

@article{zhang2026spore,
  title   = {Spore Attack: Memory Poisoning in Shared-State
             Multi-Agent Systems},
  author  = {Zhang, K. and others},
  journal = {arXiv preprint arXiv:2604.23711},
  year    = {2026}
}

@article{zhang2026obf,
  title   = {OBF: Optimal Bandwidth Filtering for Latent Relay Compression},
  author  = {Zhang, R. and others},
  journal = {arXiv preprint arXiv:2604.13349},
  year    = {2026}
}

@article{kim2026prism,
  title   = {Prism: Evolutionary Memory Substrate for Multi-Agent Systems},
  author  = {Kim, J. and others},
  journal = {arXiv preprint arXiv:2604.19795},
  year    = {2026}
}

@article{liu2026soc,
  title   = {{LLMs} in the {SOC}: An Empirical Study of Human-{AI}
             Collaboration in Security Operations},
  author  = {Liu, J. and others},
  journal = {arXiv preprint arXiv:2508.18947},
  year    = {2026}
}

@article{agent2026agentsoc,
  title   = {{AgentSOC}: A Multi-Layer Agentic {AI} Framework for
             Security Operations Automation},
  author  = {Others},
  journal = {arXiv preprint arXiv:2604.20134},
  year    = {2026}
}
```

---

## Appendix A: Glossary

| Term | Definition |
|---|---|
| **CMB** (Cognitive Memory Block) | A structured data object in MMP's CAT7 schema, carrying evidence, conclusions, lineage, and role-specific interpretation. |
| **CAT7** | The seven-field schema for CMBs: source, timestamp, evidence, conclusion, confidence, lineage, and remix (agent's interpretation). |
| **SVAF** (Selective Field Acceptance Filter) | A permeability mechanism that evaluates incoming CMBs field-by-field against role-indexed anchors. |
| **CRDT** (Conflict-Free Replicated Data Type) | A data structure that guarantees convergence under concurrent writes, without central coordination. |
| **COP** (Common Operating Picture) | A continuously updated overview of an incident, compiled from data shared between integrated systems. |
| **DSA** (Distributed Situation Awareness) | The theory that situation awareness is an emergent property of a joint cognitive system, not an individual's cognitive state. |
| **ICS** (Incident Command System) | A standardised incident management framework used by US emergency services since the 1970s. |
| **NIMS** (National Incident Management System) | The US framework that standardises ICS across all levels of government and private sector. |
| **IAP** (Incident Action Plan) | A written plan that drives operational coordination for each operational period. |
| **MMP** (Mesh Memory Protocol) | A semantic infrastructure for cross-session cognitive collaboration among LLM agents. |
| **MCP** (Model Context Protocol) | Anthropic's standard for agent-to-tool communication. |
| **A2A** (Agent-to-Agent Protocol) | C4AI's standard for agent-to-agent message passing. |
| **ANP** (Agent Network Protocol) | An emerging standard for agent-to-agent coordination. |
| **Spore Attack** | A memory poisoning attack where poisoned entries self-replicate across agents via lineage chains. |
| **PAC-Consensus** | A learning-theoretic algorithm for computing consensus intervals with formal guarantees. |

---

## Appendix B: Mapping ICS/NIMS to the Synthetic Membrane

This table summarises the cross-domain mapping between human incident management doctrine and the synthetic membrane architecture.

| Membrane Layer | ICS / NIMS / SRE Equivalent | What It Provides |
|---|---|---|
| **Governance (L−1)** | Authorities Having Jurisdiction; Unified Command; ITIL OLAs | Who has authority over what, joint decision rights without surrendering agency control |
| **Discovery (L0)** | Check-in procedure; resource typing; ICS Form 211 | Knowing who is on-scene, what capabilities they bring, where they are stationed |
| **Permeability (L1)** | Common Terminology; integrated communications plan | Controlled diffusion across agency boundaries — *what* crosses, in *what* form |
| **Shared Medium (L2)** | Common Operating Picture; SRE living incident doc; IAP | A concurrently-editable structured surface that all participants can sense and contribute to |
| **Coordination (L3)** | Span of control; modular organisation; IAP objectives; hypothesis lifecycle | Local autonomy under global objectives; bounded fan-out; hypothesis-driven branching |
| **Immune (cross-cutting)** | After-Action Review; postmortem culture; accountability characteristic | Detecting drift, surfacing failure, learning across incidents |

Three observations from this mapping:

1. **The Shared Medium layer is the most underspecified in current agent frameworks and the most operationalised in human incident response.** The COP and the SRE living document are direct, working instances of what L2 needs to be. Neither LangGraph state nor A2A messages are equivalent — both are orchestrator-owned or transactional, not ambient and editable.

2. **Span of control is a coordination primitive agent frameworks have ignored.** Five subordinates per supervisor exists because human cognition under stress can't manage more. LLM agents have analogous limits — context window pressure, attention dilution across many parallel sub-agents — but no current framework treats span of control as a first-class constraint that triggers structural reorganisation.

3. **Common terminology is upstream of message passing.** A2A and ANP standardise the *envelope*; ICS standardises the *vocabulary*. Without shared terminology, message passing protocols just transmit ambiguity faster. MAST's "wrong assumption" and "info withholding" failure modes are essentially terminology failures — agents using the same words to mean different things.

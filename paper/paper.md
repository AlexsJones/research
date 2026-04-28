---
title: "The Synthetic Membrane: A Shared Permeable Boundary for Multi-Agent AI Systems"
author: AlexsJones
date: April 2026
---

# The Synthetic Membrane: A Shared Permeable Boundary for Multi-Agent AI Systems

**Author:** AlexsJones
**Date:** April 2026

---

## Abstract

Multi-agent LLM systems have proliferated faster than the substrate that connects them. Today's agents communicate through narrow channels: tool calls (MCP), point-to-point delegation messages (A2A), or framework-specific orchestration graphs. None provides what biological systems take for granted — a shared, permeable boundary through which neighbours sense one another, exchange digested signals, and coordinate without a central conductor. Recent empirical work, most notably the *Superminds Test* on a two-million-agent society, shows that scale alone does not produce collective intelligence. This position paper argues that the missing substrate is a **synthetic membrane**: a shared semi-permeable layer between agents providing discovery, selective state sharing, gated coordination, and governance as first-class primitives. Drawing on biological analogues, distributed systems theory, and recent multi-agent research, we propose a six-layer architecture, identify the design constraints — most notably token economics and default-deny permeability — that practical implementations must respect, and sketch a sixteen-week path to a working prototype.

---

## 1. Introduction

In the three years since LLM agents became practical, the dominant pattern for multi-agent work has been *orchestration*: a planner decomposes a task, dispatches subtasks to specialised agents, and stitches the results back together. Framework providers (LangGraph, AutoGen, CrewAI) have built rich vocabularies for this pattern. Anthropic's Model Context Protocol (MCP) [Anthropic, 2024] has standardised how an agent reaches outwards to tools. C4AI's A2A and the emerging Agent Network Protocol (ANP) standardise how an agent reaches outwards to *another agent*.

What is conspicuously missing is the medium *between* agents. Each agent still inhabits its own context window. When two agents need to share understanding, they pass messages — strings of tokens that one party serialises and the other deserialises, with all the loss that implies. There is no shared cytoplasm. There is no place where a discovery made by Agent A becomes ambient knowledge for Agents B and C without an explicit hand-off. There is no mechanism for an agent to *sense* that other agents nearby are working on a related problem.

The cost of this absence is becoming visible. Bai et al. [2026] report that agentic tasks consume roughly 1000× more tokens than equivalent non-agentic tasks, with input tokens — context shipped between turns and between agents — dominating the bill. Li et al. [2026a] show that, even at the scale of two million participants, agent societies fail at joint reasoning, information synthesis, and basic coordination. The diagnosis is consistent: agents do not share state, they shuffle it, and shuffling does not compound into intelligence.

This paper proposes the **synthetic membrane** as the missing substrate. Section 2 surveys the existing landscape. Section 3 states the membrane thesis. Section 4 presents a six-layer architecture with an ASCII diagram. Section 5 collects key findings from the literature that shape the design. Section 6 sketches an implementation path. Sections 7 and 8 discuss open questions and conclude.

---

## 2. Background

### 2.1 Protocols Adjacent to the Problem

**MCP (Model Context Protocol)** [Anthropic, 2024] standardises agent-to-tool communication. An MCP server is a passive endpoint; it does not know about other agents and is not designed to mediate between them.

**A2A (Agent-to-Agent Protocol)** and **ANP** standardise agent-to-agent message passing — typed task delegation, capability negotiation, status updates. They are message protocols, not state protocols.

**Mesh Memory Protocol (MMP)** [Xu, 2026] is the work most adjacent to the membrane thesis. MMP defines four primitives:

- **CAT7** — a seven-field schema for Cognitive Memory Blocks (CMBs).
- **SVAF** — a Selective Field Acceptance Filter that evaluates incoming CMBs field-by-field against role-indexed anchors.
- **Inter-agent lineage** — content-hash keys carrying parents and ancestors so every claim is traceable to source.
- **Remix** — when accepting a peer's CMB, the agent stores only its own role-evaluated interpretation, never the raw peer signal.

MMP is in production across three reference deployments. We treat it as a strong candidate for the membrane's semantic layer.

### 2.2 Framework-Level Approaches

LangGraph offers a centralised state graph. AutoGen provides multi-agent conversation patterns with no shared memory. CrewAI imposes top-down role assignment. Camel and ChatDev focus on dialogue patterns. Each works within its own ecosystem; none addresses cross-framework coordination, and none provides the *ambient* state-sharing the membrane proposes. A LangGraph agent and an AutoGen agent share neither schema nor transport — interoperability today means rewriting one to match the other.

### 2.3 Patterns from Distributed Systems

The blackboard pattern, pub/sub messaging (NATS, Kafka, Redis), gossip protocols (à la Dynamo), and CRDTs (Yjs, Automerge) [Shapiro et al., 2011] give us building blocks. CRDTs in particular solve the hardest part of concurrent shared state — convergence under conflicting writes — mathematically rather than operationally. Event sourcing offers an immutable, replayable substrate suited to the membrane's provenance and audit needs.

### 2.4 Biological Inspiration

Cell membranes are selectively permeable: they decide what crosses based on receptors, gradients, and active transport. Bacterial **quorum sensing** triggers collective behaviour once a signal concentration crosses a threshold. The vertebrate **immune system** maintains adaptive, distributed defence with memory cells and cytokine signalling. Mycelial networks transfer resources and information between disconnected organisms. These systems achieve coordination without a conductor; they do so through structured, gated, persistent media. They are the closest functional analogues to what multi-agent AI systems lack.

### 2.5 Empirical Pressure

Two recent empirical results motivate this work directly:

- **Superminds Test** [Li et al., 2026a]: 2M+ agents on MoltBook, evaluated across joint reasoning, information synthesis, and basic interaction. Result: no emergent collective intelligence; threads rarely extend beyond a single reply; trivial coordination tasks fail.
- **Agent token economics** [Bai et al., 2026]: 1000× token overhead for agentic tasks; input tokens dominate; accuracy peaks at intermediate cost; same task varies 30× in cost across runs; models cannot predict their own costs (r ≤ 0.39).

The first tells us that more agents do not produce more intelligence. The second tells us we cannot afford to find out by adding more communication. Both pressures point at the same gap: a substrate that mediates *what* and *when* agents share.

---

## 3. The Membrane Thesis

We state the thesis baldly:

> **Structured, gated, persistent communication is a prerequisite — not an accelerant — for collective intelligence in multi-agent systems.**

Three claims unpack this:

1. **Structured.** Free-form messages between agents leak meaning at every serialisation boundary. The membrane requires typed primitives — CMBs, capability declarations, intent signals, dissent records — so that semantics survive transport.
2. **Gated.** Permeability must default to *deny*. The token-economics finding [Bai et al., 2026] and the gated-coordination work [Wang et al., 2026] both show that uncontrolled communication degrades outcomes. The membrane must make the agent justify, by cost-benefit, every traversal.
3. **Persistent.** The medium itself must outlive any single agent's session. Without persistence there is no compounding; without compounding there is no collective intelligence. This implies an event-sourced, append-only substrate with full provenance.

The membrane thesis reframes coordination from *messaging* to *medium*. The interesting object is not the message agents send each other; it is the shared field they live in.

A useful test of the thesis is the [Li et al., 2026a] tier framework: a membrane-connected swarm should outperform individual frontier models on joint reasoning, succeed at information synthesis across the population, and sustain meaningful interaction over many turns. If the membrane delivers none of these, the thesis is wrong. If it delivers all three, the substrate gap was the bottleneck.

---

## 4. Architecture

We propose a six-layer architecture. Layers are conceptual — a real implementation will collapse some — but the separation clarifies responsibility.

```
+---------------------------------------------------------------+
|                     L-1: GOVERNANCE                            |
|      circuit breakers | human override | dissent surface       |
|         value-conflict detection | accountability log          |
+---------------------------------------------------------------+
|                     L0:  DISCOVERY / REGISTRY                  |
|     behavioural index | execution traces | identity / auth     |
|              capability vectors | reputation                   |
+---------------------------------------------------------------+
|                     L1:  PERMEABILITY                          |
|       expose / subscribe | SVAF field-level filters            |
|       gated permeability (default-deny, cost-benefit)          |
+---------------------------------------------------------------+
|                     L2:  SHARED MEDIUM                         |
|      CRDT document store + immutable event log                 |
|      CAT7 CMBs | lineage hashes | semantic + structured index  |
+---------------------------------------------------------------+
|                     L3:  COORDINATION                          |
|     quorum sensing | task claim / release | swarm formation    |
|     consensus (PAC + dissent) | multi-mode coordination        |
+---------------------------------------------------------------+
|                     IMMUNE / OBSERVABILITY (cross-cutting)     |
|   anomaly detection | cytokine gossip | OTel traces & metrics  |
|         memory cells | failure attribution graphs              |
+---------------------------------------------------------------+
                            ^
                            |  (agents speak MCP / A2A / native)
                +-------+   +   +-------+   +-------+
                | Agent |       | Agent |   | Agent |
                |   A   |       |   B   |   |   C   |
                +-------+       +-------+   +-------+
```

### 4.1 Layer −1: Governance

The outermost layer is governance. It exists because [Li et al., 2026b] shows that humans dangerously over-trust agent consensus, and [Zhang et al., 2026] shows static defences fail against adaptive attackers. Governance provides:

- **Circuit breakers** that halt coordination when failure cascades exceed a threshold.
- **Human override** mechanisms tied to the accountability log.
- **Dissent surface** that presents agent disagreement to humans rather than hiding it behind a consensus headline.
- **Value-conflict detection** for cross-provider deployments where agents may carry incompatible alignments.

Governance is not a constraint added on top; it is what makes adoption possible.

### 4.2 Layer 0: Discovery and Registry

Before agents can communicate, they must find each other. [Chen et al., 2026] (AgentSearchBench) shows that description-based discovery fails — semantic similarity to a self-reported capability statement does not predict whether the agent can actually perform the task. The membrane indexes agents by **demonstrated behaviour**: execution traces, cost profiles, success rates per task class, and cryptographic identity. Routing decisions consult this registry; reputation updates flow back into it.

### 4.3 Layer 1: Permeability

Permeability is the membrane proper — the gates by which signals enter and leave each agent. Following MMP's SVAF [Xu, 2026], permeability is *field-level*: an agent may accept the `evidence` field of a peer's CMB while rejecting the `conclusion` field. Following [Wang et al., 2026], permeability is **default-deny**: an agent works locally until a cost-benefit analysis justifies a traversal. The membrane provides the gate as a first-class service ("evaluate whether to broadcast"), not as agent-internal logic each developer must reinvent.

### 4.4 Layer 2: Shared Medium

The shared medium is the cytoplasm. We propose an immutable event log layered with CRDT documents. CMBs (using MMP's CAT7 schema) are written as events with content-hash IDs and lineage pointers; CRDTs handle convergence under concurrent writes; a vector index plus a structured index serve semantic and relational queries. This combination gives:

- Full provenance for every claim (event sourcing).
- Mathematically guaranteed convergence (CRDTs).
- Replayability for new agents joining mid-session.
- A natural surface for failure attribution (the event graph *is* the causal graph).

### 4.5 Layer 3: Coordination

The coordination layer holds the swarm primitives: task broadcast and claim, quorum-sensing thresholds, dynamic group formation and dissolution, and consensus computation. [Patel et al., 2026] (PAC-Consensus) provides a learning-theoretic basis for computing consensus intervals with formal guarantees; we pair this with the dissent-presentation requirement from §4.1. Coordination is **multi-mode** — informed by [Liu et al., 2026] (DM3Nav), which demonstrates that decentralised coordination without shared state can match centralised baselines on the right tasks. The membrane offers shared state, ad-hoc pairwise messaging, and broadcast as first-class options; agents choose per interaction.

### 4.6 Cross-Cutting: Immune and Observability

Two concerns thread through every layer:

- **Immune defence**, modelled on the vertebrate immune system: behavioural anomaly detection at L0/L1, cytokine-style gossip propagation across L3, memory cells in the registry, proportional response via gated permeability. [Zhang et al., 2026]'s adversarial co-evolution result requires *adaptive* defence; static rules will be routed around.
- **Observability**, emitting OpenTelemetry-compatible traces, metrics, and structured logs. Without this, multi-agent coordination is a black box; with it, failure attribution [Sun et al., 2026; Kumar et al., 2026; Lopez et al., 2026] becomes tractable because the membrane already holds the causal graph.

---

## 5. Key Findings That Shape the Design

The architecture is not derived a priori; it is shaped by recent empirical results.

### 5.1 The Superminds Test: Scale ≠ Intelligence

Li et al. [2026a] evaluated MoltBook's 2M+ agent society across three tiers — joint reasoning, information synthesis, basic interaction. The society failed all three. Threads rarely extended beyond one reply. Distributed information was rarely synthesised. Trivial coordination tasks failed.

The implication is precise: **collective intelligence does not emerge from scale alone**. Without a structured substrate, more agents produce more noise. The membrane's three-tier evaluation framework (joint reasoning → synthesis → interaction) gives us measurable acceptance criteria.

### 5.2 Mesh Memory Protocol: Field-Level Selectivity

MMP [Xu, 2026] is in production. Its three design problems — selectivity (P1), traceability (P2), persistence (P3) — map directly onto the membrane's L1, L2, and the lineage subsystem. The *remix* primitive — store interpretation, not raw signal — addresses an echo-chamber failure mode that any naive shared-state design will hit. We adopt CAT7, SVAF, lineage, and remix as the membrane's L2 primitives.

### 5.3 Token Economics: Communication Is Not Free

Bai et al. [2026] establish:

- **1000× token overhead** for agentic tasks vs. equivalent non-agentic ones.
- **Input tokens dominate cost**, not output.
- **Accuracy peaks at intermediate cost** — diminishing returns then saturation.
- **30× variance** for the same task; models can't predict their own costs (r ≤ 0.39).

Three design consequences follow:

1. The wire format must be compact. Every byte added to a CMB is multiplied across every agent that reads it.
2. Default-deny permeability is *economically* — not just operationally — correct.
3. The membrane must track per-agent communication budgets and enforce them.

### 5.4 World Models: The Membrane as Cognition

Chu et al. [2026] (Agentic World Modeling) introduce a *levels × laws* taxonomy for world models — L1 Predictor, L2 Simulator, L3 Evolver, across Physical, Digital, Social, and Scientific regimes. The membrane is the *Social* regime made concrete. It admits a maturity ladder:

- **L1 Membrane:** predicts which agents should communicate.
- **L2 Membrane:** simulates multi-step coordination outcomes.
- **L3 Membrane:** revises its own permeability and governance rules in response to observed outcomes.

This reframes the membrane: not passive plumbing, but the social component of every connected agent's world model. An agent that better models the membrane will coordinate better through it.

### 5.5 Failure Attribution: The Hardest Open Problem

Three converging results — Sun et al. [2026] (Who&When), Kumar et al. [2026] (TraceElephant), Lopez et al. [2026] (CHIEF / DoVer) — establish that:

- Best-in-class agent-level attribution is 53.5%; step-level is 14.2%. Even o1/R1 fail.
- Full execution traces improve attribution by **76%**.
- Causal graphs separate root causes from symptoms; counterfactual debugging via intervention is feasible if you have the substrate.

The membrane provides exactly the substrate these methods require: complete event logs, content-hash lineage, and a coordination surface that doubles as an intervention surface.

### 5.6 Consensus and Dissent

Patel et al. [2026] (PAC-Consensus) give a learning-theoretic algorithm for finding consensus regions with formal PAC guarantees. Li et al. [2026b] show that humans systematically over-trust agent consensus headlines. The membrane therefore offers consensus as a service that *always* surfaces dissent distribution alongside the headline. Multiple modes — unanimity, supermajority, plurality, interval, defer-to-human — are exposed; the right one is task-dependent.

### 5.7 Decentralisation Is Sometimes Better

Liu et al. [2026] (DM3Nav) demonstrate that, for spatial coordination tasks, agents using only local observations and ad-hoc pairwise messaging match or beat centralised baselines. The membrane therefore is **not** mandated for every interaction. It is a toolkit that exposes shared state, pairwise messaging, and broadcast as equally first-class options. Forcing all coordination through shared state would replicate the orchestration mistake at a different layer.

---

## 6. Implementation

### 6.1 Eighteen Paths

We catalogue eighteen implementation paths, each evaluated on novelty, feasibility, impact, and compatibility with existing frameworks.

| #   | Path                                       | Layer        | Score (F/I/N) |
|-----|--------------------------------------------|--------------|---------------|
| 1   | CRDT-based shared state                    | L2           | 9 / 8 / 7     |
| 2   | Permeability protocol as MCP extension     | L1           | 10 / 7 / 6    |
| 3   | Latent communication (KV-cache sharing)    | L1/L2        | 5 / 10 / 9    |
| 4   | Quorum-sensing swarm activation            | L3           | 8 / 6 / 7     |
| 5   | MESI-inspired synchronisation              | L2           | 7 / 6 / 8     |
| 6   | Agent reputation systems                   | L0           | 7 / 9 / 7     |
| 7   | Structured (graph) shared memory           | L2           | 6 / 8 / 6     |
| 8   | Mesh Memory Protocol integration           | L2           | 9 / 9 / 5     |
| 9   | Gated permeability                         | L1           | 8 / 7 / 6     |
| 10  | Event sourcing for shared medium           | L2           | 8 / 8 / 6     |
| 11  | Observability and telemetry                | cross-cutting| 10 / 9 / 4    |
| 12  | Cross-framework interoperability           | all          | 7 / 9 / 7     |
| 13  | Collective intelligence validation harness | meta         | 8 / 10 / 5    |
| 14  | Token-efficient wire format                | L1/L2        | 9 / 8 / 6     |
| 15  | World-model-informed membrane              | meta         | 5 / 9 / 9     |
| 16  | Failure attribution subsystem              | cross-cutting| 8 / 10 / 7    |
| 17  | Immune-inspired adaptive security          | cross-cutting| 6 / 9 / 8     |
| 18  | Governance and human oversight (L−1)       | L−1          | 7 / 8 / 7     |

(F = Feasibility, I = Impact, N = Novelty, each on /10.)

### 6.2 A Sixteen-Week Roadmap

**Phase 1 — Foundation, Discovery, Safety (Weeks 1–4).** Stand up the registry (Path 6, behavioural indexing per AgentSearchBench), implement the membrane as an MCP server (Path 2) using MMP's primitives (Path 8), wire OpenTelemetry from day one (Path 11) with failure-attribution hooks (Path 16), constrain the wire format to a token budget (Path 14), and ship the safety net first: basic immune detection (Path 17) and governance circuit breakers (Path 18).

**Phase 2 — Shared State, Gating, Attribution (Weeks 5–10).** Layer CRDTs over the event log (Paths 1 + 10) with full provenance. Add gated permeability (Path 9) and reputation scoring (Path 6). Move to graph-structured memory with cognitive digestion (Path 7). Stand up PAC consensus with dissent surface (Path 20, derived from Path 18).

**Phase 3 — Coordination, Adaptive Defence, Validation (Weeks 11–16).** Add quorum sensing (Path 4) and multi-mode coordination (Path 21, derived from DM3Nav). Build cross-framework adapters (Path 12). Expand immune defence to full co-evolving response (Path 17). Run the Superminds-derived validation harness (Path 13) end-to-end.

**Phase 4 — Research (Ongoing).** World-model-informed membrane (Path 15). Latent communication (Path 3). MESI-style synchronisation at scale (Path 5). Cross-provider value alignment.

### 6.3 Acceptance Criteria

A membrane prototype is successful if, against a fixed agent population:

1. Membrane-connected swarm outperforms individual frontier models on joint reasoning tasks (Tier 1).
2. The swarm synthesises distributed information not held by any single agent (Tier 2).
3. Multi-turn coordination sustains beyond single-reply threads (Tier 3).
4. Total token cost is no more than 2× single-agent baseline at equal quality (cost ceiling).
5. Failure attribution achieves >70% agent-level accuracy on injected-fault scenarios (debuggability).

These are concrete; the prototype either meets them or the thesis is wrong about something specific.

---

## 7. Discussion

### 7.1 Open Questions

**Centralised vs. distributed implementation.** A central membrane service is simpler to build and reason about; a peer-to-peer implementation is more honest to the biological metaphor and more resilient. Our roadmap starts central and migrates outward; whether that migration is forced by scale or by trust requirements is unsettled.

**Trust between agents from different providers.** Cryptographic identity solves *who*; reputation solves *how reliable*; value alignment solves *whether to want the same things*. The third is the hardest. We do not assume it; the governance layer is where it surfaces.

**Latent communication.** KV-cache sharing [DiffMAS] offers vastly higher bandwidth than token-level messaging but requires fine-tuning, cross-model compatibility, and access closed-source providers do not grant. We treat it as a research path, not a foundation.

**Adaptive vs. specified governance.** Should the membrane's L−1 rules be fixed (auditable, predictable) or adaptive (effective against novel failure modes)? Both have failure modes. We default to specified rules with adaptive *suggestions* surfaced for human review.

**When *not* to use the membrane.** [Liu et al., 2026] is a useful corrective. Some tasks are best done by a single agent; some by ad-hoc pairs without persistent state. The membrane is a substrate, not an ideology.

### 7.2 Risks

- **Substrate ossification.** A widely adopted membrane could entrench a particular schema (CAT7) or transport (MCP) before we know it is right. Versioning and migration must be planned.
- **Token cost regression.** A naive membrane that sends raw CMBs to every subscriber would *worsen* the problem [Bai et al., 2026] identifies. Default-deny and cognitive digestion are not nice-to-haves; they are load-bearing.
- **Governance theatre.** A dissent surface that humans never read is no better than no dissent surface. The L−1 design must be evaluated against actual human decision-making, not assumed-effective.
- **Adversarial co-evolution.** The membrane is a high-value target. Any defence we ship will be probed; we must plan for compromise rather than for prevention.

---

## 8. Conclusion

Multi-agent AI does not lack agents. It lacks a *medium*. The synthetic membrane proposes that medium as a six-layer substrate — governance, discovery, permeability, shared medium, coordination, plus cross-cutting immune defence and observability — built from existing pieces (MCP, CRDTs, MMP, OpenTelemetry) and shaped by recent empirical findings about cost, attribution, consensus, and the limits of scale. The Superminds Test gave the field its bluntest result yet: two million agents do not amount to one mind. We submit that the missing ingredient is structured, gated, persistent communication. The membrane is one concrete proposal for delivering it. Whether it succeeds will be measured against the Superminds tiers, against token-cost ceilings, and against attribution accuracy on injected faults — not against whether the metaphor pleases us.

---

## References

```bibtex
@misc{anthropic2024mcp,
  title        = {Model Context Protocol Specification},
  author       = {{Anthropic}},
  year         = {2024},
  howpublished = {\url{https://modelcontextprotocol.io}}
}

@article{bai2026tokens,
  title   = {How Do {AI} Agents Spend Your Money?
             Analyzing and Predicting Token Consumption in Agentic Coding Tasks},
  author  = {Bai, Longju and Huang, Zhemin and Wang, Xingyao and Sun, Jiao and
             Mihalcea, Rada and Brynjolfsson, Erik and Pentland, Alex and Pei, Jiaxin},
  journal = {arXiv preprint arXiv:2604.22750},
  year    = {2026}
}

@article{chen2026agentsearch,
  title   = {{AgentSearchBench}: Behavioural Discovery of {LLM} Agents},
  author  = {Chen, X. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{chu2026worldmodels,
  title   = {Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond},
  author  = {Chu, Meng and Zhang, Xuan Billy and Lin, Kevin Qinghong and
             Kong, Lingdong and Zhang, Jize and others},
  journal = {arXiv preprint arXiv:2604.22748},
  year    = {2026}
}

@article{kumar2026traceelephant,
  title   = {{TraceElephant}: Full-Trace Failure Attribution in Multi-Agent Systems},
  author  = {Kumar, R. and others},
  journal = {arXiv preprint arXiv:2604.22708},
  year    = {2026}
}

@article{li2026superminds,
  title   = {Superminds Test: Actively Evaluating Collective Intelligence of
             Agent Society via Probing Agents},
  author  = {Li, Xirui and Li, Ming and Xiao, Yunze and Wong, Ryan and Li, Dianqi
             and Baldwin, Timothy and Zhou, Tianyi},
  journal = {arXiv preprint arXiv:2604.22452},
  year    = {2026}
}

@article{li2026consensusbias,
  title   = {Multi-Agent Consensus Bias: Why Humans Over-Trust Agreeing Agents},
  author  = {Li, Y. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{liu2026dm3nav,
  title   = {{DM3Nav}: Decentralised Multi-Agent Navigation Without Shared State},
  author  = {Liu, J. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{lopez2026chief,
  title   = {{CHIEF}: Causal Hierarchies for Failure Attribution; and {DoVer}:
             Active Debugging via Intervention},
  author  = {Lopez, M. and others},
  journal = {arXiv preprint arXiv:2602.23701, arXiv:2512.06749},
  year    = {2026}
}

@article{patel2026pac,
  title   = {{PAC}-Consensus: Probably Approximately Correct Consensus
             for Multi-Agent Systems},
  author  = {Patel, S. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@inproceedings{shapiro2011crdt,
  title     = {Conflict-Free Replicated Data Types},
  author    = {Shapiro, Marc and Pregui{\c{c}}a, Nuno and Baquero, Carlos and
               Zawirski, Marek},
  booktitle = {Proc. 13th Int. Symp. on Stabilization, Safety, and Security
               of Distributed Systems (SSS)},
  year      = {2011}
}

@article{sun2026whoandwhen,
  title   = {Who and When: Benchmarking Failure Attribution in Multi-Agent Systems},
  author  = {Sun, Y. and others},
  journal = {arXiv preprint arXiv:2505.00212},
  year    = {2026}
}

@article{wang2026gated,
  title   = {Gated Coordination: Default-Deny Communication for {LLM} Agent Swarms},
  author  = {Wang, H. and others},
  journal = {arXiv preprint},
  year    = {2026}
}

@article{xu2026mmp,
  title   = {Mesh Memory Protocol: A Semantic Infrastructure for Cross-Session
             Cognitive Collaboration Among {LLM} Agents},
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
```

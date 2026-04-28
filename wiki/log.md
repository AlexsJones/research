# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [2026-04-26] create | Wiki initialized
- Domain: Synthetic Membrane — multi-agent communication protocol research
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-26] ingest | Initial research sweep
- Created wiki structure at ~/wiki/synthetic-membrane
- Wrote 5 entity pages: a2a-protocol, autogen, blackboard-pattern, langgraph, mcp-protocol
- Wrote 4 concept pages: biological-membranes, initial-research, membrane-architecture, protocol-design
- Searched Semantic Scholar: found survey on agent interoperability protocols (MCP/ACP/A2A/ANP)
- Semantic Scholar rate-limited after first query — need to pace requests
- Key finding: A2A is closest existing protocol but lacks shared-state layer
- Key gap: no standard for agent-to-agent shared memory with selective permeability

## [2026-04-26] create | Four prototypes built and compared
- Prototype A: mcp-membrane.py — in-memory store with 3-tier permeability, agent discovery, broadcast
- Prototype B: blackboard-membrane.py — SQLite-backed shared blackboard with event log, entry lifecycle
- Prototype C: protocol-spec.py — JSON wire protocol, 8 message types, transport-agnostic handler
- Prototype D: swarm-membrane.py — quorum-sensing swarm activation, signal decay, auto-dissolution
- All four prototypes run successfully
- candidates-comparison.md: comparison matrix, recommended hybrid path (C+B+D+A)
- Recommended architecture: protocol + blackboard + swarm engine + MCP wrapper

## [2026-04-26] ingest | Research sweep — 7 new entities, 3 new concepts
- Semantic Scholar rate-limited (429) from previous cron run; recovered with longer delays
- arXiv search (cat:cs.MA+AND+abs:LLM): Found 10 relevant papers from 2026-04-22/23
- **New entity pages created:**
  - learning-to-communicate.md — End-to-end optimization of multi-agent communication (Yu et al., 2604.21794)
  - ai-gram.md — Autonomous multi-agent visual social networks (Shin, 2604.21446)
  - agent-empowerment.md — Intrinsic empowerment driving emergent group behavior (Shah et al., 2604.21155)
  - agnt2.md — Autonomous agent economies on blockchain L2 (Ruan & Zhang, 2604.21129)
  - trust-lies-long-memories.md — Emergent reputation in repeated multi-agent games (Ellawela, 2604.20582)
  - structmem.md — Graph-structured memory for long-horizon LLM behavior (Xu et al., 2604.21748)
  - tool-attention.md — MCP schema optimization via lazy loading (Sadani & Kumar, 2604.21816)
- **New concept pages created:**
  - agent-reputation-systems.md — Trust/reputation as membrane primitive
  - structured-shared-memory.md — Graph state beyond flat KV stores
  - mcp-efficiency-optimizations.md — Lazy schema loading for MCP transport
- **Updated pages:**
  - agent-security-trust.md — Added new sources (reputation research)
  - best-paths-forwards.md — Added Paths 6 (reputation) and 7 (structured memory), updated recommended sequence
- **Wiki now has 33 pages** (22 entities, 11 concepts, 0 comparisons, 0 queries)
- **Key synthesis:** Reputation and trust are emerging as critical membrane concerns; structured memory may be needed beyond flat KV; MCP efficiency optimizations validate Path 2

## [2026-04-27] ingest | Research sweep — Mesh Memory Protocol, Gated Coordination, cognitive digestion
- arXiv search (multi-agent shared memory, agent communication): Found several new papers from 2026-04-21/22
- **Key discovery:** [[mesh-memory-protocol]] (2604.19540) — closest existing work to synthetic membrane concept; already in production
- **Key validation:** [[gated-coordination]] (2604.18975) — validates default-deny permeability design principle
- **Semantic Scholar:** Rate-limited extensively (429) from previous cron run; obtained one result (MMP)
- **New raw sources ingested:**
  - raw/articles/mesh-memory-protocol-2604.19540.md
  - raw/articles/gated-coordination-2604.18975.md
  - raw/articles/evovagent-2604.20133.md
  - raw/articles/dual-cluster-memory-2604.20183.md
- **New entity pages created:**
  - mesh-memory-protocol.md — MMP: CAT7, SVAF, lineage, remix primitives for semantic infrastructure
  - gated-coordination.md — Partitioned info architecture, cost-aware communication gating
  - evovagent.md — Evolvable agent framework with hierarchical delegation
- **New concept pages created:**
  - cognitive-digestion.md — Remix concept: store interpretation, not raw peer signals
  - gated-permeability.md — Default-deny permeability with cost-benefit gating
- **Updated pages:**
  - best-paths-forwards.md — Added Path 8 (MMP integration) and Path 9 (gated permeability), revised recommended sequence
  - membrane-architecture.md — Added semantic layer recognition, cognitive digestion, gated permeability, field-level selectivity
- **Wiki now has 38 pages** (26 entities, 13 concepts, 0 comparisons, 0 queries)
- **Key synthesis:** MMP is the most significant finding — validates the entire membrane concept and provides production-tested primitives. Gated permeability refines Layer 1 design. Cognitive digestion adds a novel Layer 2 concept.

## [2026-04-27] ingest | Research sweep — event sourcing, actor model, observability, framework integration, skill stealing, value alignment
- **Note:** arXiv and Semantic Scholar APIs heavily rate-limited; used web knowledge + arXiv search results from previous runs
- **New entity pages created:**
  - skill-stealing-attack.md — Black-box skill extraction from proprietary LLM agents (Wang et al., 2604.21829)
  - value-alignment-structural.md — Pluralistic alignment and structural value delegation (LaCroix, 2604.20805)
  - pai-msc.md — Modular multi-agent system for ML theory research (Abdelmoneum et al., 2604.20622)
  - nemobot-games.md — Strategic AI gaming agents for interactive learning (Tan et al., 2604.21896)
- **New concept pages created:**
  - event-sourcing.md — Immutable event log for shared medium with full provenance, combines with CRDTs
  - actor-model-agents.md — Actor model mapping for LLM agents: encapsulated state, async messaging, supervision
  - agent-observability.md — Tracing, metrics, logging for membrane monitoring (OpenTelemetry integration)
  - framework-integration.md — Cross-framework compatibility strategies for MCP, A2A, LangGraph, AutoGen
- **Updated pages:**
  - agent-security-trust.md — Added skill stealing as new attack vector, updated sources
  - membrane-architecture.md — Added event sourcing, actor model, framework integration, observability layers
  - best-paths-forwards.md — Added Paths 10, 11, 12; revised to phased 16-week v3 recommendation sequence
  - index.md — Updated with all new pages
- **Wiki now has 46 pages** (29 entities, 17 concepts, 0 comparisons, 0 queries)
- **Key synthesis:** Event sourcing + CRDTs = full provenance + convergence. Actor model provides alternative message-passing paradigm. Observability is an operational necessity. Framework interoperability is the ecosystem strategy. Skill stealing adds a new attack vector to the security model. Value alignment adds depth to the trust model.

## [2026-04-27] ingest | Research sweep — collective intelligence, world modeling, token economics
- **arXiv search:** Found 3 highly relevant papers from 2026-04-24
- **Semantic Scholar:** Still rate-limited (429) from previous runs; relied on arXiv + web knowledge
- **Critical finding:** [[superminds-test]] (2604.22452) — 2M+ agents on MoltBook show NO collective intelligence; validates membrane thesis
- **Architectural reframe:** [[agentic-world-modeling]] (2604.22748) — 400+ paper survey with levels x laws taxonomy; membrane = social world model
- **Economic constraint:** [[agent-token-economics]] (2604.22750) — agentic tasks use 1000x tokens; input tokens dominate; validates gated permeability
- **New raw sources ingested:**
  - raw/articles/superminds-test-2604.22452.md
  - raw/articles/agentic-world-modeling-2604.22748.md
  - raw/articles/agent-token-consumption-2604.22750.md
- **New entity pages created:**
  - superminds-test.md — Empirical validation that scale alone doesn't produce collective intelligence
  - agentic-world-modeling.md — Levels x laws taxonomy; social regime = membrane domain
  - agent-token-economics.md — Token consumption patterns as design constraint
- **New concept pages created:**
  - collective-intelligence.md — The concept, current evidence, and membrane as solution
  - agentic-world-models.md — Membrane reframed as social world model with L1→L2→L3 maturity
- **Updated pages:**
  - membrane-architecture.md — Added world model framing, collective intelligence gap, token economics constraint
  - best-paths-forwards.md — Added Paths 13, 14, 15; upgraded to v4 recommendation with 3 new paths; restructured phases
  - index.md — Added all new pages, updated to 54 pages
- **Wiki now has 54 pages** (32 entities, 19 concepts, 0 comparisons, 0 queries)
- **Key synthesis:** Three papers from the same day converge on the membrane thesis: (1) Superminds Test proves the problem exists, (2) Agentic World Modeling provides an architectural reframing, (3) Token Economics provides a hard constraint. Together they strengthen the case for a structured, token-efficient, world-model-aware membrane.
- **ChromaDB reindexing pending** — will run after this log entry

## [2026-04-27] ingest | Research sweep — Failure Attribution subfield, 4 new entity pages, 1 new concept page
- **Major discovery:** Failure attribution is a rapidly emerging subfield (4+ papers since 2025) that directly validates the membrane's observability architecture
- **Semantic Scholar search** (after rate-limit recovery): Found Who&When (60 citations, foundational benchmark) plus CHIEF, DoVer, and SDBL frameworks
- **arXiv search**: Found TraceElephant (2604.22708) — full-trace attribution benchmark showing 76% improvement over partial observation
- **New raw sources ingested:**
  - raw/articles/traceelephant-2604.22708.md
  - raw/articles/whoandwhen-2505.00212.md
  - raw/articles/chief-framework-2602.23701.md
  - raw/articles/dover-2512.06749.md
- **New entity pages created:**
  - traceelephant.md — Full-trace failure attribution benchmark (76% accuracy improvement)
  - whoandwhen.md — Foundational dataset: 127 systems, even o1/R1 fail at attribution
  - chief-framework.md — Causal hierarchical failure attribution (counterfactual screening)
  - dover.md — Intervention-driven auto debugging (18-28% failures flipped to success)
- **New concept pages created:**
  - failure-attribution.md — Comprehensive synthesis of the subfield with membrane implications
- **Updated pages:**
  - agent-observability.md — Expanded with failure attribution subfield (4 papers), confidence upgraded to high
  - best-paths-forwards.md — Updated Path 16 with 4-paper validation; sources updated with new raw articles and entities; upgraded to v5 recommendation
  - index.md — Added 5 new pages (4 entities + 1 concept), reordered alphabetically
- **Wiki now has 62 pages** (37 entities, 23 concepts, 0 comparisons, 0 queries)
- **Key synthesis:** The failure attribution subfield has evolved through 4 phases (who caused it → full traces → causal graphs → active debugging), and the membrane's architecture maps directly onto all of them. Event sourcing provides full traces (TraceElephant), event references build causal graphs (CHIEF), and the membrane itself is the intervention surface (DoVer). This makes failure attribution not a bolt-on feature but a natural property of the membrane design.

## [2026-04-27] ingest | Research sweep — Index fix, abstract CoT, comprehensive audit
- **Critical lint fix:** Discovered 15 pages on disk that were NOT in index.md — all previous cron runs created pages but forgot to update the index
- **Root cause:** Previous runs created entity/concept pages in separate sessions without updating index.md afterward
- **Index repair:** Rewrote index.md with all 75 pages (47 entities + 28 concepts) organized alphabetically
- **New entity page created:**
  - abstract-chain-of-thought.md — Latent reasoning with continuous representations (Ramji et al., 2604.22709); foundation for efficient inter-agent communication
- **New raw source ingested:**
  - raw/articles/abstract-chain-of-thought-2604.22709.md
- **Updated pages:**
  - index.md — Complete rewrite: added 15 missing entries + 1 new entity; total 75 pages (was listing only 59)
  - best-paths-forwards.md — Added confidence/contested frontmatter fields
  - latent-communication.md concept — should reference abstract-chain-of-thought as new supporting evidence
- **arXiv search results:** Most recent papers (April 24) already captured in previous runs. Only genuinely new finding: abstract-chain-of-thought (2604.22709)
- **Semantic Scholar:** Still heavily rate-limited (429) — could not query. Previous runs already captured key papers.
- **Wiki now has 75 pages** (47 entities, 28 concepts, 0 comparisons, 0 queries) + 3 infrastructure files (SCHEMA.md, index.md, log.md)
- **ChromaDB:** 360 chunks across 64 previously indexed pages — reindexing after this entry
- **Key synthesis:** The wiki is now comprehensive with 21 ranked paths forward, covering the full stack from Layer -1 (governance) through Layer 3 (coordination), with identity/discovery as Layer 0 and 5 foundational prototypes. The index consistency fix reveals that previous sessions had a maintenance gap — all future sessions must update index.md atomically with page creation.

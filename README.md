# Synthetic Membrane

> A shared, permeable boundary for AI agents — enabling selective state sharing, emergent coordination, and collective intelligence.

## The Problem

Two million agents on MoltBook produced **zero collective intelligence**. No emergent reasoning. No information synthesis. Scale alone is insufficient — *structure* is what produces collective intelligence.

Current multi-agent frameworks (MCP, A2A, LangGraph, AutoGen) move *messages* between agents. What's missing is the **medium between agents** — a shared substrate where understanding accumulates, where agents can *sense* each other's state, and where coordination emerges without a central conductor.

## What It Is

A **synthetic membrane** — inspired by biological cell membranes — is a shared, semi-permeable layer between agents providing:

- **Layer 1: Permeability** — Field-level selective sharing, default-deny access control, cognitive digestion (remix)
- **Layer 2: Shared Medium** — Event-sourced memory with CRDT semantics, provenance, semantic query
- **Layer 3: Coordination** — Quorum-sensing swarm activation, dynamic grouping, task claiming

Plus **Layer 0** (discovery), **Layer -1** (governance), and an **immune layer** (adaptive defense).

```
   ┌──────────┐     ┌────────────────────────────────────────┐     ┌──────────┐
   │  AGENT A │ ◀─▶ │   LAYER 3: COORDINATION (swarm)        │ ◀─▶ │  AGENT B │
   │ ┌──────┐ │     │   quorum sensing · task claiming       │     │ ┌──────┐ │
   │ │Local │ │     ├────────────────────────────────────────┤     │ │Local │ │
   │ │ ctx  │ │     │   LAYER 2: SHARED MEDIUM (memory)      │     │ │ ctx  │ │
   │ └──────┘ │     │   event log · CRDTs · semantic store   │     │ └──────┘ │
   │   gate   │ ◀─▶ │   provenance · time-decay · replay     │ ◀─▶ │   gate   │
   │ channels │     ├────────────────────────────────────────┤     │ channels │
   │          │     │   LAYER 1: PERMEABILITY (protocol)     │     │          │
   │  remix   │ ◀─▶ │   field-level selectivity · SVAF       │ ◀─▶ │  remix   │
   │  digest  │     │   default-deny · cost-aware crossing   │     │  digest  │
   └──────────┘     └─────────────────────────────────────────┘     └──────────┘
```

## Architecture

Six layers from governance through coordination:

| Layer | Name | Purpose |
|-------|------|---------|
| **-1** | Governance | Circuit breakers, human override, value-conflict detection |
| **0** | Discovery | Behavioral indexing, identity verification, reputation |
| **1** | Permeability | Field-level selectivity, default-deny, cognitive digestion |
| **2** | Shared Medium | Event log, CRDTs, semantic query, provenance |
| **3** | Coordination | Quorum sensing, task claiming, swarm formation |
| **∞** | Immune | Anomaly detection, threat gossip, adaptive defense |

## MVP Reference Implementation

A working MCP server exposing 14 tools:

| Tool | Description |
|------|-------------|
| `register_agent` | Register with name and capabilities |
| `expose` | Share state with permeability tier |
| `query` | Query shared state (glob patterns, permeability-checked) |
| `subscribe` | Subscribe to state change patterns |
| `broadcast` | Broadcast to all registered agents |
| `swarm_create` | Create quorum-sensing swarm |
| `swarm_join` | Join swarm (capability-checked) |
| `set_trust` | Set trust score between agents |
| `stats` | Store statistics |

### Quick Start

```bash
cd mvp
pip install -e .
membrane-server  # Runs as MCP server over stdio
```

### Connect from an MCP Client

```python
# The membrane is an MCP server — any MCP client connects:
{
    "mcpServers": {
        "membrane": {
            "command": "python",
            "args": ["-m", "membrane.server"]
        }
    }
}
```

### Run Tests

```bash
cd mvp
pip install pytest pytest-asyncio
PYTHONPATH=src pytest tests/ -v
# 41/41 passing — coordination, swarm lifecycle, event replay, token budget
```

### Run the Demo

A self-contained demo lives in [`mvp/demo/`](mvp/demo/). Five agents
(Researcher, Writer, Editor, Reviewer, Orchestrator) collaborate on a
research brief through the membrane, exercising every public capability
of the MVP — registration, three permeability tiers, trust, queries,
subscriptions, broadcasts, and quorum-sensing swarms.

```bash
cd mvp
pip install -r demo/requirements.txt
python -m demo
```

The demo prints a richly-formatted terminal trace and emits five
dark-themed SVGs into [`mvp/demo/output/`](mvp/demo/output/):

| File | What it shows |
|------|---------------|
| [`architecture.svg`](mvp/demo/output/architecture.svg)     | Six-layer membrane between two agents, with arrows traversing each layer |
| [`state_graph.svg`](mvp/demo/output/state_graph.svg)       | Bipartite agents ↔ exposed entries graph, edges colored by permeability tier |
| [`swarm_timeline.svg`](mvp/demo/output/swarm_timeline.svg) | Quorum-sensing swarm lifecycle plotted against the event log sequence |
| [`benchmark.svg`](mvp/demo/output/benchmark.svg)           | Baseline (point-to-point) vs. membrane on three metrics — small multiples |
| [`scaling.svg`](mvp/demo/output/scaling.svg)               | Token cost vs. number of agents — baseline grows O(N²·F), membrane O(N·F) |

#### Headline benchmark (3 agents, 5 facts each)

|                  | baseline | membrane | reduction |
|------------------|---------:|---------:|----------:|
| messages         |       60 |       18 |   −70.0%  |
| tokens           |    7,440 |    4,320 |   −41.9%  |
| consensus steps  |        6 |        2 |   −66.7%  |

The gap widens with scale: at 20 agents the token reduction reaches
**−72.2%**.

## Position Paper

A full position paper is available in [paper/paper.md](paper/paper.md) covering:

- The thesis: structured communication as prerequisite for collective intelligence
- Six-layer architecture with ASCII diagram
- Ten empirical findings from recent research (Superminds Test, MMP, token economics, world models)
- Eighteen ranked implementation paths
- Sixteen-week phased roadmap
- Falsification criteria

## Blog Post

An accessible version for the broader AI community: [axjns.dev/research](https://axjns.dev/research) | [paper/blog-post.md](paper/blog-post.md)

## Research Wiki

The [wiki/](wiki/) directory contains 80+ interlinked markdown pages — entity pages, concept analyses, prototype code, and raw research articles. Open the wiki directory in [Obsidian](https://obsidian.md/) for the full knowledge graph experience.

## Key References

- **Superminds Test** — 2M agents, zero collective intelligence [arXiv:2604.22452](https://arxiv.org/abs/2604.22452)
- **Mesh Memory Protocol** — CAT7/SVAF/lineage/remix primitives [arXiv:2604.19540](https://arxiv.org/abs/2604.19540)
- **Token Economics** — 1000× overhead in agentic tasks [arXiv:2604.22750](https://arxiv.org/abs/2604.22750)
- **Agentic World Modeling** — Levels × laws taxonomy [arXiv:2604.22748](https://arxiv.org/abs/2604.22748)
- **Gated Coordination** — Default-deny outperforms open [arXiv:2604.18975](https://arxiv.org/abs/2604.18975)

## License

MIT

## Contributors

Want to help? The [best-paths-forwards wiki page](wiki/concepts/best-paths-forwards.md) lists 18 ranked implementation paths with feasibility/impact/novelty scores. Pick one and go.

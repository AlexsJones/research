# Research — Multi-Agent AI Coordination

> Shared, permeable boundaries for AI agents — enabling selective state sharing, emergent coordination, and collective intelligence.

## Overview

This repo documents research into **structured communication** as the prerequisite for collective intelligence in multi-agent systems. The core thesis: putting two million agents in the same room produces zero collective intelligence — not because the agents are weak, but because there is no *structure* between them.

The **Synthetic Membrane** is our proposed solution: a shared, semi-permeable layer between agents, inspired by biological cell membranes, providing selective state sharing, event-sourced memory with CRDT semantics, and quorum-sensing swarm activation.

## Sympozium

This research powers [**Sympozium**](https://github.com/sympozium-ai/sympozium) — a production-ready MCP server implementing the membrane architecture. Sympozium exposes 14 tools for agent registration, state exposure, semantic query, subscription, broadcast, and quorum-sensing swarm formation.

## Directory Structure

```
research/
├── papers/              # Position papers and research drafts
│   ├── synthetic-membrane.md        # Original position paper
│   └── 0001-synthetic-membrane-coordination-layer.md  # Draft paper
├── articles/            # Blog posts and public-facing articles
│   ├── blog-post.md                     # Accessible intro to synthetic membrane
│   └── 0001-sticky-note-problem.md      # Draft: "The Sticky-Note Problem"
├── corpus/              # Research corpus — deep-dive analyses
│   └── agent-coordination/
│       ├── corpus/           # Research articles (state of coordination, etc.)
│       ├── analysis/         # Synthesis and meta-analysis
│       ├── RESEARCH-BRIEF.md # Project brief
│       └── CLAUDE.md         # Agent instructions
├── wiki/              # Knowledge base — 80+ interlinked pages
│   ├── concepts/        # Concept analyses
│   ├── entities/        # Entity pages (protocols, frameworks)
│   ├── raw/             # Raw research notes
│   └── scripts/         # Wiki utilities
├── mvp/               # Reference implementation — MCP server
│   ├── src/             # Core package
│   ├── tests/           # 41 passing tests
│   └── demo/            # Self-contained demo with SVG output
├── LICENSE
└── README.md
```

## Getting Started

### Read the Papers

- **[Position Paper](papers/synthetic-membrane.md)** — Full thesis: structured communication as prerequisite for collective intelligence, six-layer architecture, implementation paths, and roadmap.
- **[Draft Paper](papers/0001-synthetic-membrane-coordination-layer.md)** — Extended draft on the coordination layer.
- **[Blog Post](articles/blog-post.md)** — Accessible introduction for the broader AI community.

### Run the MVP

```bash
cd mvp
pip install -e .
membrane-server  # Runs as MCP server over stdio
```

### Connect from an MCP Client

```python
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

### Explore the Wiki

The [wiki/](wiki/) directory contains 80+ interlinked markdown pages — entity pages, concept analyses, prototype code, and raw research. Open the wiki directory in [Obsidian](https://obsidian.md/) for the full knowledge graph experience.

## Key References

- **Superminds Test** — 2M agents, zero collective intelligence [arXiv:2604.22452](https://arxiv.org/abs/2604.22452)
- **Mesh Memory Protocol** — CAT7/SVAF/lineage/remix primitives [arXiv:2604.19540](https://arxiv.org/abs/2604.19540)
- **Token Economics** — 1000× overhead in agentic tasks [arXiv:2604.22750](https://arxiv.org/abs/2604.22750)
- **Agentic World Modeling** — Levels × laws taxonomy [arXiv:2604.22748](https://arxiv.org/abs/2604.22748)
- **Gated Coordination** — Default-deny outperforms open [arXiv:2604.18975](https://arxiv.org/abs/2604.18975)

## License

MIT

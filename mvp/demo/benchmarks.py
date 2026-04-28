"""
Benchmarks: baseline (point-to-point messaging) vs. Synthetic Membrane.

Setup
─────
Three agents need to share `n_facts` pieces of state with each other and
agree on a final result.

Baseline (no membrane)
  Each agent broadcasts every fact to every other agent. Each pair must
  exchange every fact and an explicit "ack" before they can proceed.
  Cost grows ~ O(agents² · facts).

Membrane
  Each agent exposes facts once. Other agents query a glob pattern and
  the membrane enforces permeability gating. No per-pair acks needed —
  the shared medium is the consensus surface.

Metrics
  messages         — wire events sent across the network
  tokens           — sum of (per-message header) + (payload tokens)
  consensus_steps  — round-trips before all agents have all facts

We render the comparison as a grouped bar chart SVG.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# Allow `python -m demo` from mvp/ without an editable install.
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from membrane.permeability import PermeabilityEngine
from membrane.store import MembraneStore

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ─── Theme (mirrors visualize.py) ───────────────────────────────────────
BG = "#0d1117"
FG = "#e6edf3"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#d29922"
RED = "#f85149"
MUTED = "#6e7681"
PANEL = "#161b22"
BORDER = "#30363d"

FONT = (
    "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
    "'Liberation Mono', 'Courier New', monospace"
)


# ─── Cost model ─────────────────────────────────────────────────────────
# Calibrated for LLM-driven agents. Every message handled by an agent
# pays an envelope cost — system prompt, tool descriptions, role tags,
# and the routing wrapper that the model has to re-read every turn. The
# membrane wins by amortising envelopes across bundled query responses.

ENVELOPE_TOKENS = 90
PAYLOAD_TOKENS = 60
ACK_TOKENS = 8


# ─── Models ─────────────────────────────────────────────────────────────

@dataclass
class BenchResult:
    label: str
    messages: int = 0
    tokens: int = 0
    consensus_steps: int = 0
    notes: list[str] = field(default_factory=list)


@dataclass
class Comparison:
    n_agents: int
    n_facts: int
    baseline: BenchResult
    membrane: BenchResult


# ─── Baseline simulation ────────────────────────────────────────────────

def run_baseline(n_agents: int, n_facts_each: int) -> BenchResult:
    """Each agent sends every fact to every other agent + one ack each."""
    r = BenchResult(label="baseline (point-to-point)")

    pairs = n_agents * (n_agents - 1)  # directed pairs

    # Each agent sends n_facts_each messages to each peer
    fact_msgs = pairs * n_facts_each
    fact_tokens = fact_msgs * (ENVELOPE_TOKENS + PAYLOAD_TOKENS)

    # Each fact triggers an ack reply
    ack_msgs = fact_msgs
    ack_tokens = ack_msgs * (ENVELOPE_TOKENS + ACK_TOKENS)

    # Consensus: each fact requires a round-trip across all pairs in series,
    # then a final "ready" round to confirm. Approximated as n_facts_each + 1.
    r.messages = fact_msgs + ack_msgs
    r.tokens = fact_tokens + ack_tokens
    r.consensus_steps = n_facts_each + 1
    r.notes = [
        f"{n_agents} agents · {n_facts_each} facts each",
        f"{pairs} directed pairs × {n_facts_each} facts × (send+ack)",
    ]
    return r


# ─── Membrane simulation ────────────────────────────────────────────────

def run_membrane(n_agents: int, n_facts_each: int) -> BenchResult:
    """Run the equivalent workflow through a real MembraneStore."""

    store = MembraneStore()
    perm = PermeabilityEngine()
    agent_ids = [f"agent_{i}" for i in range(n_agents)]

    for aid in agent_ids:
        store.register_agent(aid, aid, ["share"])
        perm.set_token_budget(aid, 1_000_000)

    r = BenchResult(label="membrane (shared medium)")

    # Each agent exposes its facts ONCE — payload only, no per-recipient envelope.
    for aid in agent_ids:
        for k in range(n_facts_each):
            store.expose(aid, f"facts.{aid}.{k}", "x" * 32, "public")
            r.messages += 1
            r.tokens += ENVELOPE_TOKENS + PAYLOAD_TOKENS

    # Each agent queries the shared medium ONCE for the full set. The
    # querier pays one envelope (one LLM turn) plus payload tokens for
    # facts it does not already own — its own facts are not re-counted.
    for aid in agent_ids:
        results = store.query(aid, "facts.*")
        new_facts = [e for e in results if e.agent_id != aid]
        r.messages += 1
        r.tokens += ENVELOPE_TOKENS + len(new_facts) * PAYLOAD_TOKENS

    # Consensus: 2 steps — expose round, query round.
    r.consensus_steps = 2
    r.notes = [
        f"{n_agents} agents · {n_facts_each} facts each",
        f"{n_agents * n_facts_each} exposes + {n_agents} queries",
    ]
    return r


# ─── Driver ─────────────────────────────────────────────────────────────

def compare(n_agents: int = 3, n_facts: int = 5) -> Comparison:
    return Comparison(
        n_agents=n_agents,
        n_facts=n_facts,
        baseline=run_baseline(n_agents, n_facts),
        membrane=run_membrane(n_agents, n_facts),
    )


def print_summary(console: Console, c: Comparison) -> None:
    title = Text(
        f"  Baseline vs. Membrane  ·  {c.n_agents} agents  ·  "
        f"{c.n_facts} facts each",
        style=f"bold {ACCENT}",
    )

    t = Table(show_header=True, header_style=f"bold {ACCENT}",
              border_style=MUTED, padding=(0, 2))
    t.add_column("metric", style=FG)
    t.add_column("baseline", justify="right", style=ORANGE)
    t.add_column("membrane", justify="right", style=GREEN)
    t.add_column("reduction", justify="right", style=ACCENT)

    def reduction(b: int, m: int) -> str:
        if b == 0:
            return "—"
        ratio = (b - m) / b
        return f"{ratio*100:5.1f}%  ({b}→{m})"

    t.add_row("messages",
              f"{c.baseline.messages:,}",
              f"{c.membrane.messages:,}",
              reduction(c.baseline.messages, c.membrane.messages))
    t.add_row("token-equivalent cost",
              f"{c.baseline.tokens:,}",
              f"{c.membrane.tokens:,}",
              reduction(c.baseline.tokens, c.membrane.tokens))
    t.add_row("consensus steps",
              f"{c.baseline.consensus_steps}",
              f"{c.membrane.consensus_steps}",
              reduction(c.baseline.consensus_steps, c.membrane.consensus_steps))

    console.print()
    console.print(Panel(t, title=title, border_style=ACCENT, padding=(1, 2)))


# ─── SVG renderer ───────────────────────────────────────────────────────

def render_benchmark_svg(c: Comparison) -> str:
    """Small-multiples chart: one linear-scaled panel per metric."""
    width, height = 1200, 540

    metrics = [
        ("messages",        "wire messages",        c.baseline.messages,
         c.membrane.messages),
        ("tokens",          "token-equivalent",     c.baseline.tokens,
         c.membrane.tokens),
        ("consensus steps", "rounds to converge",   c.baseline.consensus_steps,
         c.membrane.consensus_steps),
    ]

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Baseline vs Membrane benchmark" '
        f'font-family="{FONT}">\n'
        f'  <title>Baseline vs Membrane benchmark</title>\n'
        f'  <rect width="{width}" height="{height}" fill="{BG}"/>\n'
    )

    out.append(
        f'  <text x="32" y="44" fill="{FG}" font-size="22" font-weight="700">'
        f'Baseline vs. Synthetic Membrane</text>\n'
        f'  <text x="32" y="68" fill="{MUTED}" font-size="13">'
        f'{c.n_agents} agents · {c.n_facts} facts each · '
        f'lower is better — each metric uses its own linear scale</text>\n'
    )

    # Layout: three side-by-side panels
    panel_top = 110
    panel_h = 320
    margin = 40
    panel_w = (width - 2 * margin - 2 * margin) / 3
    bar_w = 56
    pair_gap = 32

    for i, (key, sub, base, mem) in enumerate(metrics):
        px = margin + i * (panel_w + margin)
        py = panel_top
        # Panel frame
        out.append(
            f'  <rect x="{px}" y="{py}" width="{panel_w}" height="{panel_h}" '
            f'    rx="8" fill="{PANEL}" stroke="{BORDER}" stroke-width="1"/>\n'
            f'  <text x="{px + panel_w/2}" y="{py + 26}" fill="{FG}" '
            f'    font-size="14" font-weight="700" text-anchor="middle">{key}</text>\n'
            f'  <text x="{px + panel_w/2}" y="{py + 46}" fill="{MUTED}" '
            f'    font-size="11" text-anchor="middle">{sub}</text>\n'
        )

        # Bars area inside the panel
        bars_top = py + 70
        bars_bot = py + panel_h - 70
        usable_h = bars_bot - bars_top

        denom = max(base, mem, 1)
        b_h = max(2, usable_h * (base / denom))
        m_h = max(2, usable_h * (mem / denom))

        cx = px + panel_w / 2
        bx = cx - bar_w - pair_gap / 2
        mx = cx + pair_gap / 2

        # Baseline bar
        out.append(
            f'  <rect x="{bx}" y="{bars_bot - b_h}" width="{bar_w}" height="{b_h}" '
            f'    rx="3" fill="{ORANGE}" fill-opacity="0.92"/>\n'
            f'  <text x="{bx + bar_w/2}" y="{bars_bot - b_h - 8}" fill="{ORANGE}" '
            f'    font-size="13" text-anchor="middle" font-weight="700">{base:,}</text>\n'
            f'  <text x="{bx + bar_w/2}" y="{bars_bot + 18}" fill="{MUTED}" '
            f'    font-size="10" text-anchor="middle">baseline</text>\n'
        )

        # Membrane bar
        out.append(
            f'  <rect x="{mx}" y="{bars_bot - m_h}" width="{bar_w}" height="{m_h}" '
            f'    rx="3" fill="{GREEN}" fill-opacity="0.92"/>\n'
            f'  <text x="{mx + bar_w/2}" y="{bars_bot - m_h - 8}" fill="{GREEN}" '
            f'    font-size="13" text-anchor="middle" font-weight="700">{mem:,}</text>\n'
            f'  <text x="{mx + bar_w/2}" y="{bars_bot + 18}" fill="{MUTED}" '
            f'    font-size="10" text-anchor="middle">membrane</text>\n'
        )

        # Reduction badge centered below
        if base > 0:
            ratio = (base - mem) / base * 100
            out.append(
                f'  <text x="{cx}" y="{py + panel_h - 18}" fill="{ACCENT}" '
                f'    font-size="14" text-anchor="middle" font-weight="700">'
                f'−{ratio:.1f}%</text>\n'
            )

    # Footer
    legend_y = height - 32
    out.append(
        f'  <rect x="{margin}" y="{legend_y - 14}" width="14" height="14" rx="3" '
        f'    fill="{ORANGE}"/>\n'
        f'  <text x="{margin + 20}" y="{legend_y - 2}" fill="{FG}" font-size="12">'
        f'baseline · point-to-point messaging</text>\n'

        f'  <rect x="{margin + 320}" y="{legend_y - 14}" width="14" height="14" rx="3" '
        f'    fill="{GREEN}"/>\n'
        f'  <text x="{margin + 340}" y="{legend_y - 2}" fill="{FG}" font-size="12">'
        f'membrane · shared medium</text>\n'

        f'  <text x="{width - margin}" y="{legend_y - 2}" fill="{MUTED}" '
        f'    font-size="11" text-anchor="end">'
        f'envelope={ENVELOPE_TOKENS}t · payload={PAYLOAD_TOKENS}t · '
        f'ack={ACK_TOKENS}t</text>\n'
    )

    out.append("</svg>\n")
    return "".join(out)


def generate_svg(comparison: Comparison, output_dir: Path | str) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "benchmark.svg"
    path.write_text(render_benchmark_svg(comparison))
    return path


# ─── Scaling sweep ──────────────────────────────────────────────────────

def render_scaling_svg(
    sweep: list[Comparison],
    metric: str = "tokens",
) -> str:
    """Plot baseline vs membrane vs n_agents for a chosen metric."""
    width, height = 1200, 540

    pull = {
        "tokens": lambda c: (c.baseline.tokens, c.membrane.tokens),
        "messages": lambda c: (c.baseline.messages, c.membrane.messages),
        "consensus": lambda c: (c.baseline.consensus_steps,
                                c.membrane.consensus_steps),
    }
    extract = pull[metric]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Membrane scaling sweep" '
        f'font-family="{FONT}">\n'
        f'  <title>Synthetic Membrane scaling sweep</title>\n'
        f'  <rect width="{width}" height="{height}" fill="{BG}"/>\n'

        f'  <text x="32" y="44" fill="{FG}" font-size="22" font-weight="700">'
        f'Scaling — {metric} vs. number of agents</text>\n'
        f'  <text x="32" y="68" fill="{MUTED}" font-size="13">'
        f'fixed: {sweep[0].n_facts} facts per agent · baseline grows '
        f'O(N²·F) · membrane grows O(N·F)</text>\n'
    ]

    plot_x = 90
    plot_y = 110
    plot_w = width - plot_x - 60
    plot_h = height - plot_y - 80

    out.append(
        f'  <rect x="{plot_x}" y="{plot_y}" width="{plot_w}" height="{plot_h}" '
        f'    fill="{PANEL}" stroke="{BORDER}" stroke-width="1"/>\n'
    )

    n_vals = [c.n_agents for c in sweep]
    base_vals = [extract(c)[0] for c in sweep]
    mem_vals = [extract(c)[1] for c in sweep]
    ymax = max(base_vals + mem_vals + [1]) * 1.05
    xmin, xmax = min(n_vals), max(n_vals)

    def x_of(n: int) -> float:
        if xmax == xmin:
            return plot_x + plot_w / 2
        return plot_x + (n - xmin) / (xmax - xmin) * plot_w

    def y_of(v: float) -> float:
        return plot_y + plot_h - (v / ymax) * plot_h

    # Y gridlines
    for i in range(1, 5):
        v = ymax * i / 4
        gy = y_of(v)
        out.append(
            f'  <line x1="{plot_x}" y1="{gy}" x2="{plot_x + plot_w}" y2="{gy}" '
            f'    stroke="{BORDER}" stroke-opacity="0.6" stroke-dasharray="2 6"/>\n'
            f'  <text x="{plot_x - 8}" y="{gy + 4}" fill="{MUTED}" font-size="10" '
            f'    text-anchor="end">{int(v):,}</text>\n'
        )

    # X tick labels
    for n in n_vals:
        xx = x_of(n)
        out.append(
            f'  <line x1="{xx}" y1="{plot_y + plot_h}" x2="{xx}" y2="{plot_y + plot_h + 4}" '
            f'    stroke="{MUTED}" stroke-width="1"/>\n'
            f'  <text x="{xx}" y="{plot_y + plot_h + 18}" fill="{MUTED}" '
            f'    font-size="11" text-anchor="middle">{n}</text>\n'
        )
    out.append(
        f'  <text x="{plot_x + plot_w/2}" y="{plot_y + plot_h + 42}" fill="{FG}" '
        f'    font-size="12" text-anchor="middle">number of agents</text>\n'
    )

    # Lines
    def polyline(values: list[int], color: str, label: str) -> None:
        pts = " ".join(f"{x_of(n):.1f},{y_of(v):.1f}"
                       for n, v in zip(n_vals, values))
        out.append(
            f'  <polyline points="{pts}" fill="none" stroke="{color}" '
            f'    stroke-width="2.4"/>\n'
        )
        for n, v in zip(n_vals, values):
            out.append(
                f'  <circle cx="{x_of(n):.1f}" cy="{y_of(v):.1f}" '
                f'    r="4" fill="{color}"/>\n'
            )

    polyline(base_vals, ORANGE, "baseline")
    polyline(mem_vals, GREEN, "membrane")

    # Legend
    legend_y = 120
    out.append(
        f'  <rect x="{plot_x + 16}" y="{legend_y}" width="220" height="60" '
        f'    rx="6" fill="{BG}" fill-opacity="0.65" stroke="{BORDER}"/>\n'

        f'  <line x1="{plot_x + 28}" y1="{legend_y + 22}" x2="{plot_x + 56}" '
        f'    y2="{legend_y + 22}" stroke="{ORANGE}" stroke-width="2.4"/>\n'
        f'  <circle cx="{plot_x + 42}" cy="{legend_y + 22}" r="4" fill="{ORANGE}"/>\n'
        f'  <text x="{plot_x + 64}" y="{legend_y + 26}" fill="{FG}" '
        f'    font-size="12">baseline (point-to-point)</text>\n'

        f'  <line x1="{plot_x + 28}" y1="{legend_y + 44}" x2="{plot_x + 56}" '
        f'    y2="{legend_y + 44}" stroke="{GREEN}" stroke-width="2.4"/>\n'
        f'  <circle cx="{plot_x + 42}" cy="{legend_y + 44}" r="4" fill="{GREEN}"/>\n'
        f'  <text x="{plot_x + 64}" y="{legend_y + 48}" fill="{FG}" '
        f'    font-size="12">membrane (shared medium)</text>\n'
    )

    out.append("</svg>\n")
    return "".join(out)


def generate_scaling_svg(output_dir: Path | str,
                         agents: Iterable[int] = (3, 5, 8, 12, 20),
                         n_facts: int = 5,
                         metric: str = "tokens") -> tuple[Path, list[Comparison]]:
    sweep = [compare(n, n_facts) for n in agents]
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "scaling.svg"
    path.write_text(render_scaling_svg(sweep, metric=metric))
    return path, sweep


# ─── Entry point ────────────────────────────────────────────────────────

def run_and_render(
    console: Console | None = None,
    output_dir: Path | str | None = None,
    n_agents: int = 3,
    n_facts: int = 5,
) -> Comparison:
    console = console or Console()
    c = compare(n_agents=n_agents, n_facts=n_facts)
    print_summary(console, c)
    if output_dir is not None:
        path = generate_svg(c, output_dir)
        console.print(Text(f"  benchmark chart  → {path}",
                           style=f"{MUTED}"))
        scaling_path, sweep = generate_scaling_svg(output_dir,
                                                   n_facts=n_facts)
        console.print(Text(f"  scaling chart    → {scaling_path}",
                           style=f"{MUTED}"))
        # Show the sweep table too
        st = Table(show_header=True, header_style=f"bold {ACCENT}",
                   border_style=MUTED, padding=(0, 2))
        st.add_column("agents", justify="right", style=FG)
        st.add_column("baseline tokens", justify="right", style=ORANGE)
        st.add_column("membrane tokens", justify="right", style=GREEN)
        st.add_column("reduction", justify="right", style=ACCENT)
        for cmp in sweep:
            b = cmp.baseline.tokens
            m = cmp.membrane.tokens
            ratio = (b - m) / b * 100 if b else 0
            st.add_row(str(cmp.n_agents), f"{b:,}", f"{m:,}",
                       f"{ratio:5.1f}%")
        console.print()
        console.print(Panel(
            st,
            title=Text(f"  Scaling sweep — N agents · {n_facts} facts each",
                       style=f"bold {ACCENT}"),
            border_style=ACCENT, padding=(1, 2),
        ))
    return c


if __name__ == "__main__":
    run_and_render(output_dir=Path(__file__).parent / "output")

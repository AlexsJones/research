"""
Synthetic Membrane MVP demo entry point.

Run from the mvp/ directory:

    python -m demo

Produces:
  - a richly-formatted terminal trace of the five-agent simulation
  - benchmark tables (point-to-point vs. membrane) with a scaling sweep
  - four SVGs in demo/output/:
      architecture.svg  state_graph.svg  swarm_timeline.svg  scaling.svg
      benchmark.svg
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from demo.agent_simulation import run as run_simulation
from demo.benchmarks import run_and_render as run_benchmarks
from demo.visualize import generate_all as generate_svgs


ACCENT = "#58a6ff"
GREEN = "#3fb950"
MUTED = "#6e7681"
TEXT = "#e6edf3"


def _section(console: Console, label: str, blurb: str) -> None:
    console.print()
    console.print(Rule(
        title=Text(f"  {label}  ", style=f"bold {TEXT} on {ACCENT}"),
        style=ACCENT,
    ))
    console.print(Text(f"  {blurb}", style=f"italic {MUTED}"))


def main() -> int:
    console = Console()
    output_dir = Path(__file__).parent / "output"

    # 1. Simulation
    _section(console, "I.  Five-agent coordination simulation",
             "registration · permeability · trust · subscriptions · "
             "swarms · broadcasts")
    sim = run_simulation(console=console)

    # 2. Visualizations
    _section(console, "II. Render diagrams",
             "three SVGs derived from the live event log")
    paths = generate_svgs(sim.store, sim.permeability, sim.swarm, output_dir)
    for name, p in paths.items():
        console.print(Text(f"  ▸  {name:<16} → {p}", style=MUTED))

    # 3. Benchmarks
    _section(console, "III. Baseline vs. membrane benchmark",
             "point-to-point messaging vs. shared medium · "
             "tokens, messages, consensus steps")
    run_benchmarks(console=console, output_dir=output_dir)

    # 4. Done
    console.print()
    console.print(Panel(
        Text(
            f"  All outputs written to: {output_dir}\n"
            f"  Open the SVGs in any browser to inspect — they are dark-themed "
            f"and self-contained.",
            style=TEXT,
        ),
        title=Text("demo complete", style=f"bold {GREEN}"),
        border_style=GREEN,
        padding=(1, 2),
    ))
    console.print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

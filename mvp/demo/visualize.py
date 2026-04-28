"""
SVG visualizers for the Synthetic Membrane demo.

Three diagrams, each a self-contained SVG file with a dark theme:

  architecture.svg    — six-layer membrane between two agents
  state_graph.svg     — agents on the left, exposed entries on the right,
                        edges colored by permeability tier
  swarm_timeline.svg  — quorum-sensing swarm activation timeline

Pure-stdlib SVG generation — no matplotlib, no graphviz — so the demo
runs anywhere Python runs.
"""

from __future__ import annotations

import html
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# Allow `python -m demo` from mvp/ without an editable install.
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from membrane.models import EventType, PermeabilityLevel
from membrane.permeability import PermeabilityEngine
from membrane.store import MembraneStore
from membrane.swarm import SwarmEngine


# ─── Theme ──────────────────────────────────────────────────────────────
BG = "#0d1117"
FG = "#e6edf3"
ACCENT = "#58a6ff"
GREEN = "#3fb950"
ORANGE = "#d29922"
RED = "#f85149"
MUTED = "#6e7681"
PANEL = "#161b22"
BORDER = "#30363d"

PERM_COLOR = {
    PermeabilityLevel.PUBLIC: GREEN,
    PermeabilityLevel.TRUSTED: ORANGE,
    PermeabilityLevel.PRIVATE: RED,
}

FONT = (
    "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
    "'Liberation Mono', 'Courier New', monospace"
)


# ─── Primitives ─────────────────────────────────────────────────────────

def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def _svg_open(width: int, height: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="{_esc(title)}" font-family="{FONT}">\n'
        f'  <title>{_esc(title)}</title>\n'
        f'  <rect width="{width}" height="{height}" fill="{BG}"/>\n'
        f'  <defs>\n'
        f'    <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" '
        f'      markerWidth="8" markerHeight="8" orient="auto-start-reverse">\n'
        f'      <path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/>\n'
        f'    </marker>\n'
        f'    <marker id="arrow-muted" viewBox="0 0 10 10" refX="10" refY="5" '
        f'      markerWidth="6" markerHeight="6" orient="auto-start-reverse">\n'
        f'      <path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/>\n'
        f'    </marker>\n'
        f'  </defs>\n'
    )


def _title_bar(width: int, title: str, subtitle: str) -> str:
    return (
        f'  <text x="32" y="44" fill="{FG}" font-size="22" font-weight="700">'
        f'{_esc(title)}</text>\n'
        f'  <text x="32" y="68" fill="{MUTED}" font-size="13">'
        f'{_esc(subtitle)}</text>\n'
    )


def _close() -> str:
    return "</svg>\n"


# ─── 1. Architecture ────────────────────────────────────────────────────

@dataclass
class _Layer:
    index: str
    name: str
    desc: str
    color: str


_LAYERS = [
    _Layer("∞",  "Immune",        "anomaly detection · threat gossip · adaptive defense", RED),
    _Layer("3",  "Coordination",  "quorum sensing · task claiming · swarm formation",     GREEN),
    _Layer("2",  "Shared Medium", "event log · CRDTs · semantic query · provenance",      ACCENT),
    _Layer("1",  "Permeability",  "field-level selectivity · default-deny · cost-aware",  ORANGE),
    _Layer("0",  "Discovery",     "behavioural indexing · identity · reputation",         "#a371f7"),
    _Layer("-1", "Governance",    "circuit breakers · human override · value conflicts",  MUTED),
]


def _agent_box(x: int, y: int, name: str, w: int = 130, h: int = 320) -> str:
    return (
        f'  <g>\n'
        f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" '
        f'      rx="10" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>\n'
        f'    <text x="{x + w/2}" y="{y + 24}" fill="{ACCENT}" '
        f'      font-size="13" font-weight="700" text-anchor="middle">{_esc(name)}</text>\n'

        f'    <rect x="{x + 14}" y="{y + 44}" width="{w - 28}" height="78" '
        f'      rx="6" fill="{BG}" stroke="{BORDER}"/>\n'
        f'    <text x="{x + w/2}" y="{y + 70}" fill="{FG}" '
        f'      font-size="11" text-anchor="middle">local</text>\n'
        f'    <text x="{x + w/2}" y="{y + 88}" fill="{FG}" '
        f'      font-size="11" text-anchor="middle">context</text>\n'
        f'    <text x="{x + w/2}" y="{y + 106}" fill="{MUTED}" '
        f'      font-size="9" text-anchor="middle">model state</text>\n'

        f'    <rect x="{x + 14}" y="{y + 134}" width="{w - 28}" height="48" '
        f'      rx="6" fill="{BG}" stroke="{ORANGE}"/>\n'
        f'    <text x="{x + w/2}" y="{y + 153}" fill="{ORANGE}" '
        f'      font-size="11" text-anchor="middle" font-weight="700">gate</text>\n'
        f'    <text x="{x + w/2}" y="{y + 169}" fill="{MUTED}" '
        f'      font-size="9" text-anchor="middle">tier · trust · cost</text>\n'

        f'    <rect x="{x + 14}" y="{y + 194}" width="{w - 28}" height="48" '
        f'      rx="6" fill="{BG}" stroke="{ACCENT}"/>\n'
        f'    <text x="{x + w/2}" y="{y + 213}" fill="{ACCENT}" '
        f'      font-size="11" text-anchor="middle" font-weight="700">channels</text>\n'
        f'    <text x="{x + w/2}" y="{y + 229}" fill="{MUTED}" '
        f'      font-size="9" text-anchor="middle">expose · query</text>\n'

        f'    <rect x="{x + 14}" y="{y + 254}" width="{w - 28}" height="48" '
        f'      rx="6" fill="{BG}" stroke="{GREEN}"/>\n'
        f'    <text x="{x + w/2}" y="{y + 273}" fill="{GREEN}" '
        f'      font-size="11" text-anchor="middle" font-weight="700">remix</text>\n'
        f'    <text x="{x + w/2}" y="{y + 289}" fill="{MUTED}" '
        f'      font-size="9" text-anchor="middle">cognitive digest</text>\n'
        f'  </g>\n'
    )


def render_architecture() -> str:
    width, height = 1200, 720
    out = [_svg_open(width, height,
                     "Synthetic Membrane — six-layer architecture")]
    out.append(_title_bar(
        width,
        "Synthetic Membrane — architecture",
        "six layers between two agents · default-deny · event-sourced · "
        "quorum-coordinated",
    ))

    # Membrane stack
    stack_x = 230
    stack_y = 110
    stack_w = width - 2 * stack_x
    band_h = 76
    gap = 6

    for i, layer in enumerate(_LAYERS):
        y = stack_y + i * (band_h + gap)
        # band
        out.append(
            f'  <rect x="{stack_x}" y="{y}" width="{stack_w}" height="{band_h}" '
            f'    rx="8" fill="{PANEL}" stroke="{layer.color}" stroke-width="1.4"/>\n'
        )
        # left index pill
        out.append(
            f'  <rect x="{stack_x + 12}" y="{y + 12}" width="44" height="{band_h - 24}" '
            f'    rx="6" fill="{BG}" stroke="{layer.color}"/>\n'
            f'  <text x="{stack_x + 34}" y="{y + band_h/2 + 5}" fill="{layer.color}" '
            f'    font-size="14" font-weight="700" text-anchor="middle">{_esc(layer.index)}</text>\n'
        )
        # name + desc
        out.append(
            f'  <text x="{stack_x + 76}" y="{y + 30}" fill="{FG}" '
            f'    font-size="15" font-weight="700">{_esc(layer.name)}</text>\n'
            f'  <text x="{stack_x + 76}" y="{y + 54}" fill="{MUTED}" '
            f'    font-size="11">{_esc(layer.desc)}</text>\n'
        )

    # Agents on left and right, vertically centered against the stack
    stack_bottom = stack_y + len(_LAYERS) * (band_h + gap) - gap
    agent_y = stack_y + (stack_bottom - stack_y - 320) // 2

    out.append(_agent_box(40, agent_y, "agent · A"))
    out.append(_agent_box(width - 40 - 130, agent_y, "agent · B"))

    # Crossing arrows: from agent A right edge through stack to agent B
    a_right = 40 + 130
    b_left = width - 40 - 130
    for i, layer in enumerate(_LAYERS[:3]):  # only top three layers carry traffic
        y_mid = stack_y + i * (band_h + gap) + band_h / 2
        out.append(
            f'  <line x1="{a_right + 4}" y1="{y_mid}" x2="{b_left - 4}" y2="{y_mid}" '
            f'    stroke="{layer.color}" stroke-width="1.2" stroke-opacity="0.55" '
            f'    stroke-dasharray="6 4" marker-end="url(#arrow)"/>\n'
        )
    # Reverse arrows for remaining layers
    for i, layer in enumerate(_LAYERS[3:], start=3):
        y_mid = stack_y + i * (band_h + gap) + band_h / 2
        out.append(
            f'  <line x1="{b_left - 4}" y1="{y_mid}" x2="{a_right + 4}" y2="{y_mid}" '
            f'    stroke="{layer.color}" stroke-width="1.2" stroke-opacity="0.55" '
            f'    stroke-dasharray="6 4" marker-end="url(#arrow)"/>\n'
        )

    # Footer
    out.append(
        f'  <text x="{width/2}" y="{height - 20}" fill="{MUTED}" '
        f'    font-size="11" text-anchor="middle">'
        f'every cross-membrane operation is gated · cost-aware · auditable</text>\n'
    )

    out.append(_close())
    return "".join(out)


# ─── 2. State graph ─────────────────────────────────────────────────────

def render_state_graph(store: MembraneStore) -> str:
    """Bipartite agents ↔ entries graph, colored by permeability tier."""

    agents = [a for a in store.agents.values() if a.active]
    entries = [e for e in store.entries.values() if e.active]
    # Sort entries grouped by owner so the graph reads top-down
    entries.sort(key=lambda e: (e.agent_id, e.key))

    width = 1200
    row_h = 44
    height = max(620, 140 + max(len(agents), len(entries)) * row_h + 80)

    out = [_svg_open(width, height,
                     "Synthetic Membrane — shared medium state graph")]
    out.append(_title_bar(
        width,
        "Shared medium — exposed state graph",
        "agents on the left · entries on the right · edges colored by permeability tier",
    ))

    # Legend
    legend_y = 96
    legend_items = [
        ("public", GREEN),
        ("trusted", ORANGE),
        ("private", RED),
    ]
    lx = width - 32
    for label, color in reversed(legend_items):
        # right-to-left
        out.append(
            f'  <text x="{lx}" y="{legend_y + 4}" fill="{FG}" font-size="11" '
            f'    text-anchor="end">{_esc(label)}</text>\n'
        )
        lx -= 8 + len(label) * 7
        out.append(
            f'  <rect x="{lx - 14}" y="{legend_y - 7}" width="14" height="10" '
            f'    rx="2" fill="{color}"/>\n'
        )
        lx -= 24

    # Layout columns
    col_l_x = 60
    col_l_w = 320
    col_r_x = 760
    col_top = 140
    agent_h = 56
    entry_h = 36

    # Agents: stack with even spacing
    agent_gap = max(16, (height - col_top - 80 - agent_h * len(agents)) // max(1, len(agents)))
    agent_pos: dict[str, tuple[int, int]] = {}
    for i, a in enumerate(agents):
        y = col_top + i * (agent_h + agent_gap)
        agent_pos[a.agent_id] = (col_l_x, y)
        caps = ", ".join(a.capabilities[:3])
        out.append(
            f'  <rect x="{col_l_x}" y="{y}" width="{col_l_w}" height="{agent_h}" '
            f'    rx="8" fill="{PANEL}" stroke="{ACCENT}" stroke-width="1.3"/>\n'
            f'  <circle cx="{col_l_x + 18}" cy="{y + agent_h/2}" r="6" fill="{ACCENT}"/>\n'
            f'  <text x="{col_l_x + 36}" y="{y + 22}" fill="{FG}" '
            f'    font-size="14" font-weight="700">{_esc(a.name)}</text>\n'
            f'  <text x="{col_l_x + 36}" y="{y + 42}" fill="{MUTED}" '
            f'    font-size="10">{_esc(caps)}</text>\n'
        )

    # Entries
    entry_gap = max(8, (height - col_top - 80 - entry_h * len(entries)) // max(1, len(entries)))
    entry_pos: dict[str, tuple[int, int]] = {}
    for i, e in enumerate(entries):
        y = col_top + i * (entry_h + entry_gap)
        color = PERM_COLOR[e.permeability]
        entry_pos[e.entry_id] = (col_r_x, y)
        out.append(
            f'  <rect x="{col_r_x}" y="{y}" width="370" height="{entry_h}" '
            f'    rx="6" fill="{PANEL}" stroke="{color}" stroke-width="1.3"/>\n'
            f'  <rect x="{col_r_x}" y="{y}" width="6" height="{entry_h}" '
            f'    rx="2" fill="{color}"/>\n'
            f'  <text x="{col_r_x + 16}" y="{y + entry_h/2 + 4}" fill="{FG}" '
            f'    font-size="12" font-weight="600">{_esc(e.key)}</text>\n'
            f'  <text x="{col_r_x + 370 - 10}" y="{y + entry_h/2 + 4}" fill="{color}" '
            f'    font-size="10" text-anchor="end" font-weight="700">'
            f'{_esc(e.permeability.value.upper())}</text>\n'
        )

    # Edges: agent → entry
    for e in entries:
        if e.agent_id not in agent_pos:
            continue
        ax, ay = agent_pos[e.agent_id]
        ex, ey = entry_pos[e.entry_id]
        x1 = ax + col_l_w
        y1 = ay + agent_h / 2
        x2 = ex
        y2 = ey + entry_h / 2
        # cubic bezier for a graceful curve
        cx1 = x1 + (x2 - x1) * 0.45
        cx2 = x2 - (x2 - x1) * 0.45
        color = PERM_COLOR[e.permeability]
        out.append(
            f'  <path d="M{x1},{y1} C{cx1},{y1} {cx2},{y2} {x2},{y2}" '
            f'    fill="none" stroke="{color}" stroke-width="1.4" '
            f'    stroke-opacity="0.55"/>\n'
        )

    out.append(_close())
    return "".join(out)


# ─── 3. Swarm timeline ──────────────────────────────────────────────────

def render_swarm_timeline(store: MembraneStore) -> str:
    """Show swarm lifecycle: created, joined, activated, deactivated, dissolved."""

    swarm_events = [
        e for e in store.events
        if e.event_type in {
            EventType.SWARM_CREATED,
            EventType.SWARM_JOINED,
            EventType.SWARM_LEFT,
            EventType.SWARM_ACTIVATED,
            EventType.SWARM_DEACTIVATED,
            EventType.SWARM_DISSOLVED,
        }
    ]

    swarms = list(store.swarms.values())

    width = 1200
    row_h = 140
    height = 140 + max(1, len(swarms)) * row_h + 80

    out = [_svg_open(width, height,
                     "Synthetic Membrane — swarm activation timeline")]
    out.append(_title_bar(
        width,
        "Quorum-sensing swarm timeline",
        "swarm lifecycle plotted against the event log sequence",
    ))

    if not swarms:
        out.append(
            f'  <text x="{width/2}" y="{height/2}" fill="{MUTED}" '
            f'    font-size="14" text-anchor="middle">no swarms recorded</text>\n'
        )
        out.append(_close())
        return "".join(out)

    last_seq = max((e.seq for e in store.events), default=1)
    axis_left = 220
    axis_right = width - 60
    axis_span = axis_right - axis_left

    def x_of(seq: int) -> float:
        return axis_left + (seq / max(1, last_seq)) * axis_span

    # Top axis with seq ticks
    axis_y = 110
    out.append(
        f'  <line x1="{axis_left}" y1="{axis_y}" x2="{axis_right}" y2="{axis_y}" '
        f'    stroke="{BORDER}" stroke-width="1"/>\n'
    )
    for s in range(0, last_seq + 1, max(1, last_seq // 10)):
        tx = x_of(s)
        out.append(
            f'  <line x1="{tx}" y1="{axis_y - 4}" x2="{tx}" y2="{axis_y + 4}" '
            f'    stroke="{MUTED}" stroke-width="1"/>\n'
            f'  <text x="{tx}" y="{axis_y - 10}" fill="{MUTED}" font-size="9" '
            f'    text-anchor="middle">{s}</text>\n'
        )
    out.append(
        f'  <text x="{axis_right}" y="{axis_y - 22}" fill="{MUTED}" font-size="10" '
        f'    text-anchor="end">event sequence →</text>\n'
    )

    # One row per swarm
    for i, swarm in enumerate(swarms):
        row_y = 150 + i * row_h
        center_y = row_y + 40

        # Swarm label (left gutter)
        out.append(
            f'  <rect x="32" y="{row_y}" width="170" height="{row_h - 20}" '
            f'    rx="8" fill="{PANEL}" stroke="{BORDER}"/>\n'
            f'  <text x="40" y="{row_y + 22}" fill="{ACCENT}" font-size="13" '
            f'    font-weight="700">{_esc(swarm.name)}</text>\n'
            f'  <text x="40" y="{row_y + 40}" fill="{MUTED}" font-size="10">'
            f'cap={_esc(swarm.capability_required)} · thr={swarm.threshold}</text>\n'
            f'  <text x="40" y="{row_y + 58}" fill="{FG}" font-size="10">'
            f'members: {_esc(", ".join(swarm.members) or "none")}</text>\n'
            f'  <text x="40" y="{row_y + 76}" fill="{GREEN if swarm.active else MUTED}" '
            f'    font-size="10" font-weight="700">'
            f'state: {"ACTIVE" if swarm.active else "inactive"}</text>\n'
        )

        # Baseline lane line
        out.append(
            f'  <line x1="{axis_left}" y1="{center_y}" x2="{axis_right}" y2="{center_y}" '
            f'    stroke="{BORDER}" stroke-width="1" stroke-dasharray="3 4"/>\n'
        )

        # Find created/activated/deactivated/dissolved seqs for this swarm
        related = [e for e in swarm_events
                   if e.payload.get("swarm_id") == swarm.swarm_id]
        if not related:
            continue

        created_seq = next(
            (e.seq for e in related if e.event_type == EventType.SWARM_CREATED),
            None,
        )
        activated_seq = next(
            (e.seq for e in related if e.event_type == EventType.SWARM_ACTIVATED),
            None,
        )
        deactivated_seq = next(
            (e.seq for e in related if e.event_type == EventType.SWARM_DEACTIVATED),
            None,
        )
        dissolved_seq = next(
            (e.seq for e in related if e.event_type == EventType.SWARM_DISSOLVED),
            None,
        )

        # Inactive band: created → activated (orange-ish)
        if created_seq is not None:
            end = activated_seq if activated_seq is not None else last_seq
            out.append(
                f'  <rect x="{x_of(created_seq)}" y="{center_y - 14}" '
                f'    width="{max(2, x_of(end) - x_of(created_seq))}" height="28" '
                f'    rx="4" fill="{ORANGE}" fill-opacity="0.18" '
                f'    stroke="{ORANGE}" stroke-opacity="0.55"/>\n'
            )

        # Active band: activated → deactivated|dissolved|now (green)
        if activated_seq is not None:
            end = deactivated_seq or dissolved_seq or last_seq
            out.append(
                f'  <rect x="{x_of(activated_seq)}" y="{center_y - 18}" '
                f'    width="{max(2, x_of(end) - x_of(activated_seq))}" height="36" '
                f'    rx="4" fill="{GREEN}" fill-opacity="0.22" '
                f'    stroke="{GREEN}" stroke-opacity="0.7"/>\n'
            )

        # Event tick marks — stagger labels vertically so they do not collide
        for idx, e in enumerate(sorted(related, key=lambda x: x.seq)):
            tx = x_of(e.seq)
            label_color = {
                EventType.SWARM_CREATED: ACCENT,
                EventType.SWARM_JOINED: GREEN,
                EventType.SWARM_LEFT: ORANGE,
                EventType.SWARM_ACTIVATED: GREEN,
                EventType.SWARM_DEACTIVATED: ORANGE,
                EventType.SWARM_DISSOLVED: RED,
            }.get(e.event_type, MUTED)
            out.append(
                f'  <line x1="{tx}" y1="{center_y - 22}" x2="{tx}" y2="{center_y + 22}" '
                f'    stroke="{label_color}" stroke-width="1.6"/>\n'
                f'  <circle cx="{tx}" cy="{center_y - 22}" r="4" fill="{label_color}"/>\n'
            )

            short = {
                EventType.SWARM_CREATED: "created",
                EventType.SWARM_JOINED: f"+ {e.agent_id}",
                EventType.SWARM_LEFT: f"− {e.agent_id}",
                EventType.SWARM_ACTIVATED: "ACTIVATED",
                EventType.SWARM_DEACTIVATED: "deactivated",
                EventType.SWARM_DISSOLVED: "dissolved",
            }[e.event_type]
            font_weight = "700" if e.event_type in {
                EventType.SWARM_ACTIVATED,
                EventType.SWARM_DEACTIVATED,
                EventType.SWARM_DISSOLVED,
            } else "500"
            # Cycle vertical offset across three rows to prevent overlap.
            offset = 36 + (idx % 3) * 14
            label_y = center_y + offset
            # Tiny tether from tick to label so the row assignment reads.
            out.append(
                f'  <line x1="{tx}" y1="{center_y + 22}" x2="{tx}" y2="{label_y - 9}" '
                f'    stroke="{label_color}" stroke-width="0.8" stroke-opacity="0.5" '
                f'    stroke-dasharray="2 2"/>\n'
                f'  <text x="{tx + 6}" y="{label_y}" fill="{label_color}" '
                f'    font-size="10" font-weight="{font_weight}">{_esc(short)}</text>\n'
            )

    # Bottom legend
    legend_y = height - 30
    items = [
        ("created",       ACCENT),
        ("joined",        GREEN),
        ("ACTIVATED",     GREEN),
        ("deactivated",   ORANGE),
        ("dissolved",     RED),
    ]
    lx = 40
    for label, color in items:
        out.append(
            f'  <circle cx="{lx}" cy="{legend_y}" r="4" fill="{color}"/>\n'
            f'  <text x="{lx + 10}" y="{legend_y + 4}" fill="{MUTED}" '
            f'    font-size="11">{_esc(label)}</text>\n'
        )
        lx += 12 + len(label) * 8 + 12

    out.append(_close())
    return "".join(out)


# ─── Driver ─────────────────────────────────────────────────────────────

def generate_all(
    store: MembraneStore,
    permeability: PermeabilityEngine,
    swarm: SwarmEngine,
    output_dir: Path | str,
) -> dict[str, Path]:
    """Render all SVGs into output_dir. Returns a dict of name → path."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    files = {
        "architecture": out / "architecture.svg",
        "state_graph": out / "state_graph.svg",
        "swarm_timeline": out / "swarm_timeline.svg",
    }
    files["architecture"].write_text(render_architecture())
    files["state_graph"].write_text(render_state_graph(store))
    files["swarm_timeline"].write_text(render_swarm_timeline(store))
    return files


if __name__ == "__main__":
    from demo.agent_simulation import run
    result = run()
    paths = generate_all(result.store, result.permeability, result.swarm,
                         Path(__file__).parent / "output")
    for name, p in paths.items():
        print(f"{name:18s} → {p}")

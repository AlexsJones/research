"""
Agent simulation: five agents collaborate on a research brief through the
Synthetic Membrane.

Roles
─────
  orchestrator  — plans the work and creates swarms
  researcher    — gathers facts, exposes findings
  writer        — drafts prose at TRUSTED tier
  editor        — reviews drafts and posts feedback
  reviewer      — final approval member of the review swarm

The simulation exercises every public capability of the membrane MVP:
register / expose / query / subscribe / broadcast / set_trust / swarm_*
and the three permeability tiers. It returns the live store, permeability
engine, and swarm engine so visualizers and benchmarks can read the same
trace.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Allow `python -m demo` from mvp/ without an editable install.
_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from membrane.models import EventType, PermeabilityLevel
from membrane.permeability import PermeabilityEngine
from membrane.store import MembraneStore
from membrane.swarm import SwarmEngine

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns


# ─── Theme ──────────────────────────────────────────────────────────────
ACCENT = "#58a6ff"   # blue   — info / structure
GREEN = "#3fb950"    # green  — success / activation
ORANGE = "#d29922"   # orange — attention / trusted
RED = "#f85149"      # red    — denied / private
MUTED = "#6e7681"    # muted  — meta
TEXT = "#e6edf3"     # base text


PERM_STYLE = {
    PermeabilityLevel.PUBLIC: GREEN,
    PermeabilityLevel.TRUSTED: ORANGE,
    PermeabilityLevel.PRIVATE: RED,
}


@dataclass
class SimulationResult:
    """Everything the demo produced — used by visualize and benchmarks."""

    store: MembraneStore
    permeability: PermeabilityEngine
    swarm: SwarmEngine
    transcript: list[dict[str, Any]] = field(default_factory=list)
    elapsed_seconds: float = 0.0


# ─── Logging helpers ────────────────────────────────────────────────────


def _heading(console: Console, n: int, title: str, subtitle: str = "") -> None:
    label = Text(f"  STEP {n:02d}  ", style=f"bold {TEXT} on {ACCENT}")
    name = Text(f"  {title}", style=f"bold {TEXT}")
    sub = Text(f"   {subtitle}", style=f"italic {MUTED}") if subtitle else Text("")
    console.print()
    console.print(Group(label + name + sub))
    console.print(Rule(style=MUTED))


def _act(console: Console, agent: str, verb: str, detail: str = "") -> None:
    arrow = Text("  ▸ ", style=ACCENT)
    who = Text(f"{agent:<13}", style=f"bold {TEXT}")
    action = Text(f"{verb}", style=f"{TEXT}")
    bits = arrow + who + action
    if detail:
        bits.append(f"  {detail}", style=MUTED)
    console.print(bits)


def _emit_panel(console: Console, title: str, body: Any, color: str = ACCENT) -> None:
    console.print(Panel(body, title=Text(title, style=f"bold {color}"),
                        border_style=color, padding=(0, 2)))


def _stats_table(store: MembraneStore, swarm: SwarmEngine,
                 perm: PermeabilityEngine) -> Table:
    s = store.get_stats()
    t = Table(show_header=True, header_style=f"bold {ACCENT}",
              border_style=MUTED, padding=(0, 2))
    t.add_column("metric", style=TEXT)
    t.add_column("value", style=TEXT, justify="right")
    t.add_row("events in log", str(s["total_events"]))
    t.add_row("registered agents", str(s["registered_agents"]))
    t.add_row("active entries", str(s["active_entries"]))
    t.add_row("active subscriptions", str(s["active_subscriptions"]))
    t.add_row("broadcasts", str(s["broadcasts"]))
    t.add_row("active swarms", str(s["active_swarms"]))
    t.add_row("last sequence", str(s["last_seq"]))
    t.add_row("trust edges", str(sum(len(v) for v in perm.get_trust_graph().values())))
    return t


def _events_breakdown(store: MembraneStore) -> Table:
    counts: dict[str, int] = {}
    for e in store.events:
        counts[e.event_type.value] = counts.get(e.event_type.value, 0) + 1
    t = Table(show_header=True, header_style=f"bold {ACCENT}",
              border_style=MUTED, padding=(0, 2))
    t.add_column("event_type", style=TEXT)
    t.add_column("count", style=TEXT, justify="right")
    for k in sorted(counts, key=lambda x: -counts[x]):
        t.add_row(k, str(counts[k]))
    return t


def _state_table(store: MembraneStore) -> Table:
    t = Table(show_header=True, header_style=f"bold {ACCENT}",
              border_style=MUTED, padding=(0, 2))
    t.add_column("key", style=TEXT)
    t.add_column("owner", style=TEXT)
    t.add_column("tier", style=TEXT)
    t.add_column("value", style=MUTED)
    for entry in store.entries.values():
        if not entry.active:
            continue
        tier = Text(entry.permeability.value,
                    style=PERM_STYLE[entry.permeability])
        v = str(entry.value)
        if len(v) > 50:
            v = v[:47] + "..."
        t.add_row(entry.key, entry.agent_id, tier, v)
    return t


def _banner(console: Console) -> None:
    title = Text("SYNTHETIC  MEMBRANE", style=f"bold {ACCENT}")
    sub = Text("MVP demonstration — five agents, one shared medium",
               style=f"italic {MUTED}")
    body = Group(title, sub)
    console.print()
    console.print(Panel(body, border_style=ACCENT, padding=(1, 4),
                        title=Text("demo", style=MUTED)))


# ─── Simulation ─────────────────────────────────────────────────────────


def run(console: Console | None = None, pause: float = 0.0) -> SimulationResult:
    """Run the full coordination scenario.

    Args:
        console: rich Console (created if None)
        pause: seconds to sleep between steps for dramatic pacing
    """
    console = console or Console()
    started = time.perf_counter()

    store = MembraneStore()
    perm = PermeabilityEngine()
    swarm = SwarmEngine(store)
    transcript: list[dict[str, Any]] = []

    def log(kind: str, **payload: Any) -> None:
        transcript.append({"kind": kind, **payload})

    _banner(console)

    # ── 01: registration ────────────────────────────────────────────────
    _heading(console, 1, "Boot the membrane",
             "instantiate store · permeability · swarm engines")
    _emit_panel(console, "initial stats", _stats_table(store, swarm, perm))
    if pause:
        time.sleep(pause)

    # ── 02: agents register ─────────────────────────────────────────────
    _heading(console, 2, "Agents register",
             "each agent advertises capabilities the membrane will use")
    roster = [
        ("orchestrator", "Orchestrator", ["coordination", "planning", "synthesis"]),
        ("researcher", "Researcher", ["research", "fact_check", "data_analysis"]),
        ("writer", "Writer", ["writing", "drafting", "summarization"]),
        ("editor", "Editor", ["editing", "reviewing", "style"]),
        ("reviewer", "Reviewer", ["reviewing", "critique", "quality_check"]),
    ]
    for aid, name, caps in roster:
        store.register_agent(aid, name, caps)
        _act(console, aid, "register_agent", f"caps={caps}")
        log("register", agent=aid, capabilities=caps)
    if pause:
        time.sleep(pause)

    # ── 03: token budgets ───────────────────────────────────────────────
    _heading(console, 3, "Set token budgets",
             "every cross-membrane read costs tokens — default 1000 each")
    for aid, *_ in roster:
        perm.set_token_budget(aid, 1000)
        _act(console, aid, "set_token_budget", "= 1000")
    if pause:
        time.sleep(pause)

    # ── 04: trust ───────────────────────────────────────────────────────
    _heading(console, 4, "Establish trust relationships",
             "trust is directional — peer trust enables TRUSTED tier reads")
    trust_edges = [
        ("writer", "editor", 0.9),
        ("editor", "writer", 0.9),
        ("editor", "reviewer", 0.8),
        ("reviewer", "editor", 0.8),
        ("orchestrator", "writer", 0.7),
        ("orchestrator", "editor", 0.7),
        ("orchestrator", "researcher", 0.7),
    ]
    for a, b, s in trust_edges:
        perm.set_trust(a, b, s)
        _act(console, a, "set_trust",
             f"→ {b} = {s}")
        log("trust", source=a, target=b, score=s)
    if pause:
        time.sleep(pause)

    # ── 05: subscriptions ───────────────────────────────────────────────
    _heading(console, 5, "Orchestrator subscribes",
             "watches three pattern families to react to incoming work")
    for pattern in ["findings.*", "drafts.*", "feedback.*", "final.*"]:
        store.subscribe("orchestrator", pattern)
        _act(console, "orchestrator", "subscribe", f"pattern='{pattern}'")
    if pause:
        time.sleep(pause)

    # ── 06: orchestrator posts task ─────────────────────────────────────
    _heading(console, 6, "Orchestrator exposes the task",
             "PUBLIC tier — any agent can pick it up")
    store.expose(
        "orchestrator", "tasks.brief",
        "Write a 500-word brief on urban climate adaptation strategies.",
        PermeabilityLevel.PUBLIC,
    )
    _act(console, "orchestrator", "expose",
         "key=tasks.brief  tier=public")
    if pause:
        time.sleep(pause)

    # ── 07: researcher picks up the task ────────────────────────────────
    _heading(console, 7, "Researcher discovers the task",
             "queries `tasks.*` — receives the brief from orchestrator")
    tasks = store.query("researcher", "tasks.*")
    for r in tasks:
        _act(console, "researcher", "query → hit",
             f"{r.key} = \"{r.value[:60]}...\"")
    if pause:
        time.sleep(pause)

    # ── 08: researcher exposes findings ─────────────────────────────────
    _heading(console, 8, "Researcher exposes findings",
             "two PUBLIC facts, one PRIVATE note that should stay internal")
    findings = [
        ("findings.heat_islands", "Urban heat islands raise local temp 5–10°C",
         PermeabilityLevel.PUBLIC),
        ("findings.coastal_risk",
         "1B people exposed to 100yr flood zones by 2050 (IPCC AR6)",
         PermeabilityLevel.PUBLIC),
        ("findings.green_infra",
         "Green roofs reduce building cooling load 20–30%",
         PermeabilityLevel.PUBLIC),
        ("findings.notes_internal",
         "TODO verify IPCC citation against AR6 WGII Table 9.SM.5",
         PermeabilityLevel.PRIVATE),
    ]
    for k, v, tier in findings:
        store.expose("researcher", k, v, tier)
        tier_text = Text(tier.value, style=PERM_STYLE[tier])
        _act(console, "researcher", "expose", f"key={k}  tier=")
        console.print(Text("                 ", end="") + tier_text +
                      Text(f"  value=\"{v[:60]}...\"", style=MUTED))
    if pause:
        time.sleep(pause)

    # ── 09: writer reads findings ───────────────────────────────────────
    _heading(console, 9, "Writer reads PUBLIC findings",
             "the PRIVATE note is invisible — gated at the membrane")
    candidates = store.query("writer", "findings.*")
    for entry in candidates:
        decision = perm.evaluate(
            reader_id="writer", owner_id=entry.agent_id,
            permeability=entry.permeability, token_cost=15,
        )
        if decision.allowed:
            perm.consume_tokens("writer", 15)
            _act(console, "writer", "query → hit",
                 f"{entry.key}  (cost=15 tok, gate='{decision.reason}')")
        else:
            _act(console, "writer", "query → DENIED",
                 f"{entry.key}  ({decision.reason})")
    # Confirm the private one stayed hidden
    private_visible = any(e.key == "findings.notes_internal" for e in candidates)
    note = "PRIVATE note hidden" if not private_visible else "PRIVATE note leaked"
    color = GREEN if not private_visible else RED
    console.print()
    _emit_panel(console, "permeability check",
                Text(note, style=f"bold {color}"), color=color)
    if pause:
        time.sleep(pause)

    # ── 10: writer drafts ───────────────────────────────────────────────
    _heading(console, 10, "Writer drafts at TRUSTED tier",
             "drafts visible only to peers with sufficient trust")
    drafts = [
        ("drafts.intro",
         "Cities are adapting through cooling corridors, blue infrastructure..."),
        ("drafts.body",
         "Heat resilience and coastal defense are the two structural vectors..."),
        ("drafts.outro",
         "Adaptation is no longer optional — it is the default planning frame."),
    ]
    for k, v in drafts:
        store.expose("writer", k, v, PermeabilityLevel.TRUSTED)
        _act(console, "writer", "expose", f"key={k}  tier=trusted")
    if pause:
        time.sleep(pause)

    # ── 11: reviewer denied (no trust score) ────────────────────────────
    _heading(console, 11, "Reviewer attempts to read drafts",
             "no trust edge with writer → membrane denies the read")
    candidates = store.query("reviewer", "drafts.*")
    denied_count = 0
    allowed_count = 0
    for entry in candidates:
        decision = perm.evaluate(
            reader_id="reviewer", owner_id=entry.agent_id,
            permeability=entry.permeability, token_cost=15,
        )
        if decision.allowed:
            allowed_count += 1
            _act(console, "reviewer", "query → hit", entry.key)
        else:
            denied_count += 1
            _act(console, "reviewer", "query → DENIED",
                 f"{entry.key}  ({decision.reason})")
    _emit_panel(console, "gate result",
                Text(f"{denied_count} denied · {allowed_count} allowed",
                     style=f"bold {ORANGE if denied_count else GREEN}"),
                color=ORANGE if denied_count else GREEN)
    if pause:
        time.sleep(pause)

    # ── 12: editor reviews drafts ───────────────────────────────────────
    _heading(console, 12, "Editor reads drafts (trust = 0.9)",
             "trust edge with writer permits TRUSTED tier reads")
    candidates = store.query("editor", "drafts.*")
    for entry in candidates:
        decision = perm.evaluate(
            reader_id="editor", owner_id=entry.agent_id,
            permeability=entry.permeability, token_cost=15,
        )
        if decision.allowed:
            perm.consume_tokens("editor", 15)
            _act(console, "editor", "query → hit",
                 f"{entry.key}  (gate='{decision.reason}')")
    if pause:
        time.sleep(pause)

    # ── 13: editor posts feedback ───────────────────────────────────────
    _heading(console, 13, "Editor posts feedback",
             "TRUSTED tier — visible to writer, invisible to reviewer")
    fb = [
        ("feedback.intro",
         "Strengthen the opening hook — lead with a specific city."),
        ("feedback.body",
         "Cite the IPCC AR6 figures explicitly to anchor the claim."),
    ]
    for k, v in fb:
        store.expose("editor", k, v, PermeabilityLevel.TRUSTED)
        _act(console, "editor", "expose", f"key={k}  tier=trusted")
    if pause:
        time.sleep(pause)

    # ── 14: writer revises and ships final ──────────────────────────────
    _heading(console, 14, "Writer revises and ships final brief",
             "PUBLIC tier — broadcast to all and crawlable by the orchestrator")
    feedback = store.query("writer", "feedback.*")
    for entry in feedback:
        decision = perm.evaluate(
            reader_id="writer", owner_id=entry.agent_id,
            permeability=entry.permeability, token_cost=10,
        )
        if decision.allowed:
            perm.consume_tokens("writer", 10)
            _act(console, "writer", "query → hit",
                 f"{entry.key}  → revising")

    # Retract drafts since they are superseded
    for entry in list(store.entries.values()):
        if entry.active and entry.agent_id == "writer" and entry.key.startswith("drafts."):
            store.retract("writer", entry.entry_id)
            _act(console, "writer", "retract", f"{entry.key}  (superseded)")

    store.expose(
        "writer", "final.brief",
        "Cities like Singapore, Rotterdam, and Phoenix illustrate three "
        "approaches to climate adaptation: cooling corridors, water "
        "buffering, and shade infrastructure. Each addresses a specific "
        "exposure profile yet shares a common substrate of distributed "
        "sensing and shared decision-making.",
        PermeabilityLevel.PUBLIC,
    )
    _act(console, "writer", "expose", "key=final.brief  tier=public")
    if pause:
        time.sleep(pause)

    # ── 15: swarm formation ─────────────────────────────────────────────
    _heading(console, 15, "Orchestrator forms a review swarm",
             "capability=reviewing  threshold=2  → activates on 2nd join")
    _, sw = swarm.create_swarm("Final Review", "reviewing", threshold=2)
    _act(console, "orchestrator", "swarm_create",
         f"name='Final Review' cap=reviewing threshold=2")
    log("swarm_create", swarm_id=sw.swarm_id, name=sw.name)

    # editor joins (under threshold — not active)
    swarm.join_swarm(sw.swarm_id, "editor")
    _act(console, "editor", "swarm_join",
         f"members={len(sw.members)}/{sw.threshold}  active={sw.active}")
    log("swarm_join", swarm_id=sw.swarm_id, agent="editor",
        active=sw.active, members=list(sw.members))

    # reviewer joins → activation
    swarm.join_swarm(sw.swarm_id, "reviewer")
    _act(console, "reviewer", "swarm_join",
         f"members={len(sw.members)}/{sw.threshold}  active={sw.active}")
    log("swarm_join", swarm_id=sw.swarm_id, agent="reviewer",
        active=sw.active, members=list(sw.members))
    if sw.active:
        _emit_panel(
            console,
            "QUORUM SENSED — swarm activated",
            Text(f"  swarm '{sw.name}'  members={sw.members}",
                 style=f"bold {GREEN}"),
            color=GREEN,
        )
    if pause:
        time.sleep(pause)

    # ── 16: broadcast complete ──────────────────────────────────────────
    _heading(console, 16, "Writer broadcasts completion",
             "all other registered agents receive the message")
    _, bcast = store.broadcast("writer", "Brief complete — ready for review.")
    _act(console, "writer", "broadcast",
         f"recipients={bcast.recipients}")
    if pause:
        time.sleep(pause)

    # ── 17: final state ─────────────────────────────────────────────────
    _heading(console, 17, "Final state",
             "the membrane has accumulated structure across 17 steps")
    console.print(Columns([
        Panel(_stats_table(store, swarm, perm),
              title=Text("store stats", style=f"bold {ACCENT}"),
              border_style=ACCENT, padding=(0, 1)),
        Panel(_events_breakdown(store),
              title=Text("event log breakdown", style=f"bold {ACCENT}"),
              border_style=ACCENT, padding=(0, 1)),
    ], expand=True))
    console.print()
    _emit_panel(console, "shared medium — current entries",
                _state_table(store))

    elapsed = time.perf_counter() - started
    console.print()
    console.print(Text(f"  simulation complete · {len(store.events)} events · "
                       f"{elapsed*1000:.1f} ms wall-clock",
                       style=f"bold {GREEN}"))
    console.print()

    return SimulationResult(
        store=store,
        permeability=perm,
        swarm=swarm,
        transcript=transcript,
        elapsed_seconds=elapsed,
    )


if __name__ == "__main__":
    run()

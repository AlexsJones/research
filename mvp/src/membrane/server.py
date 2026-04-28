"""
MCP server for the Synthetic Membrane MVP.

Exposes the membrane's core capabilities — agent registration, state
exposure, querying, subscriptions, broadcasts, swarms, trust, and
introspection — as MCP tools over stdio.

Wires the store, permeability engine, and swarm engine through
closures so handlers stay simple and the runtime state is owned
by `main()`.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from mcp import types
from mcp.server.lowlevel.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from membrane.models import EventType
from membrane.permeability import PermeabilityEngine
from membrane.store import MembraneStore
from membrane.swarm import SwarmEngine


SERVER_NAME = "membrane"
SERVER_VERSION = "0.1.0"


def _encode(obj: Any) -> Any:
    """JSON-encode dataclasses, enums, and datetimes."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _encode(v) for k, v in asdict(obj).items()}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_encode(v) for v in obj]
    return obj


def _ok(payload: Any) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(_encode(payload), indent=2))]


def _err(message: str, **extra: Any) -> list[types.TextContent]:
    body: dict[str, Any] = {"ok": False, "error": message}
    body.update(extra)
    return [types.TextContent(type="text", text=json.dumps(body, indent=2))]


def _tool_definitions() -> list[types.Tool]:
    """Schemas for the 14 membrane tools."""
    return [
        types.Tool(
            name="register_agent",
            description="Register an agent with the membrane.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "name": {"type": "string"},
                    "capabilities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": [],
                    },
                },
                "required": ["agent_id", "name"],
            },
        ),
        types.Tool(
            name="unregister_agent",
            description="Unregister an agent and retract its state.",
            inputSchema={
                "type": "object",
                "properties": {"agent_id": {"type": "string"}},
                "required": ["agent_id"],
            },
        ),
        types.Tool(
            name="expose",
            description="Expose a key/value to the shared medium at a permeability tier.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "key": {"type": "string"},
                    "value": {},
                    "permeability": {
                        "type": "string",
                        "enum": ["public", "trusted", "private"],
                        "default": "public",
                    },
                },
                "required": ["agent_id", "key", "value"],
            },
        ),
        types.Tool(
            name="retract",
            description="Retract an exposed entry by id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "entry_id": {"type": "string"},
                },
                "required": ["agent_id", "entry_id"],
            },
        ),
        types.Tool(
            name="query",
            description="Query the shared medium with a glob pattern, gated by permeability.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reader_id": {"type": "string"},
                    "pattern": {"type": "string", "default": "*"},
                    "permeability": {
                        "type": "string",
                        "enum": ["public", "trusted", "private"],
                    },
                    "trust_threshold": {"type": "number", "default": 0.5},
                    "token_cost": {"type": "integer", "default": 0},
                },
                "required": ["reader_id"],
            },
        ),
        types.Tool(
            name="subscribe",
            description="Subscribe an agent to state changes matching a glob pattern.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "pattern": {"type": "string"},
                },
                "required": ["agent_id", "pattern"],
            },
        ),
        types.Tool(
            name="unsubscribe",
            description="Remove an existing subscription by id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "subscription_id": {"type": "string"},
                },
                "required": ["agent_id", "subscription_id"],
            },
        ),
        types.Tool(
            name="broadcast",
            description="Broadcast a message to all other registered agents.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["agent_id", "message"],
            },
        ),
        types.Tool(
            name="swarm_create",
            description="Define a quorum-sensing swarm.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "capability_required": {"type": "string"},
                    "threshold": {"type": "integer", "minimum": 1},
                },
                "required": ["name", "capability_required", "threshold"],
            },
        ),
        types.Tool(
            name="swarm_join",
            description="Join a swarm; activates the swarm if the threshold is reached.",
            inputSchema={
                "type": "object",
                "properties": {
                    "swarm_id": {"type": "string"},
                    "agent_id": {"type": "string"},
                },
                "required": ["swarm_id", "agent_id"],
            },
        ),
        types.Tool(
            name="swarm_leave",
            description="Leave a swarm; deactivates it if members fall below threshold.",
            inputSchema={
                "type": "object",
                "properties": {
                    "swarm_id": {"type": "string"},
                    "agent_id": {"type": "string"},
                },
                "required": ["swarm_id", "agent_id"],
            },
        ),
        types.Tool(
            name="swarm_dissolve",
            description="Explicitly dissolve a swarm.",
            inputSchema={
                "type": "object",
                "properties": {"swarm_id": {"type": "string"}},
                "required": ["swarm_id"],
            },
        ),
        types.Tool(
            name="set_trust",
            description="Set the trust score (0.0–1.0) from one agent toward a peer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "peer_id": {"type": "string"},
                    "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                },
                "required": ["agent_id", "peer_id", "score"],
            },
        ),
        types.Tool(
            name="stats",
            description="Return store stats, active swarms, and the trust graph.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


def build_server(
    store: MembraneStore,
    permeability: PermeabilityEngine,
    swarm: SwarmEngine,
) -> Server:
    """Construct a configured MCP `Server` wired to the given engines."""
    server: Server = Server(SERVER_NAME)

    @server.list_tools()
    async def _list_tools() -> list[types.Tool]:
        return _tool_definitions()

    @server.call_tool()
    async def _call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
        args = arguments or {}

        if name == "register_agent":
            event = store.register_agent(
                agent_id=args["agent_id"],
                name=args["name"],
                capabilities=args.get("capabilities", []),
            )
            return _ok({"ok": True, "event": event})

        if name == "unregister_agent":
            event = store.unregister_agent(agent_id=args["agent_id"])
            return _ok({"ok": True, "event": event})

        if name == "expose":
            event, entry = store.expose(
                agent_id=args["agent_id"],
                key=args["key"],
                value=args["value"],
                permeability=args.get("permeability", "public"),
            )
            return _ok({"ok": True, "entry": entry, "event": event})

        if name == "retract":
            event = store.retract(agent_id=args["agent_id"], entry_id=args["entry_id"])
            return _ok({"ok": True, "event": event})

        if name == "query":
            reader_id = args["reader_id"]
            pattern = args.get("pattern", "*")
            perm_filter = args.get("permeability")
            trust_threshold = float(args.get("trust_threshold", 0.5))
            token_cost = int(args.get("token_cost", 0))

            candidates = store.query(reader_id=reader_id, pattern=pattern, permeability=perm_filter)
            results = []
            denied = []
            for entry in candidates:
                decision = permeability.evaluate(
                    reader_id=reader_id,
                    owner_id=entry.agent_id,
                    permeability=entry.permeability,
                    token_cost=token_cost,
                    trust_threshold=trust_threshold,
                )
                if decision.allowed:
                    if token_cost:
                        permeability.consume_tokens(reader_id, token_cost)
                    results.append({"entry": entry, "gate": decision})
                else:
                    denied.append({"entry_id": entry.entry_id, "key": entry.key, "gate": decision})
            return _ok({"ok": True, "count": len(results), "results": results, "denied": denied})

        if name == "subscribe":
            event, sub = store.subscribe(agent_id=args["agent_id"], pattern=args["pattern"])
            return _ok({"ok": True, "subscription": sub, "event": event})

        if name == "unsubscribe":
            sub_id = args["subscription_id"]
            existing = store.subscriptions.get(sub_id)
            if existing is None:
                return _err("subscription not found", subscription_id=sub_id)
            event = store._emit(args["agent_id"], EventType.SUBSCRIPTION_REMOVED, {
                "subscription_id": sub_id,
            })
            store._apply_event(event)
            return _ok({"ok": True, "event": event})

        if name == "broadcast":
            event, bcast = store.broadcast(agent_id=args["agent_id"], message=args["message"])
            return _ok({"ok": True, "broadcast": bcast, "event": event})

        if name == "swarm_create":
            event, sw = swarm.create_swarm(
                name=args["name"],
                capability_required=args["capability_required"],
                threshold=int(args["threshold"]),
            )
            return _ok({"ok": True, "swarm": sw, "event": event})

        if name == "swarm_join":
            event, sw = swarm.join_swarm(swarm_id=args["swarm_id"], agent_id=args["agent_id"])
            if sw is None:
                return _err("swarm join denied", event=_encode(event))
            info = swarm.get_swarm_info(sw.swarm_id)
            return _ok({"ok": True, "swarm": info, "event": event})

        if name == "swarm_leave":
            event = swarm.leave_swarm(swarm_id=args["swarm_id"], agent_id=args["agent_id"])
            if event is None:
                return _err("not a member or swarm not found", swarm_id=args["swarm_id"])
            return _ok({"ok": True, "event": event, "swarm": swarm.get_swarm_info(args["swarm_id"])})

        if name == "swarm_dissolve":
            event = swarm.dissolve_swarm(swarm_id=args["swarm_id"])
            if event is None:
                return _err("swarm not found", swarm_id=args["swarm_id"])
            return _ok({"ok": True, "event": event})

        if name == "set_trust":
            permeability.set_trust(
                agent_id=args["agent_id"],
                peer_id=args["peer_id"],
                score=float(args["score"]),
            )
            return _ok({
                "ok": True,
                "agent_id": args["agent_id"],
                "peer_id": args["peer_id"],
                "score": permeability._get_trust(args["agent_id"], args["peer_id"]),
            })

        if name == "stats":
            return _ok({
                "ok": True,
                "store": store.get_stats(),
                "active_swarms": [swarm.get_swarm_info(s.swarm_id) for s in swarm.get_active_swarms()],
                "trust_graph": permeability.get_trust_graph(),
            })

        return _err(f"unknown tool: {name}")

    return server


async def _run() -> None:
    store = MembraneStore()
    permeability = PermeabilityEngine()
    swarm = SwarmEngine(store)
    server = build_server(store, permeability, swarm)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main() -> None:
    """Entrypoint registered as the `membrane-server` script."""
    asyncio.run(_run())


if __name__ == "__main__":
    main()

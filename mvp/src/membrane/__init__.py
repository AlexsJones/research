"""
Synthetic Membrane — A shared permeable boundary layer for AI agents.

The membrane provides:
- Permeability: 3-tier access control (public/trusted/private)
- Shared Medium: Event-sourced in-memory state store
- Coordination: Quorum-sensing swarms for emergent collaboration
"""

from membrane.models import Agent, Event, Entry, Swarm, PermeabilityLevel
from membrane.store import MembraneStore
from membrane.permeability import PermeabilityEngine
from membrane.swarm import SwarmEngine

__all__ = [
    "Agent",
    "Event",
    "Entry",
    "Swarm",
    "PermeabilityLevel",
    "MembraneStore",
    "PermeabilityEngine",
    "SwarmEngine",
]

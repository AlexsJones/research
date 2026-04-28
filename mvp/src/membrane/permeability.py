"""
Permeability engine for the Synthetic Membrane.

Implements default-deny communication gating: agents work locally by default
and only cross the membrane when cost-benefit analysis justifies it.

Three tiers:
- PUBLIC: Any registered agent can read
- TRUSTED: Only agents with mutual trust relationships
- PRIVATE: Only the owner can read

The gate engine evaluates whether a cross-membrane operation should proceed
based on the permeability tier and optional cost-benefit analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from membrane.models import PermeabilityLevel


@dataclass
class GateDecision:
    """Result of a permeability gate evaluation."""

    allowed: bool
    reason: str
    token_cost_estimate: int = 0  # Estimated token cost of the operation


class PermeabilityEngine:
    """Evaluates permeability gates for cross-membrane operations.

    Design principles:
    1. Default-deny: operations are blocked unless explicitly permitted
    2. Tier-based: PUBLIC < TRUSTED < PRIVATE access control
    3. Cost-aware: tracks and estimates token cost of cross-membrane reads
    4. Trust relationships: agents can form trust relationships that grant
       TRUSTED-level access to specific peers

    For Phase 2, this integrates with:
    - Token budgets (Path 14): per-agent token budgets for membrane operations
    - Reputation (Path 6): trust scores as gating criterion
    - Cognitive digestion (Path 7): interpretation vs raw data decisions
    """

    def __init__(self):
        # Trust relationships: {agent_id: {peer_id: trust_score}}
        self.trust_map: dict[str, dict[str, float]] = {}
        # Token budgets: {agent_id: remaining_budget}
        self.token_budgets: dict[str, int] = {}
        # Default trust score
        self.default_trust: float = 0.0

    def set_trust(self, agent_id: str, peer_id: str, score: float) -> None:
        """Set trust score for a peer relationship (0.0 to 1.0)."""
        if agent_id not in self.trust_map:
            self.trust_map[agent_id] = {}
        self.trust_map[agent_id][peer_id] = max(0.0, min(1.0, score))

    def set_token_budget(self, agent_id: str, budget: int) -> None:
        """Set the token budget for an agent's membrane operations."""
        self.token_budgets[agent_id] = budget

    def consume_tokens(self, agent_id: str, cost: int) -> bool:
        """Consume tokens from an agent's budget. Returns True if successful."""
        budget = self.token_budgets.get(agent_id)
        if budget is not None and cost > budget:
            return False
        self.token_budgets[agent_id] = (budget or 0) - cost
        return True

    def evaluate(
        self,
        reader_id: str,
        owner_id: str,
        permeability: PermeabilityLevel,
        token_cost: int = 0,
        trust_threshold: float = 0.5,
    ) -> GateDecision:
        """Evaluate whether a cross-membrane read should be allowed.

        Args:
            reader_id: The agent trying to read
            owner_id: The agent that owns the data
            permeability: The permeability tier of the entry
            token_cost: Estimated token cost of the operation
            trust_threshold: Minimum trust score for TRUSTED access

        Returns:
            GateDecision with allowed/allowed and reason
        """
        # Self-read is always allowed
        if reader_id == owner_id:
            return GateDecision(
                allowed=True,
                reason="owner read",
                token_cost_estimate=token_cost,
            )

        if permeability == PermeabilityLevel.PUBLIC:
            allowed = self._check_budget(reader_id, token_cost)
            return GateDecision(
                allowed=allowed,
                reason="public tier" if allowed else "token budget exhausted",
                token_cost_estimate=token_cost,
            )

        if permeability == PermeabilityLevel.TRUSTED:
            trust = self._get_trust(reader_id, owner_id)
            if trust < trust_threshold:
                return GateDecision(
                    allowed=False,
                    reason=f"insufficient trust (score={trust:.2f}, threshold={trust_threshold})",
                    token_cost_estimate=token_cost,
                )
            allowed = self._check_budget(reader_id, token_cost)
            return GateDecision(
                allowed=allowed,
                reason=f"trusted tier (trust={trust:.2f})" if allowed else "token budget exhausted",
                token_cost_estimate=token_cost,
            )

        # PRIVATE: only owner
        return GateDecision(
            allowed=False,
            reason="private tier — owner only",
            token_cost_estimate=token_cost,
        )

    def _get_trust(self, agent_id: str, peer_id: str) -> float:
        """Get trust score for a relationship."""
        return self.trust_map.get(agent_id, {}).get(peer_id, self.default_trust)

    def _check_budget(self, agent_id: str, cost: int) -> bool:
        """Check if an agent has budget remaining."""
        if not cost:
            return True
        budget = self.token_budgets.get(agent_id)
        if budget is None:
            return True  # No budget configured = unlimited
        return budget >= cost

    def get_trust_graph(self) -> dict[str, dict[str, float]]:
        """Get the full trust graph."""
        return {k: dict(v) for k, v in self.trust_map.items()}

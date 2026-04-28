"""
Token budget enforcement in the permeability engine.

The membrane treats every cross-membrane read as having a token cost.
Agents have a per-agent budget; a read is denied at the gate when the
estimated cost would exceed the remaining budget. Agents without a
configured budget are unbounded.
"""

from __future__ import annotations

import pytest

from membrane.models import PermeabilityLevel
from membrane.permeability import GateDecision, PermeabilityEngine


@pytest.fixture
def perm() -> PermeabilityEngine:
    return PermeabilityEngine()


def test_set_and_consume_within_budget(perm):
    perm.set_token_budget("a", 100)

    assert perm.consume_tokens("a", 30) is True
    assert perm.token_budgets["a"] == 70

    assert perm.consume_tokens("a", 70) is True
    assert perm.token_budgets["a"] == 0


def test_consume_over_budget_is_rejected(perm):
    perm.set_token_budget("a", 50)

    assert perm.consume_tokens("a", 60) is False
    # budget is unchanged on rejection
    assert perm.token_budgets["a"] == 50


def test_no_budget_configured_is_unbounded(perm):
    # No set_token_budget call → consume always succeeds
    assert perm.consume_tokens("nobody", 10_000) is True


def test_evaluate_denies_public_read_over_budget(perm):
    perm.set_token_budget("reader", 10)
    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.PUBLIC,
        token_cost=50,
    )
    assert decision.allowed is False
    assert "token budget exhausted" in decision.reason
    assert decision.token_cost_estimate == 50


def test_evaluate_allows_public_read_within_budget(perm):
    perm.set_token_budget("reader", 100)
    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.PUBLIC,
        token_cost=30,
    )
    assert decision.allowed is True
    assert decision.token_cost_estimate == 30


def test_evaluate_owner_read_skips_budget_check(perm):
    perm.set_token_budget("alice", 5)
    decision = perm.evaluate(
        reader_id="alice",
        owner_id="alice",
        permeability=PermeabilityLevel.PRIVATE,
        token_cost=10_000,
    )
    assert decision.allowed is True
    assert decision.reason == "owner read"


def test_evaluate_trusted_tier_requires_both_trust_and_budget(perm):
    perm.set_trust("reader", "writer", 0.8)
    perm.set_token_budget("reader", 10)

    # Sufficient trust but exceeds budget
    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.TRUSTED,
        token_cost=20,
        trust_threshold=0.5,
    )
    assert decision.allowed is False
    assert "token budget exhausted" in decision.reason


def test_evaluate_trusted_tier_denied_on_low_trust_before_budget(perm):
    perm.set_trust("reader", "writer", 0.1)
    perm.set_token_budget("reader", 10_000)

    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.TRUSTED,
        token_cost=5,
        trust_threshold=0.5,
    )
    assert decision.allowed is False
    assert "insufficient trust" in decision.reason


def test_consume_after_zero_budget_blocks_everything(perm):
    perm.set_token_budget("reader", 0)

    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.PUBLIC,
        token_cost=1,
    )
    assert decision.allowed is False


def test_zero_cost_read_always_allowed_under_budget(perm):
    perm.set_token_budget("reader", 0)

    decision = perm.evaluate(
        reader_id="reader",
        owner_id="writer",
        permeability=PermeabilityLevel.PUBLIC,
        token_cost=0,
    )
    # zero-cost reads pass the budget gate
    assert decision.allowed is True


def test_repeated_consumes_drain_budget(perm):
    perm.set_token_budget("reader", 100)

    assert perm.consume_tokens("reader", 25) is True
    assert perm.consume_tokens("reader", 25) is True
    assert perm.consume_tokens("reader", 25) is True
    assert perm.consume_tokens("reader", 25) is True

    # Exactly empty
    assert perm.token_budgets["reader"] == 0

    # The next consume of any non-zero cost is rejected
    assert perm.consume_tokens("reader", 1) is False


def test_set_budget_resets_remaining(perm):
    perm.set_token_budget("a", 50)
    perm.consume_tokens("a", 30)
    assert perm.token_budgets["a"] == 20

    perm.set_token_budget("a", 200)
    assert perm.token_budgets["a"] == 200


def test_budget_decision_carries_cost_estimate(perm):
    perm.set_token_budget("r", 1000)
    decision: GateDecision = perm.evaluate(
        reader_id="r",
        owner_id="w",
        permeability=PermeabilityLevel.PUBLIC,
        token_cost=128,
    )
    assert decision.token_cost_estimate == 128

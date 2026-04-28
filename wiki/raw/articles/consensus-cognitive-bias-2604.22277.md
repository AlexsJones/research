---
source_url: https://arxiv.org/abs/2604.22277
ingested: 2026-04-27
---

# Multi-Agent Consensus as a Cognitive Bias Trigger in Human-AI Interaction

Lee, Lee (2026-04-24) — cs.HC

## Summary

As multi-agent AI systems become more common, users increasingly encounter not a single AI voice but a collective one. This shift introduces social dynamics — consensus, dissent, and gradual convergence — that can trigger cognitive biases and distort human judgment.

The study presents findings from a controlled experiment (N = 127) comparing three multi-agent configurations: Majority, Minority, and Consensus.

## Key Findings

1. **Consensus triggers overconfidence** — When multiple agents agree, humans are more likely to accept incorrect conclusions. This is the "false consensus effect" amplified by apparent authority.

2. **Minority dissent reduces errors** — When even one agent disagrees, humans are more skeptical and make fewer errors, but are also more likely to reject correct conclusions.

3. **Majority rule creates herd behavior** — Humans defer to agent majority even when the majority is wrong, demonstrating that multi-agent systems introduce new failure modes in human-AI collaboration.

## Implications for Multi-Agent Systems

This research reveals a critical design consideration for any multi-agent system with human oversight:
- **Consensus ≠ correctness** — Agent agreement is a social signal that humans misinterpret
- **Controlled dissent may be beneficial** — Deliberate minority opinions can improve human judgment
- **Humans need context about agent dynamics** — Transparency about how agents reached conclusions matters

## Relevance to Synthetic Membrane

For membrane designs that include human-in-the-loop oversight:
- The membrane's governance layer needs to present agent disagreements transparently
- Reputation systems shouldn't simply amplify majority opinion
- The membrane could intentionally surface dissenting opinions to counter cognitive bias
- This validates the need for [[agent-reputation-systems]] that go beyond simple consensus

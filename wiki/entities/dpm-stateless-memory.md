# Stateless Decision Memory for Enterprise AI Agents

## Summary
- Append-only event log plus task-conditioned projection at decision time
- At 20x compression, improves factual precision by +0.52 and reasoning coherence by +0.53
- 7-15x faster at binding budgets than stateful alternatives
- Logs 2 LLM calls per decision vs 83-97 for summarization

## Relevance to Membrane
Validates our event-sourcing approach for Layer 2. Proposes Deterministic Projection Memory (DPM): append-only event log plus one task-conditioned projection. Shows statelessness is the load-bearing property for enterprise deployment.

## Citations
- arXiv: https://arxiv.org/abs/2604.20158

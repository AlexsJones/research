# ContextWeaver: Selective and Dependency-Structured Memory for LLM Agents

## Summary
- Dependency-based construction linking each step to earlier steps it relies on
- Compact dependency summarization condenses reasoning paths into reusable units
- Improves pass@1 on SWE-Bench while reducing reasoning steps and token usage

## Relevance to Membrane
Supports Layer 2 (Shared Medium) design. Organizes interaction traces into a graph of reasoning steps with dependency-based construction. Improves performance while reducing token usage -- validates cognitive digestion.

## Citations
- arXiv: https://arxiv.org/abs/2604.23069

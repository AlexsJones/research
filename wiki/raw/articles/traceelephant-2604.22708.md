---
source_url: https://arxiv.org/abs/2604.22708
ingested: 2026-04-27
sha256:
---

# Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems

**Authors:** Mengzhuo Chen, Junjie Wang, Fangwen Mu, Yawen Wang, Zhe Liu, Huanxiang Feng, Qing Wang
**Published:** 2026-04-24
**Categories:** cs.MA

## Abstract

Failure attribution, i.e., identifying the responsible agent and decisive step of a failure, is particularly challenging in LLM-based multi-agent systems (MAS) due to their natural-language reasoning, nondeterministic outputs, and intricate interaction dynamics. A reliable benchmark is therefore essential to guide and evaluate attribution techniques. Yet existing benchmarks rely on partially observable traces that capture only agent outputs, omitting the inputs and context that developers actually use when debugging. We argue that failure attribution should be studied under full execution observability, aligning with real-world developer-facing scenarios where complete traces, rather than only outputs, are accessible for diagnosis. To this end, we introduce TraceElephant, a benchmark designed for failure attribution with full execution traces and reproducible environments. We then systematically evaluate failure attribution techniques across various configurations. Specifically, full traces improve attribution accuracy by up to 76% over a partial-observation counterpart, confirming that missing inputs obscure many failure causes. TraceElephant provides a foundation for follow-up failure attribution research, promoting evaluation practices that reflect real-world debugging and supporting the development of more transparent MASs.

## Key Takeaways for Synthetic Membrane

1. **Full observability is critical** — partial traces (outputs only) severely degrade attribution accuracy. Full execution traces (inputs + outputs + context) improve attribution by up to 76%.
2. **Multi-agent systems are inherently hard to debug** — natural-language reasoning, nondeterminism, and interaction dynamics create opacity.
3. **Benchmarks now exist** — TraceElephant provides a standard evaluation framework with reproducible environments.
4. **Implication for membrane design** — the membrane's event log (event sourcing layer) is not just for provenance; it's the primary observability substrate. The membrane must capture full execution traces, not just agent outputs.

---
title: TraceElephant — Full-Trace Failure Attribution Benchmark
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [benchmark, multi-agent, agent-communication, risk]
sources: [raw/articles/traceelephant-2604.22708.md]
confidence: high
---

# TraceElephant

A benchmark for failure attribution in LLM-based multi-agent systems with **full execution traces** and reproducible environments.

**Paper:** 2604.22708 — "Seeing the Whole Elephant"
**Authors:** Mengzhuo Chen, Junjie Wang, Fangwen Mu, Yawen Wang, Zhe Liu, Huanxiang Feng, Qing Wang
**Published:** 2026-04-24
**Category:** cs.MA

## What It Does

- Provides a standard benchmark for evaluating failure attribution techniques
- Uses **full execution traces** (inputs + outputs + context) rather than partial observations
- Demonstrates that full traces improve attribution accuracy by up to **76%** over partial-observation baselines
- Includes reproducible environments for consistent evaluation

## Key Finding

Missing inputs obscure many failure causes. When only agent outputs are observable (the previous standard), attribution accuracy drops dramatically. Full observability is not optional — it's essential for debugging multi-agent systems.

## Relevance to Synthetic Membrane

This validates the membrane's event sourcing design. The membrane's immutable event log naturally provides full execution traces — every message, every state change, every access decision is recorded with provenance. This makes the membrane an ideal substrate for failure attribution.

[[agent-observability]] [[event-sourcing]] [[membrane-architecture]] [[best-paths-forwards]]

---
title: Who&When — Failure Attribution Dataset for LLM Multi-Agent Systems
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [benchmark, multi-agent, risk]
sources: [raw/articles/whoandwhen-2505.00212.md]
confidence: high
---

# Who&When

The foundational dataset and benchmark for automated failure attribution in LLM multi-agent systems.

**Paper:** 2505.00212 — "Which Agent Causes Task Failures and When?"
**Authors:** Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu
**Citations:** 60 (as of April 2026)
**Repo:** https://github.com/mingyin1/Agents_Failure_Attribution

## What It Is

- Dataset of **127 LLM multi-agent systems** with fine-grained failure annotations
- Each failure tagged with responsible **agent** and **decisive step**
- Three attribution methods evaluated, with pros and cons documented

## Performance Numbers

| Method | Agent Accuracy | Step Accuracy |
|--------|---------------|---------------|
| Best | 53.5% | 14.2% |
| Some methods | Below random | Below random |
| o1 / R1 | Failed | Failed |

## Key Finding

Even state-of-the-art reasoning models (OpenAI o1, DeepSeek R1) cannot practically solve failure attribution. The problem is fundamentally hard due to natural-language reasoning, nondeterminism, and interaction dynamics. This means the membrane must provide structural scaffolding — not just rely on LLM reasoning alone.

[[traceelephant]] [[agent-observability]] [[agent-security-trust]] [[best-paths-forwards]]

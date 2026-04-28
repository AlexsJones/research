---
title: RCR-Router — Role-Aware Context Routing
created: 2026-04-26
updated: 2026-04-26
type: entity
tags: [multi-agent, agent-communication, architecture, optimization]
sources: [raw/articles/rcr-router-paper.md]
confidence: medium
---

# RCR-Router — Role-Aware Context Routing

## Overview

RCR-Router (Liu et al., 2025) addresses inefficient context routing in multi-agent LLM systems. Most systems use static or full-context routing, leading to excessive token waste. RCR-Router routes context selectively based on agent roles and structured memory.

## The Problem

Current multi-agent coordination uses either:
- **Static routing**: pre-defined which agent gets what context
- **Full-context broadcast**: every agent sees everything (wasteful, noisy)

Both approaches waste tokens and degrade performance as system scale increases.

## Solution

Role-aware routing: context is routed to agents based on:
1. **Agent role profiles** — each agent declares what context types it processes
2. **Structured memory** — context is indexed/tagged for efficient matching
3. **Dynamic routing decisions** — routing adapts as tasks evolve

## Relevance to Synthetic Membrane

This is a concrete **permeability mechanism** for the membrane:
- Agents declare roles/capabilities → membrane routes relevant information
- Structured memory enables semantic matching (not just keyword filtering)
- Routing is dynamic, adapting to task context

Complements [[token-coherence]] (when to sync) and [[selective-memory-sharing]] (what to share) by answering **where information flows**.

[[membrane-architecture]] [[protocol-design]] [[token-coherence]] [[selective-memory-sharing]]

---
title: OneManCompany — Organising Heterogeneous Agents as a Real-World Company
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [architecture, multi-agent, orchestration, person]
sources: [raw/articles/2604-22446.md]
confidence: high
---

# OneManCompany (OMC) — Organising Heterogeneous Agents as a Real-World Company

## Overview

By Zhengxu Yu, Yu Fu, Zhiyuan He, Yuxuan Huang, Lee Ka Yiu, Meng Fang, Weilin Luo, Jun Wang (2604.22446).

OMC elevates multi-agent systems from static pipelines to self-organising, self-improving AI organisations by introducing an organisational layer decoupled from individual agent capabilities.

## Core Components

### 1. Talents — Portable Agent Identities

Skills, tools, and runtime configurations are encapsulated into portable agent identities called **Talents**. A Talent is the organisational view of an agent — what it can do, not how it does it. This mirrors how human companies manage employees by role rather than internal psychology.

### 2. Talent Market — On-Demand Recruitment

A community-driven **Talent Market** enables organisations to recruit agents on-demand, closing capability gaps dynamically during execution. Agents can join/leave as organisational needs change.

### 3. Typed Organisational Interfaces

Interfaces abstract over heterogeneous backends, allowing agents from different frameworks to participate in the same organisation. This is the membrane's cross-framework interoperability problem at the organisational level.

### 4. Explore-Execute-Review (E²R) Tree Search

Organisational decision-making via a unified hierarchical loop:
- **Explore**: Decompose tasks top-down into accountable units
- **Execute**: Agents carry out their assigned tasks
- **Review**: Aggregate outcomes bottom-up to drive systematic review and refinement

Provides formal guarantees on termination and deadlock freedom while mirroring enterprise feedback mechanisms.

## Performance

- **84.67% success rate on PRDBench**, surpassing SOTA by 15.48 percentage points
- Cross-domain case studies demonstrate generality

## Membrane Relevance

OMC validates and extends several membrane concepts:

- **Organisational layer**: The membrane should support organisational abstractions, not just technical coordination. OMC shows this layer matters.
- **Talent as agent identity**: Maps to [[agent-identity-cryptography]] — agents have capabilities that can be verified and delegated
- **Talent Market as discovery**: Maps to [[agent-discovery-registry]] — agents need to be findable and recruitable
- **Typed interfaces**: Maps to [[framework-integration]] — cross-framework interoperability via typed contracts
- **E²R loop**: Maps to [[agent-governance]] — structured review cycles with formal guarantees

## Relationship to Membrane Architecture

OMC's organisational layer sits **above** the membrane's coordination layer. The membrane provides the communication fabric (shared state, messaging, permeability) while OMC provides the organisational structure (roles, recruitment, review cycles). Together they form a complete picture: the membrane is the nervous system, OMC is the organisational chart.

## Related

- [[agent-governance]] — E²R loop provides structured governance cycles
- [[agent-discovery-registry]] — Talent Market is a discovery mechanism
- [[framework-integration]] — Typed interfaces enable cross-framework participation
- [[agent-identity-cryptography]] — Talents encapsulate agent capabilities
- [[evovagent]] — Evolvable agents with skill learning (related but different scope)
- [[best-paths-forwards]] — Organisational layer as potential Phase 3 addition

[[agent-governance]] [[agent-discovery-registry]] [[framework-integration]] [[evovagent]] [[best-paths-forwards]]

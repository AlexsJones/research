---
title: PASS — Provenanced Access Subaccounts for AI Agent Wallets
created: 2026-04-27
updated: 2026-04-27
type: entity
tags: [protocol, architecture, multi-agent]
sources: [raw/articles/pass-ai-wallets-2604.22602.md]
confidence: medium
---

# PASS — Provenanced Access Subaccounts for AI Agent Wallets

Jay Yu, Shunfan Zhou, Hang Yin (2026-04-24) — [arXiv:2604.22602](https://arxiv.org/abs/2604.22602)

## What It Is

PASS introduces a provenanced access model for blockchain wallets that provides fine-grained delegation without surrendering unilateral control. Designed specifically for emerging settings like AI agent wallets, organizational custody, and enterprise payroll.

## Key Features

- **Fine-grained delegation**: Grant specific capabilities (spend X, access Y) without full key access
- **Provenance tracking**: Every access grant is recorded with who granted it, when, and why
- **Revocation**: Access can be revoked without rotating the entire key
- **Auditability**: Full history of who accessed what and when

## Relevance to Synthetic Membrane

### Resource Delegation Pattern
Agents may need to grant each other access to tools, data, or compute resources. PASS provides a model for this:
- **Scoped access**: Agent A grants Agent B read-only access to a specific data store
- **Time-bounded**: Access expires after a duration or after the task completes
- **Revocable**: Agent A can immediately revoke Agent B's access if it behaves maliciously
- **Auditable**: Every delegation is recorded for [[agent-observability]] and [[failure-attribution]]

### Membrane Integration
This maps to the permeability layer's access control — but applied to resources (tools, data, compute) rather than information flow.

## Limitations

- Currently designed for financial/wallet resources, not general-purpose agent resources
- Blockchain dependency for the provenance layer
- May be overkill for lightweight in-membrane delegation

## Related

- [[erc-8004]] — Blockchain agent identity; could provide the identity layer for PASS
- [[agent-identity-cryptography]] — Identity verification prerequisite for delegation
- [[gated-permeability]] — Similar access-control principle for information flow
- [[agnt2]] — Blockchain agent economies; resource exchange between agents

[[erc-8004]] [[gated-permeability]] [[agnt2]]

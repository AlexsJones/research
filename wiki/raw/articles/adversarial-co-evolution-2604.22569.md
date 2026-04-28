---
source_url: https://arxiv.org/abs/2604.22569
ingested: 2026-04-27
---

# Adversarial Co-Evolution of Malware and Detection Models: A Bilevel Optimization Perspective

Jurečková, Jureček, Kozák, Lórencz (2026-04-24) — cs.CR

## Summary

Machine learning-based malware detectors are increasingly vulnerable to adversarial examples. Traditional defenses, such as one-shot adversarial training, often fail against adaptive attackers who use reinforcement learning to bypass detection.

The paper proposes a robust defense framework based on bilevel optimization, explicitly modeling the strategic interaction between a defender and an adaptive attacker.

## Key Findings

1. **Static defenses fail**: One-shot adversarial training is insufficient against attackers that adapt
2. **Bilevel optimization works**: Modeling the defender-attacker interaction as a nested optimization problem produces more robust defenses
3. **Co-evolution is the reality**: Attackers and defenders are locked in an arms race; defenses must be designed to evolve alongside attacks

## Relevance to Synthetic Membrane

This directly applies to the membrane's immune-inspired defense layer:
- The membrane cannot rely on static detection rules
- Defense must co-evolve with threat patterns
- Bilevel optimization framework applies to agent security: the membrane defends knowing that malicious agents optimize against it
- Validates the need for adaptive, learning-based security ([[immune-inspired-defense]])

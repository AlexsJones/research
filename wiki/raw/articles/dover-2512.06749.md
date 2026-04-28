---
source_url: https://arxiv.org/abs/2512.06749
ingested: 2026-04-27
sha256:
---

# DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems

**Authors:** Ming-Jie Ma, Jue Zhang, Fangkai Yang, Yu Kang, Qingwei Lin, S. Rajmohan, Dongmei Zhang
**Published:** 2025-12
**Repo:** https://aka.ms/DoVer

## Abstract

LLM-based multi-agent systems are challenging to debug because failures often arise from long, branching interaction traces. The prevailing practice is to leverage LLMs for log-based failure localization, attributing errors to a specific agent and step. However, this paradigm has two key limitations: (i) log-only debugging lacks validation, producing untested hypotheses, and (ii) single-step or single-agent attribution is often ill-posed, as multiple distinct interventions can independently repair the failed task. We introduce DoVer, an intervention-driven debugging framework, which augments hypothesis generation with active verification through targeted interventions (e.g., editing messages, altering plans). Rather than evaluating on attribution accuracy, we focus on measuring whether the system resolves the failure or makes quantifiable progress toward task success. DoVer flips 18-28% of failed trials into successes, achieves up to 16% milestone progress, and validates or refutes 30-60% of failure hypotheses. DoVer also performs on different frameworks (AG2, Magnetic-One).

## Key Innovation: Intervention-Based Verification

- **Beyond attribution:** Don't just identify the problem — verify by intervening
- **Active debugging:** Edit messages, alter plans, re-run to see if failure is fixed
- **Outcome-oriented:** Measure success by whether the system works, not just attribution accuracy
- **18-28% of failed trials flipped to success** through intervention

## Implication for Membrane

The membrane could support active debugging:
- **Intervention hooks:** The membrane can replay scenarios with modified parameters
- **Counterfactual simulation:** "What if Agent A had shared X instead of Y?"
- **The membrane IS the intervention surface** — you modify shared state, message routing, permeability rules, and observe effects

This elevates the membrane from passive observation to active debugging infrastructure.

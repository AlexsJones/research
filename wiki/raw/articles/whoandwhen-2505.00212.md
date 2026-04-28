---
source_url: https://arxiv.org/abs/2505.00212
ingested: 2026-04-27
sha256:
---

# Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems

**Authors:** Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu
**Published:** 2025 (Semantic Scholar)
**Citations:** 60
**Dataset:** Who&When (127 LLM multi-agent systems, fine-grained failure annotations)
**Repo:** https://github.com/mingyin1/Agents_Failure_Attribution

## Abstract (from Semantic Scholar)

Failure attribution in LLM multi-agent systems — identifying the agent and step responsible for task failures — provides crucial clues for systems debugging but remains underexplored and labor-intensive. In this paper, we propose and formulate a new research area: automated failure attribution for LLM multi-agent systems. We introduce the Who&When dataset, comprising extensive failure logs from 127 LLM multi-agent systems with fine-grained annotations linking failures to specific agents and decisive error steps. Using the Who&When, we develop and evaluate three automated failure attribution methods, summarizing their corresponding pros and cons. The best method achieves 53.5% accuracy in identifying failure-responsible agents but only 14.2% in pinpointing failure steps, with some methods performing below random. Even SOTA reasoning models, such as OpenAI o1 and DeepSeek R1, fail to achieve practical usability. These results highlight the task's complexity and the need for further research in this area.

## Key Findings

- **Agent-level accuracy:** 53.5% best case (finding WHICH agent failed)
- **Step-level accuracy:** 14.2% best case (finding WHICH STEP failed)
- **Even o1 and R1 fail** — the problem is genuinely hard, not solved by bigger models
- **127 systems** in the dataset — broad coverage
- **Below-random performance** for some methods — the task is not trivial

## Implication for Membrane

Failure attribution is a key use case for the membrane's observability layer. If even o1 and R1 can't reliably attribute failures, the membrane needs to provide rich structural context (event logs, causal traces, provenance) that makes attribution tractable.

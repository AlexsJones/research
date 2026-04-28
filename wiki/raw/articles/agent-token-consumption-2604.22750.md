---
source_url: https://arxiv.org/abs/2604.22750
ingested: 2026-04-27
---

# How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks

**Authors:** Longju Bai, Zhemin Huang, Xingyao Wang, Jiao Sun, Rada Mihalcea, Erik Brynjolfsson, Alex Pentland, Jiaxin Pei

**Published:** 2026-04-24
**Categories:** cs.CL, cs.CY, cs.HC, cs.SE
**arXiv:** 2604.22750

## Abstract

The wide adoption of AI agents in complex human workflows is driving rapid growth in LLM token consumption. When agents are deployed on tasks that require a significant amount of tokens, three questions naturally arise: (1) Where do AI agents spend the tokens? (2) Which models are more token-efficient? and (3) Can agents predict their token usage before task execution? In this paper, we present the first systematic study of token consumption patterns in agentic coding tasks. We analyze trajectories from eight frontier LLMs on SWE-bench Verified and evaluate models' ability to predict their own token costs before task execution.

## Key Findings

1. **Agentic tasks are uniquely expensive:** Consume 1000x more tokens than code reasoning and code chat, with input tokens rather than output tokens driving the overall cost
2. **Token usage is highly variable:** Runs on the same task can differ by up to 30x in total tokens; higher token usage does NOT translate into higher accuracy — accuracy often peaks at intermediate cost and saturates at higher costs
3. **Model efficiency varies substantially:** Kimi-K2 and Claude-Sonnet-4.5 consume over 1.5 million more tokens than GPT-5 on the same tasks
4. **Human difficulty vs. actual cost:** Task difficulty rated by human experts only weakly aligns with actual token costs
5. **Poor self-prediction:** Frontier models fail to accurately predict their own token usage (correlations up to 0.39) and systematically underestimate real token costs

## Relevance to Synthetic Membrane

- **Communication cost budgeting:** If agentic tasks consume 1000x more tokens, inter-agent communication via the membrane must be extremely cost-efficient
- **Input tokens dominate:** This validates the need for compact wire formats and lazy loading ([[mcp-efficiency-optimizations]])
- **Accuracy-cost tradeoff:** Membrane should enable agents to achieve goals at intermediate cost — the "sweet spot" rather than maximum communication
- **Token economics as membrane constraint:** The membrane must be designed with token efficiency as a first-class concern, not an afterthought
- **Validation of gated permeability:** Since more communication ≠ better results, default-deny permeability ([[gated-permeability]]) is economically justified

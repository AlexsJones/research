---
source_url: https://arxiv.org/abs/2604.22748
ingested: 2026-04-27
---

# Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond

**Authors:** Meng Chu, Xuan Billy Zhang, Kevin Qinghong Lin, Lingdong Kong, Jize Zhang, Teng Tu, Weijian Ma, Ziqi Huang, Senqiao Yang, Wei Huang, Yeying Jin, Zhefan Rao, Jinhui Ye, Xinyu Lin, Xichen Zhang, Qisheng Hu, Shuai Yang, Leyang Shen, Wei Chow, Yifei Dong, Fengyi Wu, Quanyu Long, Bin Xia, Shaozuo Yu, Mingkang Zhu, Wenhu Zhang, Jiehui Huang, Haokun Gui, Haoxuan Che, Long Chen, Qifeng Chen, Wenxuan Zhang, Wenya Wang, Xiaojuan Qi, Yang Deng, Yanwei Li, Mike Zheng Shou, Zhi-Qi Cheng, See-Kiong Ng, Ziwei Liu, Philip Torr, Jiaya Jia

**Published:** 2026-04-24
**Categories:** cs.AI
**arXiv:** 2604.22748

## Abstract

As AI systems move from generating text to accomplishing goals through sustained interaction, the ability to model environment dynamics becomes a central bottleneck. Agents that manipulate objects, navigate software, coordinate with others, or design experiments require predictive environment models, yet the term world model carries different meanings across research communities. We introduce a "levels x laws" taxonomy organized along two axes. The first defines three capability levels: L1 Predictor, which learns one-step local transition operators; L2 Simulator, which composes them into multi-step, action-conditioned rollouts that respect domain laws; and L3 Evolver, which autonomously revises its own model when predictions fail against new evidence. The second identifies four governing-law regimes: physical, digital, social, and scientific. These regimes determine what constraints a world model must satisfy and where it is most likely to fail. Using this framework, we synthesize over 400 works and summarize more than 100 representative systems spanning model-based reinforcement learning, video generation, web and GUI agents, multi-agent social simulation, and AI-driven scientific discovery. We analyze methods, failure modes, and evaluation practices across level-regime pairs, propose decision-centric evaluation principles and a minimal reproducible evaluation package, and outline architectural guidance, open problems, and governance challenges. The resulting roadmap connects previously isolated communities and charts a path from passive next-step prediction toward world models that can simulate, and ultimately reshape, the environments in which agents operate.

## Taxonomy: Levels x Laws

### Capability Levels
- **L1 Predictor:** Learns one-step local transition operators (what happens next given current state)
- **L2 Simulator:** Composes transitions into multi-step, action-conditioned rollouts that respect domain laws
- **L3 Evolver:** Autonomously revises its own model when predictions fail against new evidence

### Governing-Law Regimes
- **Physical:** Governed by physics (robotics, manipulation, navigation)
- **Digital:** Governed by software/API semantics (GUI agents, web agents)
- **Social:** Governed by social dynamics, norms, and agent interactions (multi-agent societies)
- **Scientific:** Governed by scientific method, experimentation, hypothesis testing

## Key Findings

- Synthesizes 400+ works across previously isolated research communities
- Surveys 100+ representative systems
- Analyzes failure modes across level-regime pairs
- Proposes decision-centric evaluation principles
- Outlines architectural guidance, open problems, and governance challenges
- Charts path from passive prediction to active environment reshaping

## Relevance to Synthetic Membrane

The "Social" regime is directly relevant — it covers multi-agent social simulation and coordination. The L1-L3 taxonomy maps to membrane capabilities:
- **L1 → Permeability layer:** Predict what information an agent wants to share/receive
- **L2 → Coordination layer:** Multi-step coordination patterns (swarm formation, task delegation)
- **L3 → Adaptive membrane:** Membrane that evolves its rules based on interaction outcomes

The "social" regime's governing laws (norms, social dynamics) directly inform the membrane's permeability rules and reputation systems.

# Incident Management Coordination Models: ICS, NIMS, SRE, and the Primitives Agents Are Missing

**Date:** 2026-05-05
**Researcher:** Claude Code (delegated via `claude -p`)
**Cycle:** 0002

## Context

Cycle 0001 established that every current agent framework reduces to message passing or graph orchestration, and that production-scale critiques converge on the same symptom: disconnected agents, separate contexts, broken governance at scale. The synthetic membrane proposes a six-layer answer to this gap. But before validating that architecture, we need a reference model of what *good* operational coordination actually looks like — not in the abstract, but in domains where humans have been forced to solve it under life-and-death constraints for fifty years.

That domain is incident management. Wildfires in 1970s California, the 9/11 multi-agency response, Google's first major service outages, every ransomware tabletop run since 2020 — each has produced a layer of formalised coordination doctrine. ICS, NIMS, ITIL, and the SRE incident-management approach (IMAG) are the result. They are not theoretical models. They are battle-tested protocols that explicitly answer the question: *how do independent actors with separate contexts coordinate around an emerging situation without a single brain in charge?*

This entry surveys those frameworks, extracts their coordination primitives, maps them to the membrane layers, and identifies what carries over to agent systems and what doesn't.

## Key Findings

### Finding 1: ICS solved the coordination problem in 1970, and its primitives are still load-bearing

The Incident Command System emerged from FIRESCOPE in California after the 1970 wildfires, where fire departments from multiple jurisdictions arrived at the same incident with incompatible radios, conflicting command structures, and no shared map. The post-mortem identified the failures as *organisational*, not tactical. ICS is the result.

The ICS primitives that matter for agent coordination are:

- **Modular organisation.** The ICS structure expands top-down based on incident size and complexity. A small fire might be one person handling Operations and Planning together; a major disaster expands to hundreds. Sections that aren't needed are simply not filled. ([Wikipedia — ICS](https://en.wikipedia.org/wiki/Incident_Command_System))
- **Unity of command.** Every individual reports to exactly one supervisor. This eliminates conflicting directives from multiple bosses — a separate concept from the *chain of command*, which describes the overall hierarchy. ([USDA ICS 200 Lesson 2](https://www.usda.gov/sites/default/files/documents/ICS200Lesson02.pdf))
- **Span of control.** Any single person should supervise between three and seven subordinates, with five being the canonical ratio. This is a hard limit on cognitive load, and it is *the* mechanism that forces the modular structure to expand. ([Splunk — ICS](https://www.splunk.com/en_us/blog/learn/incident-command-system-ics.html))
- **Common terminology.** Plain language, no agency-specific codes, jargon, or radio codes. Functional roles and resource types have standard names across all participating agencies. ([EMSI — 14 NIMS Management Characteristics](https://www.emsics.com/resources/reference-documents/14-management-characteristics-of-nims/))
- **Unified Command.** When multiple jurisdictions or agencies have authority, each gets a seat at the command table; they jointly set objectives without surrendering authority over their own resources.
- **Management by Objectives.** Each operational period has explicit objectives that drive the Incident Action Plan (IAP). The IAP is written, distributed, and used to pre-coordinate actions across sections without runtime back-and-forth.

The deep observation: ICS does *not* coordinate by routing every decision through the Incident Commander. It coordinates by **structuring the medium of work** — common terminology, written objectives, modular roles — so that local autonomy is preserved while global coherence emerges. The IC sets objectives; sections execute. This is the opposite of orchestration.

### Finding 2: NIMS makes ICS interoperable across agencies — and the interoperability layer is the hard part

NIMS, established by HSPD-5 in 2003 after 9/11, takes ICS and standardises it across all levels of US government, private sector, and NGOs. Its 14 Management Characteristics formalise the primitives above and add explicit coordination machinery: Common Terminology, Modular Organization, Management by Objectives, Incident Action Planning, Manageable Span of Control, Incident Facilities and Locations, Comprehensive Resource Management, Integrated Communications, Establishment and Transfer of Command, Unified Command, Chain of Command and Unity of Command, Accountability, Dispatch/Deployment, and Information and Intelligence Management. ([FEMA — NIMS Components](https://www.fema.gov/emergency-managers/nims/components))

NIMS' Multi-Agency Coordination System (MACS) introduces three coordination structures that operate at different scopes:

1. **ICS** — on-scene tactical coordination
2. **EOC (Emergency Operations Center)** — regional resource and policy coordination
3. **MAC Groups** — multi-agency policy coordination at the strategic level

The critical insight: a single coordination structure cannot cover all scopes. NIMS explicitly separates tactical, operational, and strategic coordination into distinct structures with different cadences and different participants. ([Tidal Basin — Understanding NIMS](https://www.tidalbasingroup.com/understanding-the-national-incident-management-system-nims/))

Interoperability — the part that NIMS adds on top of ICS — is achieved through *Integrated Communications*: a common communications plan and interoperable processes that span voice and data. Crucially, NIMS does *not* try to unify the communication systems themselves. Each agency keeps its radios, dispatchers, and ops culture. Interoperability is achieved at a higher layer — common terminology, common forms, common objectives, common reporting cadence. ([EMSI 14 Characteristics PDF](http://www.emsics.com/wp-content/uploads/2020/06/EMSI-14-Principles-of-NIMS.pdf))

This is directly relevant to the membrane thesis. The framework that has survived fifty years of multi-agency disaster response does not solve coordination by forcing everyone onto a shared message bus. It solves it by establishing a **shared structured medium** (terminology, IAP, COP) on top of agency-specific channels.

### Finding 3: Distributed Situation Awareness reframes coordination as a property of the system, not the team

The classical Endsley model treats situation awareness (SA) as a cognitive state inside an individual operator: perception → comprehension → projection. That model assumes a single mind. Multi-agency response breaks it.

Stanton, Salmon, and Walker's Distributed Situation Awareness (DSA) model reframes SA as an **emergent property of a joint cognitive system** — humans, technologies, protocols, and procedures together. SA is "activated knowledge for a specific task within a system at a specific time by specific agents." It does not live in any one head. It lives in the interaction. ([Salmon, Stanton & Jenkins — DSA book](https://www.routledge.com/Distributed-Situation-Awareness-Theory-Measurement-and-Application-to/Salmon-Stanton-Jenkins/p/book/9781138073852); [Stanton et al., Distributed situation awareness in dynamic systems](https://bura.brunel.ac.uk/bitstream/2438/1419/1/Distributed_situation_awareness_in_dynamic_systems_Stanton_et_al.pdf))

A key empirical finding from multi-agency exercise studies: agencies hold *complementary, not redundant*, information. Police, fire, and ambulance at the same scene have different mental models, different priorities, and different lexicons. Forcing them onto a single shared model is both impossible and counterproductive. What works is *transactive* awareness — knowing who knows what, and being able to query or signal across boundaries. ([ScienceDirect — Situation Awareness in multi-agency emergency response](https://www.sciencedirect.com/science/article/abs/pii/S2212420920300443))

This maps directly onto the membrane's permeability layer. Permeability is not "everyone sees everything." It is "structured, gated diffusion across boundaries that preserve agency-internal models."

The Common Operating Picture (COP) is the operational artefact that DSA produces. A COP is "a continuously updated overview of an incident compiled throughout an incident's life cycle from data shared between integrated communication, information management, and intelligence and information sharing systems." It is *not* a database. It is a shared, updating representation that any participant can read, contribute to, and rely on. Reported impact: 34% reduction in incident response time, 94% SLA adherence in industries that adopt one. ([Wikipedia — Common Operational Picture](https://en.wikipedia.org/wiki/Common_operational_picture); [DHS — Common Operating Picture for Emergency Responders](https://www.dhs.gov/publication/common-operating-picture-emergency-responders))

### Finding 4: SRE's IMAG is ICS adapted for software, and its core artefact is the living incident document

Google's Incident Management at Google (IMAG) is, by their own admission, ICS rebadged for software incidents. The "three Cs" — coordinate, communicate, control — and the role split (Incident Commander, Communications Lead, Operations Lead) come straight from the wildfire playbook. ([Google SRE — Managing Incidents](https://sre.google/sre-book/managing-incidents/))

The most important detail in the SRE Book chapter, for our purposes, is this:

> "The incident commander's most important responsibility is to keep a living incident document, which can live in a wiki but should ideally be editable by several people concurrently."

Google SRE explicitly avoids hosting the incident doc on the same systems they're trying to debug — they use Google Sites rather than Google Docs for exactly this reason. The living document is the primary coordination artefact. Roles, hypotheses, current actions, timeline, and decisions all converge on it. Multiple people edit it simultaneously. It is the operational equivalent of the IAP and the COP collapsed into one writable surface. ([SRE Incident Management Guide](https://sre.google/static/pdf/IncidentManagementGuide.pdf))

This is the closest concrete prior art for what the membrane's Shared Medium layer should provide. It is not a message log. It is not a stream. It is a *concurrently-editable structured surface* that is the source of truth for the incident.

ITIL's "war room" — virtual or physical — fills the same function for IT service management, with a Major Incident Manager, technicians, business representatives, and a communications coordinator collaborating in real time. ([Alloy Software — Major Incidents Management in ITIL 4](https://www.alloysoftware.com/blog/major-incident-management-itil-4/))

### Finding 5: Hypothesis-driven investigation is a first-class coordination primitive

The dominant pattern in modern security incident triage is *hypothesis-driven investigation*: rather than starting from "is this an incident?", investigators form testable assertions and eliminate occurrences that can be logically explained, leaving events with no clear explanation as the candidates for genuine threats. ([Graylog — The Importance of Triage in Incident Response](https://graylog.org/post/the-importance-of-triage-in-incident-response/); [SecurityScorecard — What Is Triage in Cybersecurity Incident Response](https://securityscorecard.com/blog/what-is-triage-in-cybersecurity-incident-response/))

This pattern shows up in three forms:

- **Lead-driven (structured) hunting** — hypothesis is anchored on a specific IOC or intelligence input
- **Hypothesis-driven hunting** — analysts pose "what if X is happening?" and investigate
- **Anomaly-driven hunting** — deviations from baseline trigger formation of explanatory hypotheses

Microsoft's Defender Copilot, in production since late 2025, makes this explicit: the agent "retrieves and analyzes large volumes of security data (up to ~100MB), correlates signals across telemetry sources, and iteratively explores hypotheses to surface patterns and threats that might otherwise go unnoticed." Microsoft Defender Experts for Hunting reports now include an "Emerging threats" section detailing the proactive, hypothesis-based hunts conducted in the customer environment. ([Microsoft Learn — Triage and investigate incidents with guided responses](https://learn.microsoft.com/en-us/defender-xdr/security-copilot-m365d-guided-response); [Microsoft — Security Copilot in Defender, agentic AI](https://techcommunity.microsoft.com/blog/microsoftthreatprotectionblog/security-copilot-in-defender-empowering-the-soc-with-assistive-and-autonomous-ai/4503047))

Hypotheses are the unit of work in operational coordination. They have lifecycle (open → testing → confirmed/rejected), they have evidence attached, they are owned and assigned, and they branch. None of the current general-purpose agent frameworks treats hypotheses as first-class objects. They treat *messages* and *tasks* as first-class. This is a specific, measurable gap.

### Finding 6: AI agents in the SOC are arriving, but as point assistants, not coordinated swarms

The 2025 academic surveys converge on a common picture. The MDPI survey "AI-Augmented SOC: A Survey of LLMs and Agents for Security Automation" (Nov 2025) reviewed 500+ papers and 100 selected sources, mapping AI use across eight SOC functions: log summarization, alert triage, threat intelligence, ticket handling, incident response, report generation, asset discovery, vulnerability management. It proposes a five-level Capability Maturity Model for progressive AI autonomy in SOCs. ([MDPI — AI-Augmented SOC](https://www.mdpi.com/2624-800X/5/4/95))

AgentSOC (arXiv:2604.20134) is a multi-layer agentic AI framework reaching ~506 ms end-to-end reasoning loops, designed for real-time SOC use. ([AgentSOC arXiv preprint](https://arxiv.org/html/2604.20134))

The empirical study "LLMs in the SOC" (arXiv:2508.18947) reports on actual human-AI collaboration patterns in production security operations. ([LLMs in the SOC](https://arxiv.org/html/2508.18947v1))

But the architectural pattern across all of these is the same: **a single agent (or a small orchestrated group) augments a human analyst on a single SOC function**. There is no equivalent of a Unified Command for AI agents. There is no equivalent of an IAP for an AI-handled incident. There is no shared medium where multiple AI agents (alert triage, threat intel, hunting, response) coordinate hypotheses across the lifecycle of a single incident. The agents do not sense each other. They do not hand off cleanly. They do not share evidence in a structured medium.

This is exactly the gap the membrane targets, restated in operational terms.

### Finding 7: Modelling and simulating ICS as a multi-agent system has been done — but not for AI agent coordination

Prior computational work has modelled ICS itself as a multi-agent system: coalition formation for resource hierarchies, sequential characteristic function games for command chains ([Springer — Modelling a chain of command in the ICS](https://link.springer.com/article/10.1007/s10472-023-09878-7)), human-in-the-loop disaster simulators with rules elicited from responder interviews ([ResearchGate — Modelling and simulation of inter- and intra-organisational communication](https://www.researchgate.net/publication/244924837_Modelling_and_simulation_of_inter-_and_intra-organisational_communication_and_coordination_in_emergency_response)), and IEEE work on model-based simulation augmenting ICS for disaster response ([IEEE — Using model-based simulation for augmenting ICS](https://ieeexplore.ieee.org/document/7822336/)).

This body of work treats ICS as a *target system to simulate*. It does not treat ICS as *the architectural pattern that AI agents should adopt*. That inversion is the contribution this research project can make.

## Mapping ICS/NIMS to the Synthetic Membrane

| Membrane Layer | ICS / NIMS / SRE Equivalent | What It Provides |
|---|---|---|
| **Governance (L-1)** | Authorities Having Jurisdiction; Unified Command; ITIL OLAs | Who has authority over what, joint decision rights without surrendering agency control |
| **Discovery (L0)** | Check-in procedure; resource typing; ICS Form 211 | Knowing who is on-scene, what capabilities they bring, where they are stationed |
| **Permeability (L1)** | Common Terminology; integrated communications plan | Controlled diffusion across agency boundaries — *what* crosses, in *what* form |
| **Shared Medium (L2)** | Common Operating Picture; SRE living incident doc; IAP | A concurrently-editable structured surface that all participants can sense and contribute to |
| **Coordination (L3)** | Span of control; modular organisation; IAP objectives; hypothesis lifecycle | Local autonomy under global objectives; bounded fan-out; hypothesis-driven branching |
| **Immune (cross-cutting)** | After-Action Review; postmortem culture; accountability characteristic | Detecting drift, surfacing failure, learning across incidents |

Three observations from this mapping:

1. **The Shared Medium layer is the most underspecified in current agent frameworks and the most operationalised in human incident response.** The COP and the SRE living document are direct, working instances of what L2 needs to be. Neither LangGraph state nor A2A messages are equivalent — both are orchestrator-owned or transactional, not ambient and editable.

2. **Span of control is a coordination primitive agent frameworks have ignored.** Five subordinates per supervisor exists because human cognition under stress can't manage more. LLM agents have analogous limits — context window pressure, attention dilution across many parallel sub-agents — but no current framework treats span of control as a first-class constraint that triggers structural reorganisation.

3. **Common terminology is upstream of message passing.** A2A and ANP standardise the *envelope*; ICS standardises the *vocabulary*. Without shared terminology, message passing protocols just transmit ambiguity faster. MAST's "wrong assumption" and "info withholding" failure modes from cycle 0001 are essentially terminology failures — agents using the same words to mean different things.

## Real-World Scenarios for Validating Agent Coordination

Four candidate scenarios, ranked by how cleanly they exercise the membrane primitives:

1. **Ransomware incident response (highest coordination demand).** Detection (EDR agent), containment (network agent), forensics (DFIR agent), threat intel (TI agent), comms (stakeholder agent), legal/regulatory (compliance agent) all need to coordinate around a single living incident under hard time pressure. Hypotheses (which family? which initial vector? which lateral path?) branch and converge. This is the canonical test case.

2. **IT cascading-failure outage (high coordination, lower stakes).** Multiple services degrade simultaneously; root cause is shared. Each service has its own oncall agent. Coordination is hypothesis-driven (is it the database? the load balancer? a deployment?). Direct analog of SRE IMAG.

3. **Healthcare code blue / mass casualty (well-documented human protocols).** ICS is mandatory in US hospitals under NIMS; protocols are explicit. Useful for benchmarking agent coordination against a known-good human baseline, but harder to instrument.

4. **Natural disaster multi-agency response (highest fidelity to NIMS, hardest to operationalise for agents).** Validates the framework but the operational substrate (sensors, actuators, real-world action) is not yet agent-ready.

Recommendation: scenario 1 (ransomware) is the validation case for cycle 3+ work. It maximises coordination load, has rich existing telemetry, and produces measurable outcomes (time-to-containment, MTTD, false-positive rate).

## Relevance to Synthetic Membrane

Cycle 0001 established the gap. Cycle 0002 establishes that **the gap has already been solved for humans**, and the solution has a name (ICS/NIMS/IMAG), a fifty-year track record, and a documented set of primitives. The membrane is not inventing operational coordination. It is asking what it would take to make those primitives available to AI agents that share a runtime instead of a radio channel.

The strongest takeaways for the membrane thesis:

- **Coordination is not orchestration.** ICS works by structuring the medium, not by routing every decision through a central node. The Incident Commander sets objectives; the modular structure executes locally. This is the architectural pattern the membrane should embody. LangGraph-style orchestration is the antipattern.

- **The Shared Medium layer is concretely instantiable.** The COP and the SRE living incident doc are working examples. The membrane's L2 should be a concurrently-editable structured surface with hypothesis lifecycles, evidence attachment, and role-aware permeability — not a message log, not an event bus.

- **Common terminology precedes communication.** Before agents can coordinate, they need shared types for the operational objects: incident, hypothesis, evidence, action, role, objective. This is upstream of A2A or MCP. It is the first thing the membrane has to standardise.

- **Span of control is a missing constraint in agent systems.** Modular reorganisation under load — splitting one agent's job into a hierarchy when fan-out exceeds five — is something the coordination layer should handle automatically.

## Relevance to Sympozium

Sympozium's role is to be the runtime where these primitives become real. Concrete implications:

1. **The Sympozium control plane should host an Incident object as a first-class CRD.** Not a workflow, not a graph — an Incident. With status, IAP, COP, hypothesis list, role assignments, and timeline. This is the K8s-native form of the SRE living document.

2. **Hypotheses should be a first-class CRD.** With lifecycle states (proposed, testing, confirmed, rejected, superseded), evidence references, owners, and parent/child relationships. Agents subscribe to hypothesis events the way they subscribe to pod events.

3. **Agent capability registration should be ICS-typed.** Not "this agent can call these tools" but "this agent fills these operational roles" (Operations Lead, Comms Lead, Forensics, Threat Intel). Capability-based routing then maps incident objectives to agent capacity.

4. **Span-of-control auto-expansion.** When a single agent's hypothesis fan-out or evidence load exceeds a threshold, Sympozium should spawn a sub-coordinator agent and re-shard the work. This is the modular organisation principle, automated.

5. **After-Action Review as part of the lifecycle.** Every Incident produces a structured postmortem artefact that updates the Common Terminology and the IAP templates. This is the immune layer feeding the governance layer.

The pitch sharpens: Sympozium is *the Incident Command System for AI agents*, implemented on Kubernetes. Cycle 0001 said the gap exists. Cycle 0002 says the gap already has a fifty-year-old solution, and we know exactly what the primitives are.

## Open Questions

1. **Span of control for LLM agents — what is the actual ratio?** Five is the human number. Is the LLM equivalent the same, smaller (because of context pressure), or larger (because cognitive load works differently)? This is empirically testable.

2. **Hypothesis representation.** Hypotheses in human IR are typically natural-language assertions. Should agent-shared hypotheses be structured (predicate logic, ATT&CK technique IDs), unstructured (text), or hybrid? Microsoft Defender Copilot does this implicitly — what is the explicit schema?

3. **How does Unified Command translate when "agencies" are AI agents from different vendors?** Multi-agent runtimes will have to span Anthropic, OpenAI, Google, open-weights, and custom agents. NIMS solved interoperability at the *protocol* layer (common terminology, common forms). What is the agent equivalent — beyond A2A's transport layer?

4. **What is the AI equivalent of an After-Action Review?** Postmortems update human procedures. What updates an AI's procedures? Fine-tuning? A shared memory store? Updates to the Common Terminology dictionary? This connects to cycle 5 work on token economics and persistence.

5. **How does the COP render for agents?** Humans need a visual COP. Agents arguably need a structured one. But is there value in a *shared* COP that both render from? This may be where the membrane interfaces with human operators most directly.

6. **What cadence does the IAP run on for agent incidents?** Human IAPs run on operational-period boundaries (typically 12 or 24 hours). AI agents may need much faster cadences. Is the IAP a continuous structure, or does the operational-period concept still apply?

## References

### Frameworks and Doctrine
- [Incident Command System — Wikipedia](https://en.wikipedia.org/wiki/Incident_Command_System)
- [USDA ICS 200 Lesson 2: ICS Features and Principles](https://www.usda.gov/sites/default/files/documents/ICS200Lesson02.pdf)
- [Splunk — Incident Command Systems: How To Establish an ICS](https://www.splunk.com/en_us/blog/learn/incident-command-system-ics.html)
- [14 Management Characteristics of NIMS — EMSI](https://www.emsics.com/resources/reference-documents/14-management-characteristics-of-nims/)
- [EMSI 14 Principles of NIMS PDF](http://www.emsics.com/wp-content/uploads/2020/06/EMSI-14-Principles-of-NIMS.pdf)
- [National Incident Management System — Wikipedia](https://en.wikipedia.org/wiki/National_Incident_Management_System)
- [FEMA — NIMS Components](https://www.fema.gov/emergency-managers/nims/components)
- [FEMA — NIMS document](https://www.fema.gov/pdf/emergency/nims/NIMS_core.pdf)
- [Tidal Basin — Understanding NIMS](https://www.tidalbasingroup.com/understanding-the-national-incident-management-system-nims/)
- [Common Operational Picture — Wikipedia](https://en.wikipedia.org/wiki/Common_operational_picture)
- [DHS — Common Operating Picture for Emergency Responders](https://www.dhs.gov/publication/common-operating-picture-emergency-responders)

### SRE / IT Service Management
- [Google SRE Book — Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [Google SRE — Incident Management Guide](https://sre.google/resources/practices-and-processes/incident-management-guide/)
- [Google SRE — Incident Management Guide PDF](https://sre.google/static/pdf/IncidentManagementGuide.pdf)
- [Google Cloud Blog — How incident management is done at Google](https://cloud.google.com/blog/products/gcp/incident-management-at-google-adventures-in-sre-land)
- [Rootly — 2025 SRE Incident Management Best Practices Checklist](https://rootly.com/sre/2025-sre-incident-management-best-practices-checklist)
- [ManageEngine — IT Incident Management ITIL Lifecycle](https://www.manageengine.com/products/service-desk/it-incident-management/what-is-it-incident-management.html)
- [Alloy Software — Major Incidents Management in ITIL 4](https://www.alloysoftware.com/blog/major-incident-management-itil-4/)

### Situation Awareness
- [Salmon, Stanton & Jenkins — Distributed Situation Awareness (Routledge)](https://www.routledge.com/Distributed-Situation-Awareness-Theory-Measurement-and-Application-to/Salmon-Stanton-Jenkins/p/book/9781138073852)
- [Stanton et al. — Distributed situation awareness in dynamic systems (Brunel)](https://bura.brunel.ac.uk/bitstream/2438/1419/1/Distributed_situation_awareness_in_dynamic_systems_Stanton_et_al.pdf)
- [ScienceDirect — Situation Awareness in multi-agency emergency response](https://www.sciencedirect.com/science/article/abs/pii/S2212420920300443)
- [ScienceDirect — Protocol for analysing shared situational awareness in cooperative disaster simulations](https://www.sciencedirect.com/science/article/pii/S2212420923000249)
- [ScienceDirect — Developing shared situational awareness for emergency management](https://www.sciencedirect.com/science/article/abs/pii/S0925753513000027)
- [ScienceDirect — Situation awareness for incident response: a case study of management practice](https://www.sciencedirect.com/science/article/abs/pii/S0167404820303953)
- [PMC — Exploring shared identity and interoperability in multi-agency exercises](https://pmc.ncbi.nlm.nih.gov/articles/PMC11649211/)
- [ResearchGate — Shared situational awareness in information security incident management](https://www.researchgate.net/publication/325075058_Shared_situational_awareness_in_information_security_incident_management)
- [arXiv:2508.16669 — Situational Awareness as the Imperative Capability for Disaster Resilience](https://arxiv.org/html/2508.16669v1)

### Hypothesis-Driven Investigation and Triage
- [Graylog — The Importance of Triage in Incident Response](https://graylog.org/post/the-importance-of-triage-in-incident-response/)
- [SecurityScorecard — What Is Triage in Cybersecurity Incident Response](https://securityscorecard.com/blog/what-is-triage-in-cybersecurity-incident-response/)
- [Radiant Security — What is Incident Triage](https://radiantsecurity.ai/learn/incident-triage/)
- [Zscaler — What Is Threat Hunting](https://www.zscaler.com/zpedia/what-is-threat-hunting)

### AI Agents in SOC / Incident Response
- [MDPI — AI-Augmented SOC: A Survey of LLMs and Agents for Security Automation](https://www.mdpi.com/2624-800X/5/4/95)
- [arXiv:2604.20134 — AgentSOC: A Multi-Layer Agentic AI Framework for Security Operations Automation](https://arxiv.org/html/2604.20134)
- [arXiv:2601.05293 — A Survey of Agentic AI and Cybersecurity](https://arxiv.org/html/2601.05293v1)
- [arXiv:2508.18947 — LLMs in the SOC: An Empirical Study of Human-AI Collaboration](https://arxiv.org/html/2508.18947v1)
- [arXiv:2509.10858 — Large Language Models for Security Operations Centers: A Comprehensive Survey](https://arxiv.org/html/2509.10858v1)
- [Microsoft Learn — Triage and investigate incidents with guided responses](https://learn.microsoft.com/en-us/defender-xdr/security-copilot-m365d-guided-response)
- [Microsoft — Security Copilot in Defender, agentic AI](https://techcommunity.microsoft.com/blog/microsoftthreatprotectionblog/security-copilot-in-defender-empowering-the-soc-with-assistive-and-autonomous-ai/4503047)
- [ACM Web Conference 2025 — AI-Driven Guided Response for SOCs with Microsoft Copilot for Security](https://dl.acm.org/doi/10.1145/3701716.3715209)

### Computational Models of ICS / Multi-Agent Simulation
- [Springer — Modelling a chain of command in the ICS using sequential characteristic function games](https://link.springer.com/article/10.1007/s10472-023-09878-7)
- [IEEE — Using model-based simulation for augmenting ICS for disaster response](https://ieeexplore.ieee.org/document/7822336/)
- [ResearchGate — Modelling and simulation of inter- and intra-organisational communication and coordination in emergency response](https://www.researchgate.net/publication/244924837_Modelling_and_simulation_of_inter-_and_intra-organisational_communication_and_coordination_in_emergency_response)
- [GovInfo — Modeling and Simulation of Incident Management for Homeland Security](https://www.govinfo.gov/content/pkg/GOVPUB-C13-4340870bb2b1d1143428e68d56056875/pdf/GOVPUB-C13-4340870bb2b1d1143428e68d56056875.pdf)

### Multi-Agent LLM Coordination (carryover from cycle 0001)
- [arXiv:2507.08616 — AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs](https://arxiv.org/html/2507.08616v1)
- [arXiv:2511.20639 — Latent Collaboration in Multi-Agent Systems](https://arxiv.org/html/2511.20639v1)
- [arXiv:2509.20502 — MARS: toward more efficient multi-agent collaboration for LLM reasoning](https://arxiv.org/abs/2509.20502)

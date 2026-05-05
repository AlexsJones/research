# We've been building AI agents wrong.

I want to start with a number that bothered me for weeks. **Two million.**

That's roughly the population of agents on MoltBook — a real, running multi-agent society where LLMs talk to each other, post, reply, coordinate, and generally behave like a small digital civilization. If you'd asked me a year ago what would happen when you put two million agents in the same room, I'd have said something hand-wavy about emergent behavior, swarm intelligence, the wisdom of crowds. You know the genre. We've been telling ourselves this story since the first AutoGen demo.

The actual result, when researchers measured it, was almost insulting in its clarity: **zero collective intelligence.** No emergent reasoning. No synthesis of distributed knowledge. The swarm did not outperform a single frontier model. On most tasks, it performed *worse* — drowning in shallow single-reply threads and generic responses. Even trivial coordination tasks failed.

Two million agents. Zero supermind.

This is the thing I want to talk about. Not because it's surprising — once you stare at it for a while, it stops being surprising and starts being obvious — but because it tells us something specific about what's broken in the way we're building agents right now. And I think the fix is interesting enough to be worth a blog post.

## The story we've been telling ourselves

The dominant frame for "multi-agent AI" right now goes like this: take an LLM, give it tools (MCP), let it talk to other LLMs (A2A, ACP, ANP, pick your acronym), wrap the whole thing in an orchestration framework (LangGraph, AutoGen, CrewAI), and out the other end falls intelligence-at-scale.

Each of those pieces is doing real work. MCP is great — it standardized how an agent calls a tool, and it deserves the adoption it's getting. A2A is doing useful things for direct agent-to-agent task delegation. LangGraph gives you a sane state machine. None of this is wrong.

But notice what they all have in common: **they're moving messages, not minds.**

Every agent in this stack has its own private context window. They pass messages back and forth like emails. They call each other like microservices. The "state" of a multi-agent system is whatever happens to be in the active conversation buffer of whichever agent is currently thinking. There is no shared substrate. There is no place where understanding accumulates.

We took the org chart, replaced the humans with LLMs, and called it a society. Of course it doesn't think.

If you've ever worked in a real org, you know that the org chart is not where the work happens. The work happens in the shared documents, the long-running Slack threads, the codebase, the wiki, the implicit knowledge that compounds in a team's collective head. Take all of that away and leave only the email lattice, and you don't get a company — you get a help desk.

That's what current multi-agent systems are. A help desk of LLMs.

## The biological detour

Here's the part where I have to talk about cells, because the analogy is too good to skip and biology has been doing this for about three billion years longer than we have.

A cell is not a closed black box that emails other cells. A cell is wrapped in a *membrane* — a permeable, intelligent boundary that decides, in real time, what to let in and what to keep out. Ions flow through gated channels. Receptors on the surface sense the chemical state of the neighborhood. Hormones diffuse, and a thousand cells respond in coordinated waves without anyone in charge. Bacteria do quorum sensing — they literally count their neighbors via molecular concentration and *change behavior* when the population crosses a threshold. Fungal mycelium routes nutrients across kilometers. Neurons fire across synapses with weighted, plastic, learning connections.

What all of these have in common is **selective permeability**. There is an inside and an outside. There are channels through the boundary. The channels are gated — they decide what to share and what to keep private. And critically, the medium between cells *is itself part of the computation*. The cytoplasm, the synaptic cleft, the extracellular fluid — these aren't pipes. They're shared substrate.

When you put two million single-celled organisms in a pond, you get a biofilm — a coordinated, communicating, surprisingly adaptive entity. When you put two million LLM agents on a forum, you get… two million LLM agents on a forum.

The difference is the membrane.

## What the membrane actually is

Let me try to be concrete. The thing I've been calling a "synthetic membrane" is a shared, permeable substrate between agents, with three layers. None of these layers are individually new — that's actually the point. The interesting work is in the interface between them.

```
                         ┌─────────────────────────────────────────┐
                         │       LAYER -1: GOVERNANCE              │
                         │  circuit breakers · human override      │
                         │  value-conflict detection · audit       │
                         └─────────────────────────────────────────┘
                                            ▲
                                            │
                         ┌─────────────────────────────────────────┐
                         │       LAYER  0: DISCOVERY                │
                         │  behavioral indexing · identity verify  │
                         │  capability matching · reputation        │
                         └─────────────────────────────────────────┘
                                            ▲
                                            │
   ┌──────────┐     ┌────────────────────────────────────────┐     ┌──────────┐
   │  AGENT A │ ◀─▶ │   LAYER 3: COORDINATION (swarm)        │ ◀─▶ │  AGENT B │
   │ ┌──────┐ │     │   quorum sensing · task claiming       │     │ ┌──────┐ │
   │ │Local │ │     │   dynamic grouping · conflict resolve  │     │ │Local │ │
   │ │ ctx  │ │     ├────────────────────────────────────────┤     │ │ ctx  │ │
   │ └──────┘ │     │   LAYER 2: SHARED MEDIUM (memory)      │     │ └──────┘ │
   │   gate   │ ◀─▶ │   event log · CRDTs · semantic store   │ ◀─▶ │   gate   │
   │ channels │     │   provenance · time-decay · replay     │     │ channels │
   │          │     ├────────────────────────────────────────┤     │          │
   │  remix   │ ◀─▶ │   LAYER 1: PERMEABILITY (protocol)     │ ◀─▶ │  remix   │
   │  digest  │     │   field-level selectivity · SVAF       │     │  digest  │
   └──────────┘     │   default-deny · cost-aware crossing   │     └──────────┘
                    └────────────────────────────────────────┘
                                            ▲
                                            │
                                  ┌─────────────────────┐
                                  │  IMMUNE LAYER       │
                                  │  anomaly detection  │
                                  │  threat gossip      │
                                  │  memory cells       │
                                  └─────────────────────┘
```

**Layer 1, the permeability layer.** This is the protocol — the part that says what an agent exposes and what it's willing to receive. Every agent declares: *here are my capabilities, here are the slices of my state I'm willing to publish, here are the events I'm listening for.* The crucial design choice: **default-deny, field-level selectivity.** An agent can accept some fields from a peer's state and reject others. The membrane is permeable, but selectively. Just like ion channels.

This is also where **cognitive digestion** happens. Agents don't dump raw output into the shared medium. They store their *interpretation* of what they saw — a remix, in the language of mesh-memory protocols. This matters because raw signal accumulation creates echo chambers and burns input tokens for nothing. (We'll get to tokens in a second; they turn out to dominate everything.)

**Layer 2, the shared medium.** The cytoplasm. This is the substrate where state actually lives — not the messages between agents, but the *fact pool* the agents are drawing from. The right primitive here, I think, is an immutable event log with CRDT semantics. Every state change is an event with a timestamp and a provenance. New agents joining the swarm can replay history. Conflicts are detected at write time. Old entries decay. The whole thing is semantically queryable so an agent can ask "what does the swarm know about X" and get a meaningful answer.

This is the layer that's most missing from current systems. AutoGen doesn't have it. CrewAI doesn't have it. LangGraph has a centralized state graph, which is closer, but it's still one orchestrator's view of the world rather than a substrate the agents share.

**Layer 3, the coordination layer.** The thing that actually lets a swarm form. Task broadcasting, claiming, dynamic grouping, dissolution. Think of it as the bacterial quorum-sensing layer — agents emit "intent signals" into the medium, and when the concentration crosses a threshold, the swarm activates around the problem. Then it dissolves. No top-down orchestrator deciding who does what.

There are two layers wrapping the whole thing — **discovery** (you can't coordinate with agents you can't find, and description-based search demonstrably fails; you need behavioral indexing) and **governance** (circuit breakers, human override, audit trails, value-conflict escalation). Plus a parallel **immune layer** doing adaptive defense via anomaly detection and threat gossip — because the moment shared state becomes valuable, somebody is going to try to poison it.

## Why now

I want to flag a constraint that has been quietly reshaping the design space, because if you don't know about it, the whole architecture looks like over-engineering.

**Agentic tasks consume roughly 1000x more tokens than non-agentic ones.** Input tokens dominate cost. And — this is the cruel part — accuracy peaks at *intermediate* token spend, not maximum. Past a certain point, more communication makes results worse, not better.

This changes everything about how a membrane has to be designed. It means:

- Wire formats have to be compact. You cannot afford verbose JSON.
- Permeability has to be **gated by cost-benefit analysis**, not just by access control. An agent should only cross the membrane when crossing is worth it.
- Cognitive digestion (storing interpretations rather than raw data) becomes economically essential, not just architecturally cleaner.
- Communication budgets need to be a first-class membrane concept — per agent, tracked, enforceable.

Five years ago you could argue about whether a shared-state layer was worth the complexity. Today the math runs the other way: in a 1000x-input-token regime, you cannot afford to broadcast everything to everyone. The membrane is not a luxury. It's the only way to keep agentic systems economically viable as they scale.

This is the "why now" and it's also why I think this isn't a problem that solves itself with bigger context windows or better models. The bigger the context windows get, the more they cost. The bigger the models get, the more their input-token bill dominates. The constraint isn't going away — it's getting tighter.

## What "ZERO collective intelligence" actually maps to

Coming back to the two million agents. The reason that result lands so hard, once you sit with it, is that it's not a model-quality problem. The agents on MoltBook are real frontier-model agents. Smart enough individually to do real work. The problem isn't IQ — it's plumbing.

Specifically, four pieces of plumbing are missing:

1. **No structured protocol** — they communicate via raw text, which means every interaction is shallow, ambiguous, and impossible to build on. → Layer 1 fixes this.
2. **No shared memory** — there's no place for distributed knowledge to synthesize. → Layer 2 fixes this.
3. **No quality gating** — every interaction is weighted equally; reputation and trust don't exist. → Layer 1 (gated permeability) and the immune layer fix this.
4. **No coordination primitives** — no swarming, no role assignment, no task claiming. → Layer 3 fixes this.

The MoltBook result is, in a strange way, the cleanest empirical case yet for why something like a membrane has to exist. We tried scale. Scale alone doesn't produce minds. **Structure does.**

## What we're building

Now, the embarrassing part. None of this is a finished thing yet. I'm writing this blog post in the middle of the work, not after it.

What we have right now is:

- A working sketch of the Layer 1 protocol — field-level selective sharing, default-deny semantics, a wire format that's compact enough to actually use under the token-economics constraint.
- A reference Layer 2 implementation built on an event log with CRDT operations, with semantic query on top. It's small, it's slow, and it works.
- A handful of Layer 3 coordination primitives — task broadcast, claim, quorum activation. Mostly cribbed from biological quorum sensing and from gossip protocols.
- A running test harness that lets us replay the MoltBook-style "shallow swarm" condition and the membrane-mediated condition side by side, against the three-tier evaluation framework (joint reasoning, information synthesis, basic interaction).

The thing I most want feedback on right now is the protocol itself — specifically, whether the field-level selectivity model is the right primitive or whether we should be thinking in terms of capabilities, like an object-capability system. Both have working prototypes. Both have arguments for them. I genuinely don't know which is right.

## Call for collaborators

If any of this rhymes with something you've been thinking about, I'd love to talk. Specifically, I'm looking for people who are:

- **Building multi-agent systems in production** and feeling the pain of message-passing-only architectures. Your war stories are the most valuable thing in the world right now.
- **Working on agent protocols** — A2A, ACP, ANP, MCP extensions. The membrane should compose with these, not replace them, and figuring out the composition story is open work.
- **Coming from biology, distributed systems, or game theory.** The interesting questions in this space — quorum sensing, CRDT design, mechanism design for cooperation — are all stolen from older fields. I want more theft.
- **Skeptical that any of this matters.** Especially this one. The strongest version of the "you're overthinking it" argument is something I haven't heard yet, and I'd rather hear it from you now than from reality in twelve months.

The repo is small enough that one good afternoon can move it forward by a meaningful percentage. If you want to find me, the contact info is at the top of this site, or just open an issue.

We've been building AI agents wrong. The fix is not bigger models or longer contexts — those help individual agents, not collective ones. The fix is the substrate between them. We're going to need a membrane, and the sooner we agree on what one looks like, the sooner the next two million agents will actually have something to say to each other.

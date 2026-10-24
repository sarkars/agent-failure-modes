# Plan: Failure Discovery and Analytics for Chatbots

> **Superseded 2026-10-24 by [gort-plan.md](gort-plan.md), the only product and code plan.** Kept as background: its direction (failure discovery and analytics for chat) is Stage 2 of GORT. Do not plan or build from this page.

> **Status: proposed plan, 2026-10-19.** Direction set by the owner: become the failure-discovery and analytics layer for chat. Developers integrate it into their chatbot and find failure points and drop-offs; we publish studies, some run on simulations we build; and we give a starting set of rules and frameworks to choose from. This is a plan, not a result: nothing here has been built or run, no claim is made that it improves conversion, and every external fact below is from a search summary unless marked opened. It changes an earlier rule: this layer is **code**, not Markdown only. Pattern writing stays paused.

## 1. The one-sentence product
**"Find where your chatbot loses people, and why, in your own conversations, then test fixes before you ship them."**

## 2. What we reuse and what is new
| Already built (in this repo) | Becomes |
|---|---|
| 27 failure patterns, each with a detection idea and a metric | The **failure taxonomy** and the first detectors |
| 27 test files (12 scenarios, rubrics, "Not yet run") | The first **scenario library** for simulation |
| Metrics tables with counter-metrics | The first **analytics definitions** |
| [L0 base spec](l0-base-spec.md) and [L1 base agent design](l1-base-agent-design.md) | The **starter rule packs** and a **reference bot** to test on |
| [Developer search plan](seo/developer-search-plan.md) | The **distribution** plan for studies |

**New, to build:** an event schema and SDK, an analytics engine (funnels and drop-off), failure detectors with measured accuracy, a conversation simulator, a study pipeline, and a rules and frameworks registry.

## 3. Architecture (minimum viable)
1. **Ingest.** Three ways in: a small SDK (Python and TypeScript) that wraps a chat handler; an HTTP endpoint; and import from log files (JSONL). Developers choose.
2. **Event schema (open).** Conversation, turn, message (role, text, timestamps), tool call, handoff, goal and outcome, user feedback, model and prompt version. Redaction and hashing of personal data happen **before** storage.
3. **Analytics engine.**
   - Turn-level **survival curve**: the share of conversations still active at each turn, by entry point, intent, and bot version.
   - **Drop-off hotspots:** the turns, intents, and steps after which people leave, with the preceding bot message shown.
   - **Containment versus confirmed resolution**, time to first useful answer, repeat contact, handoff outcomes.
   - Segment and version comparison, with uncertainty shown.
4. **Failure detectors.** One per taxonomy item (handoff ignored, dead-end reply, correction not applied, buried answer, silent wait, and so on), each a mix of rules and an LLM judge, **each measured against human labels** with precision and recall published. A detector without measured accuracy is labeled "experimental".
5. **Simulator.** Simulated users with a persona, a goal, a patience level, and a language style, run against a bot through an adapter. Scenarios come from the test files. Everything is seeded and versioned (model, prompt, date) so a study can be re-run.
6. **Study pipeline.** A preregistration template (question, hypotheses, scenarios, metrics, analysis), the run, raw transcripts published where privacy allows, and a results page.
7. **Rules and frameworks registry.** Selectable **rule packs** (handoff, fallback, corrections, error messages, refusals, citations, wait states, closers). Each pack = instruction text + a detector + test scenarios + a metric with a counter-metric. Packs combine into **frameworks** (for example "support bot", "lead-capture bot", "voice agent"), and developers pick and edit them.
8. **Output.** First a static report (HTML and Markdown) per bot and per period; a hosted dashboard is a later decision.

## 4. Studies to publish (each preregistered; all start as simulation)
| # | Question | Design | Why it matters |
|---|---|---|---|
| S0 | **Do our detectors agree with people?** | Humans label a sample of transcripts; compare each detector (precision, recall, agreement) | Nothing else is credible without it |
| S1 | How often do chatbots honor "talk to a human" within two turns? | Simulated users run the same scenarios against reference bots built on several models and common system prompts | Handoff is the top real complaint; results are easy to quote |
| S2 | Do corrections stick? | Scenarios with a correction followed by 2 to 5 turns, scored by the end state | Maps to a concrete, checkable failure |
| S3 | Fallback designs compared | Same unrecognized inputs, with a generic reply versus our ladder, measured by simulated abandonment and handoff | Tests our own fix; reported with the simulation caveat |
| S4 | Opening messages and early drop-off | Several openers on a common task; simulated engagement, then a small human panel to check whether the simulation matches | Starts the "boring bot" question with evidence |
| S5 | Containment versus confirmed resolution | Same conversations scored both ways | Shows the gap this metric hides |
| S6 | Simulation validity | Compare simulated-user behavior with a small set of human participants on the same scenarios | Tells readers how far to trust S1 to S5 |

Rules for every study: publish the method, the scenarios, the model versions, the prompts, and the raw outputs; state the limits; never present simulated results as results on real users; do not name or rank third-party commercial products unless the test is reproducible by anyone, permitted by the product's terms, and checked for fairness.

## 5. Phases
| Phase | Goal | Done when |
|---|---|---|
| 0. Foundations | Verify the landscape by opening the tools' docs (Dashbot, Botium, Rasa tests, LLM observability tools, voice-agent testers); choose repo, name, license; fix the event schema | A short landscape page and an approved schema |
| 1. Detect | SDK and log import; the first six detectors; the static report | A bot's logs go in and a failure report comes out |
| 2. Simulate and study | The simulator and reference bots; run S0, S1, S2 | The first study is published with data and method |
| 3. Analytics | Survival curves and drop-off hotspots; containment versus resolution; version comparison | One real or simulated bot shows a ranked list of drop-off causes |
| 4. Rules and frameworks | The registry with selectable packs; "apply pack, rerun tests, compare" | A developer picks a framework and sees the before and after on the same scenarios |
| 5. Conversion layer | Experiments on openers, ask timing, objections, with guardrails against dark patterns and rules on disclosure | Only after S0 shows the detectors are trustworthy |

## 6. What each phase needs from you
- **A separate code repository.** The current repo is a content repo; this layer needs its own code, tests, and releases. I would create it only with your approval, under your account.
- **Model API access** as environment variables (never pasted in chat) for the simulator and the judges.
- **Human labeling capacity** for S0 and S6: someone to label a few hundred transcripts, or a budget for a small panel.
- **At least one design partner** with real conversations for Phase 3, otherwise analytics is shown on simulated data only.
- **A license and a name.**

## 7. Risks and how the plan handles them
| Risk | Handling |
|---|---|
| Simulated users do not behave like people | S6 measures it; every simulated result carries a validity note; no lift claims without human data |
| LLM judges are unreliable | S0 measures them; show confidence intervals; keep a human-label set to re-check |
| Crowded market (conversation analytics, LLM observability, voice testing) | Phase 0 landscape review; differentiate on failure taxonomy, tested rule packs, and open studies, not on dashboards |
| Privacy of logs | Redact before storage, store hashes, document retention; no personal data in published data |
| Naming products that fail | Reproducible, permitted, fair tests only; otherwise anonymize |
| Persuasion becomes manipulation | Phase 5 gated; guardrails from the existing patterns on dark patterns; disclosure treated as a constraint, not an obstacle |
| Scope | Build in phases; stop at the end of any phase that does not show value |

## 8. How we would know it is working
- Detector precision and recall against human labels (S0), with the numbers published.
- Studies published with reproducible data.
- Developers who integrate and use the report (count real integrations, not stars).
- A drop-off cause found in a real or simulated bot, fixed by a chosen rule pack, and verified on the same scenarios.
- Search impressions and clicks on the study pages, from the [developer search plan](seo/developer-search-plan.md).

## 9. Decisions needed now
1. **Create a new code repository?** Name, license, and whether it is public from day one.
2. **Model API access** in the environment, and a spending limit.
3. **Human labeling:** who labels, and how many transcripts.
4. **Whether to test named commercial bots** at all, or only our own reference bots.
5. **First design partner**, if any.

## Related
- [Developer search plan](seo/developer-search-plan.md) · [L0 base spec](l0-base-spec.md) · [L1 base agent design](l1-base-agent-design.md) · [L1 harness decision](l1-harness-decision.md) · [Gap analysis](gap-analysis.md) · [Content program](content-program.md)

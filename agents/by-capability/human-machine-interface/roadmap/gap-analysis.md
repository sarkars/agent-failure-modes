# Gap Analysis: What Already Exists, Per Agent Type, and Whether This Library Stands Out

> **Status: first pass, 2026-10-15.** Everything below comes from one round of web searches, read through search summaries. I did **not** open the primary documents. "Nothing found" means one search found nothing, not that nothing exists. A scheduled task (see the [content program](content-program.md), task 13) redoes this properly by opening each source.

## 1. What already exists
| Area | What I found | Type | What it means for us |
|---|---|---|---|
| Failure taxonomies | [MAST](https://arxiv.org/html/2503.13657v2) (Berkeley): 14 failure modes in 3 groups from 7 multi-agent frameworks and 200+ tasks, with a 1,642-trace annotated dataset | Peer-reviewed research | A real, annotated trace dataset is something we lack. Its authors say failures come mostly from system design and inter-agent misalignment, not only model limits |
| Failure taxonomies | [TRAIL](https://www.patronus.ai/blog/introducing-trail-a-benchmark-for-agentic-evaluation) (Patronus AI): a benchmark with a failure taxonomy (the vendor says 20+ modes) | Vendor | Taxonomy not seen; count is the vendor's claim |
| Failure taxonomies | [A 2026 preprint](https://arxiv.org/pdf/2607.16387) argues fixed catalogs like MAST are limited and that failure vocabulary should be built from a system's own traces | Preprint, not peer-reviewed | A fixed catalog alone is a weak position; trace-derived tagging is the argued direction |
| Failure lists | [vectara/awesome-agent-failures](https://github.com/vectara/awesome-agent-failures): community list of failure modes, case studies, mitigations (about 157 stars on a third-party tracker) | Community | Closest in spirit to this library |
| Incident catalogs | [AI Incident Database](https://arxiv.org/pdf/2011.08512); a [32-case agent failure catalog](https://dev.to/vdalal/i-catalogued-32-real-ai-agent-failures-then-marked-the-ones-we-cannot-stop-40k8) from one author | Research; single-author blog | Incident pages are not new. Sourced, pattern-linked ones still are rare |
| Build guides | [Anthropic's "Building effective agents"](https://www.anthropic.com/engineering/building-effective-agents), [OpenAI's practical guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), and Google's Agents Companion (described as covering evaluation and operations) | Vendors | Generic "how to build" is covered by the biggest names |
| Customer-service benchmarks | [τ-bench](https://arxiv.org/pdf/2406.12045) (airline and retail, `pass^k` for consistency), its successor tau2-bench (adds telecom, banking, voice), and Hyper-τ-bench (coding agents building a customer-service agent; one report gave the best automated configuration 23.9% vs. 82.2% for an engineer plus a frontier model) | Vendor-run benchmarks, secondary summaries | They measure task success and policy adherence. I found nothing on tone, handoff, or refusal behavior |
| Self-improvement research | [A 2025 survey of self-evolving agents](https://arxiv.org/pdf/2507.21046), plus Reflexion, Self-Refine, Agent Workflow Memory; one survey says much work mixes in-task retry with persistent self-evolution | Research | Heavily covered in research. Production deployment patterns were thin in my search |
| Self-improvement in practice | [OpenAI's self-evolving agents cookbook](https://cookbook.openai.com/examples/partners/self_evolving_agents/autonomous_agent_retraining) (a retraining loop with graders, built on a healthcare-documentation task, using GEPA for prompt evolution) and vendor posts on turning production traces into eval cases (Braintrust, Arize, Latitude) | Vendor | The basic loop is documented. Differentiation must come from elsewhere |
| Self-improvement safety | [Darwin Gödel Machine](https://arxiv.org/pdf/2505.22954): the authors warn that benchmark-optimized self-modification could introduce misalignment and uninterpretable logic, and run in sandboxes with traceable lineage. A [runtime-governance paper](https://arxiv.org/pdf/2603.16586) argues guardrails inside the agent can't be audited independently and that an agent that writes code can bypass them | Research | Supports keeping guardrails and permissions out of the agent's reach |
| Self-improvement governance | [An enterprise playbook](https://www.truefoundry.com/blog/self-evolving-agents-enterprise-governance-playbook) (versioned candidates, evaluation gates, rollback, human approval for permission or production changes) | Vendor | The "propose, evaluate, gate" design is already published. Detail for customer-facing conversation behavior is not |

## 2. This library's coverage by agent type
Counts are catalog rows (written plus candidate), not verified patterns, and none of the types has more than a few written. The adoption ranking behind the agent-type list is weak: my search found no survey breaking adoption down by type, only forecasts and overall rates.

| Agent type | Catalog rows | External coverage found in this pass | Gap suggested |
|---|---|---|---|
| Customer service and support | Many, spread across several files (not counted) | τ-bench family for task success; vendor playbooks | Human-side behavior (handoff, tone, refusals, accessibility): nothing found |
| Embedded copilots | 23 | Not searched | Unknown |
| Coding agents | 6 | Two academic studies of failures in agent-written code changes | Library has few rows; broad external work exists |
| Research and data agents | 5 | Not searched | Unknown |
| Workflow, IT, finance, healthcare, sales, voice, browser, shopping, education, assistant, HR, legal | 2 to 5 each | Not searched in this pass | Unknown; the scheduled gap analysis covers them |
| Multi-agent platforms | 2 | MAST covers this deeply | Do not compete; link to MAST |

## 3. Will this content stand out? A first verdict
| Content | Verdict | Why |
|---|---|---|
| A large failure catalog | **Will not stand out on its own** | MAST, TRAIL, the Vectara list, and incident databases exist. Size isn't a differentiator, and MAST has annotated real traces we lack |
| A generic "how to build an agent" guide | **Will not stand out** | Anthropic, OpenAI, and Google have published guides |
| A generic self-improving-agent write-up | **Will not stand out** | Surveys, an OpenAI cookbook, and vendor playbooks exist |
| Failure-first human-side coverage: handoff, refusals, tone, accessibility, wrong channel, with tests | **Plausible gap** | My searches found benchmarks for task success but none for handoff or tone. Unverified beyond one pass |
| A self-correcting customer-facing agent whose learning signal is a failure library, with a stated policy on what it may change itself, with measured results | **Plausible gap, high effort** | The loop, the safety warnings, and the governance advice each exist separately. I found no reference implementation that ties them to a named failure library. Needs a real build and real results to count |
| Real traces and anonymized transcripts | **Strongest differentiator, not yet available** | It is what MAST's value rests on |

## 4. What this does not establish
- One search per topic. The gaps could close with a second search.
- No primary documents opened. Several figures (Hyper-τ-bench results, star counts) come from secondary pages.
- No traffic data for any competitor, so "stands out" here means "differs in content", not "will rank".

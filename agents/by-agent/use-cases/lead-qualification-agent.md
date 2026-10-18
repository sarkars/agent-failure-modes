# Lead Qualification (SDR) Agent: Business Goals, Failure Definitions, and Test List

An agent that talks to inbound or outbound leads, finds out whether there is a fit, and hands qualified leads to a salesperson with the facts.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline. Parts of this agent touch law or regulated practice (flags: L); get legal or expert review before use.

## Scope (a starting point)

**The agent does:**
- Ask discovery questions and record the answers
- Score or tag the lead from what the lead actually said
- Book a meeting or hand off with a summary

**The agent does not:**
- Negotiate price or make commitments
- Contact people who have not agreed to be contacted or who opted out
- Invent what the lead said

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Qualify accurately from what the lead actually said | Scores and tags reflect the lead's real needs, budget, and timing, and match the company's current scoring rules. | Head of sales development |
| G2 | Hand off with the facts a salesperson needs | The salesperson starts with the lead's budget, timing, and objections already known. | Head of sales development and sales operations |
| G3 | Respect consent, opt-outs, and outreach rules | Only people who may be contacted are contacted, at allowed times, and opt-outs are honored. | Compliance with sales operations |
| G4 | Make no promises the company has not approved | The agent does not commit to prices, discounts, or terms. | Head of sales and legal |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Qualify accurately from what the lead actually said

| Field | Definition |
|---|---|
| How to measure | Agreement between the agent's qualification and a salesperson's review on a sample; conversion of agent-qualified leads vs. others. |
| A failure is | The agent applies an old scoring rule from memory, scores from a look-alike deal, or records an objection the lead did not state. |
| Severity | High: a fabricated statement in the record. Medium: a wrong score from a stale rule. |
| Hand over to a person when | The lead asks something the agent cannot answer, or states a constraint the agent cannot place. |

**Failures to test for this goal (from the library):**
- [Agent Applies Remembered Scoring Heuristic Instead of Querying Live Scoring-Rules Tool](../../by-use-case/sales-crm/goals/lead-scoring/failures/agent-applies-remembered-scoring-heuristic-instead-of-querying-live-scoring-rules-tool.md): A Lead-Scoring Agent, When Asked to Explain or Compute a Lead's Score, Falls Back on a Generic Firmographic-Weighting Heuristic Resembling…
- [Embedding-Similarity Retrieves Superficially Similar Deal as Precedent](../../by-use-case/sales-crm/goals/lead-scoring/failures/embedding-similarity-retrieves-superficially-similar-deal-as-precedent.md): A Lead-Scoring Agent That Justifies Its Score by Retrieving "Similar Past Deals" via Embedding Search over the Closed-Deal History Pulls a…
- [Agent Fabricates a Stated Objection When the Call-Transcript Tool Returns Empty](../../by-use-case/sales-crm/goals/lead-scoring/failures/agent-fabricates-stated-objection-when-call-transcript-tool-returns-empty.md): A Lead-Scoring Agent Asked to Factor In a Prospect's Most Recent Discovery-Call Sentiment Calls the Call-Transcript Retrieval Tool,…

### G2. Hand off with the facts a salesperson needs

| Field | Definition |
|---|---|
| How to measure | Share of handoffs where the salesperson re-asked something the lead had already told the agent. |
| A failure is | A disclosed budget ceiling or disqualifier is dropped between qualification and the next step. |
| Severity | High: a disqualifying fact lost. Medium: a missing detail. |
| Hand over to a person when | The lead asks for a person, or a disqualifier appears. |

**Failures to test for this goal (from the library):**
- [SDR-Qualification Handoff Drops a Disclosed Budget Ceiling Before Lead Scoring](../../by-use-case/sales-crm/goals/lead-scoring/failures/sdr-qualification-handoff-drops-disclosed-budget-ceiling-before-scoring.md): An SDR-Qualification Agent That Talks to a Prospect and Learns an Explicit, Hard Budget Ceiling Hands the Qualified Lead Off to a…

### G3. Respect consent, opt-outs, and outreach rules

| Field | Definition |
|---|---|
| How to measure | Contacts without recorded consent, outside permitted hours, or to suppressed numbers. Target: zero. |
| A failure is | Messages sent without consent, STOP requests ignored, or quiet hours violated. |
| Severity | Critical: contact after an opt-out or without consent where required. High: outside permitted hours. |
| Hand over to a person when | Any opt-out or complaint. |

**Failures to test:** none documented in the library yet for this goal; this is a gap to fill.

### G4. Make no promises the company has not approved

| Field | Definition |
|---|---|
| How to measure | Sampled review for commitments or discounts offered. Target: zero. |
| A failure is | The agent gives away a discount or states terms it cannot grant. |
| Severity | High: a price or term promised. Medium: an overstated product claim. |
| Hand over to a person when | Any request about price, contract terms, or discounts. |

**Failures to test:** none documented in the library yet for this goal; this is a gap to fill.

## Conversation-level failures to check

This agent talks to people. Also test these:
- [negotiation capitulation](../../by-capability/human-machine-interface/goals/relational-and-boundaries/failures/negotiation-capitulation.md)
- [undisclosed bot identity](../../by-capability/human-machine-interface/goals/trust-and-rapport/failures/undisclosed-bot-identity.md)

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | CRM reads and writes must be real, not assumed | 19 |
| [Memory Management](../../cross-cutting/operations/goals/memory-management/) | Lead facts must persist across sessions without leaking | 22 |
| [State Tracking](../../cross-cutting/operations/goals/state-tracking/) | What the lead said versus what the agent inferred | 9 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | The handoff to a salesperson is the product | 10 |
| [Tool Rate Quota Limits](../../cross-cutting/operations/goals/tool-rate-quota-limits/) | Outreach and CRM APIs have limits | 16 |

## Security and governance to check

- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Governance](../../cross-cutting/governance/goals/governance/) (governance)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- What counts as qualified, and who owns the definition
- The consent rules for each channel and region
- What the agent may say about price
- Whether the agent must tell leads it is an AI

## Related

- [All agents by business goal](../)

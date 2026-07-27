# What Are the Most Common Offer Generation Failures in AI Agents?

**Offer-generation agents produce compensation figures from stale training-data benchmarks instead of querying live market data, anchor offers to mismatched leveling precedents selected via embedding similarity, and commit to negotiated terms in offer letters without verifying those terms were actually captured in the structured handoff from the recruiting coordinator.** These failures cluster around two categories: stale knowledge overriding live tools (compensation data, leveling precedents), and multi-agent handoff loss (negotiated exceptions, visa-contingent arrangements). Offer generation errors are silent — the output looks like a plausible offer letter — and materially affect allocational fairness (disparate offer bands by inadvertently using wrong precedents) and employer compliance (offers that contradict what the candidate was verbally promised).

## Key Takeaways

- 4 distinct failure patterns affect offer generation, grouped into two mechanisms: knowledge staleness (training-corpus market data and leveling precedents override live tools), and handoff information loss (negotiated exceptions and contingencies).
- Stale training-corpus compensation data affects offers in fast-moving roles (AI/ML engineering, specialized skills) by 5-50%, with candidates declining or countering at higher rates than offers grounded in live benchmarking data.
- Multi-agent handoff drops negotiated visa-contingent remote-work exceptions or other non-standard offer terms at "occasional" frequency, with discrepancies discovered only when candidates compare offer letters against their negotiation conversation.
- Embedding-retrieval leveling mismatches affect 10-15% of offers when precedent selection is done by description-text similarity rather than structured leveling-framework metadata, producing band distributions inconsistent with framework intent.

## Scope

- **Knowledge Staleness & Tool Avoidance** — [stale-training-corpus-comp-benchmarks-override-live-market-data](failures/stale-training-corpus-comp-benchmarks-override-live-market-data.md), [embedding-retrieval-pulls-mismatched-job-family-leveling-precedent-for-offer-band](failures/embedding-retrieval-pulls-mismatched-job-family-leveling-precedent-for-offer-band.md). Agents substitute parametric knowledge absorbed during pretraining (compensation figures, leveling precedents) for live tool results, even when the live tools are available and callable.
- **Handoff Schema Brittleness** — [multi-agent-handoff-drops-negotiated-visa-tied-remote-exception-before-offer-letter-generation](failures/multi-agent-handoff-drops-negotiated-visa-tied-remote-exception-before-offer-letter-generation.md), [offer-letter-auto-sent-without-rechecking-live-background-check-gate-status](failures/offer-letter-auto-sent-without-rechecking-live-background-check-gate-status.md). Negotiated terms and compliance gates are established in one agent's conversational context but not carried into the structured fields the downstream offer-letter agent reads, and compliance gates are checked against cached state rather than live status.

## When Offer Generation Matters

- Offer generation is the economic commitment stage: an offer letter with terms and compensation binds both parties and becomes the reference point for onboarding, compensation reviews, and legal disputes over work arrangements.
- Market misalignment in offers (above or below current market rate) directly affects candidate quality (candidates decline or negotiate) and pay-equity exposure (offers systematically under-market for certain demographic groups or career backgrounds).
- Visa-contingent and remote-work exceptions are especially likely to fall outside standard offer schemas and to be lost in handoffs; these exceptions are often compliance-critical for international hires and affect start date feasibility.

## Cross-Pattern Insight

All four offer-generation patterns root in the same architectural choice: treating agent-generated answers and retrieved live data as having equivalent reliability. When an agent has immediate access to a live compensation-benchmarking tool or a leveling-framework rubric, but the underlying model also carries parametric knowledge of typical figures or precedents, both produce plausible answers with identical fluency. Without an enforced requirement that certain decision-relevant data (market rates, live leveling rubrics, compliance-gate status) must be sourced from live tools rather than parametric knowledge, the agent defaults to whichever path is easier or most generative — and the stale path is often more fluent because it reflects high-frequency pretraining patterns. Mitigation is structural: mandatory tool-call requirements for decision-critical data, live status re-checks immediately before consequential actions (offer sending, background-check gates), and structured handoff fields that force explicit representation of every negotiated term and compliance gate.

## Frequently Asked Questions

### How do you know if an offer's market-rate figure came from live data or training knowledge?

Require the offer-generation agent to log a tool-call entry for every market-rate figure cited in the offer rationale. If a market-rate claim has no corresponding live-tool call in the trace, treat the offer as unverified and regenerate it with the live tool enforced. Independently query the live benchmarking tool for the same role/level/location and compare; a material mismatch indicates the offer was anchored to stale data.

### What causes leveling mismatches when an agent retrieves past precedents?

Embedding-similarity retrieval over role descriptions ranks candidates by textual overlap (title vocabulary, industry keywords), not by the structured criteria (career track, leveling framework, scope of role) that actually determine comparable compensation. A "Senior Engineer" from one framework can share near-identical description text with a "Senior Engineer" from a different framework while having entirely different banding criteria. Pre-filter retrieved precedents by leveling-framework and career-track identity before applying text similarity.

### Can a recruiter recover if an offer letter goes out with a missing visa-contingency or exception?

Only by reaching out proactively — the candidate will see the discrepancy and may use it as leverage or lose trust in the hiring team. Mitigation requires reconciliation before the letter is sent: scan the recruiting coordinator's negotiation transcript for any term not represented in the structured offer parameters, flag mismatches as mandatory holds, and require human review before the letter is finalized.

### How do you prevent an offer letter from being sent based on stale background-check status?

Require a fresh, synchronous call to the background-check vendor's status API immediately before any offer letter is marked for sending, not a cached or task-list-derived state. Treat the absence of a check item from the agent's internal task list as not equivalent to "cleared" — a cleared status must come from the vendor's own status field explicitly equaling the defined "clear" value.

### What's the difference between a leveling-framework error and a negotiation-handoff error in offer generation?

Leveling-framework errors affect the computed band (wrong precedent selection, wrong framework applied). Negotiation-handoff errors affect offer terms (visa contingency, relocation timing) — the compensation may be correct, but the conditional terms are wrong or missing. Both are silent failures: the offer looks complete, but critical context is missing.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Stale Training-Corpus Comp Benchmarks Override Live Market Data](failures/stale-training-corpus-comp-benchmarks-override-live-market-data.md) | Agent answers market-rate questions from pretraining knowledge instead of calling live benchmarking tool, producing offers anchored to outdated figures |
| [Embedding Retrieval Pulls Mismatched Job-Family Leveling Precedent for Offer Band](failures/embedding-retrieval-pulls-mismatched-job-family-leveling-precedent-for-offer-band.md) | Precedent retrieval by text similarity surfaces a role from a different leveling framework, misaligning the computed offer band |
| [Multi-Agent Handoff Drops Negotiated Visa-Tied Remote Exception Before Offer-Letter Generation](failures/multi-agent-handoff-drops-negotiated-visa-tied-remote-exception-before-offer-letter-generation.md) | Recruiting coordinator negotiates a visa-contingent remote-work exception that exists only in free-text notes, not in structured offer parameters; offer letter omits it |
| [Offer Letter Auto-Sent Without Rechecking Live Background-Check Gate Status](failures/offer-letter-auto-sent-without-rechecking-live-background-check-gate-status.md) | Offer sent based on background-check item disappearing from agent's task list (not re-queried) rather than confirming actual "clear" status from vendor's live API |

**Total: 4 patterns**

## Related Goals

- [Candidate Screening](../candidate-screening/) — upstream from offer generation; screening errors (bias, skill misassessment) affect the candidate pool an offer agent works with.
- [Onboarding](../onboarding/) — downstream from offer generation; visa-sponsorship terms and work-location exceptions negotiated at offer stage need to be reflected in onboarding tasks.

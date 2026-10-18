# Sales and CRM Agents: Business Goals, Failure Patterns, and Fixes

**Sales and CRM Agents fail along 4 goals: Quota Achievement, Lead Scoring, Pipeline Forecasting carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 16 documented failure patterns across 4 goals. What it does: score leads, manage deals, and forecast pipeline.
- The most documented goal is [Quota Achievement](../by-use-case/sales-crm/goals/quota-achievement/) with 5 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Quota Achievement](../by-use-case/sales-crm/goals/quota-achievement/) | When agents calculate rep quota attainment using stale discount policies | 5 |
| [Lead Scoring](../by-use-case/sales-crm/goals/lead-scoring/) | When agents compute a lead's likelihood-to-close using stale scoring rules | 4 |
| [Pipeline Forecasting](../by-use-case/sales-crm/goals/pipeline-forecasting/) | Pipeline-forecasting failures occur across multiple independent dimensions | 4 |
| [Deal Management](../by-use-case/sales-crm/goals/deal-management/) | When agents assemble contract clauses, track negotiated terms | 3 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Best-Case Projection Bias](../by-use-case/sales-crm/goals/pipeline-forecasting/failures/best-case-projection-bias.md) | Sales forecasting model uses deal probability from salesperson input, which is inherently optimistic; projects deals that salesperson hopes will… | Common |
| [Embedding-Similarity Retrieves Superficially Similar Deal as Precedent](../by-use-case/sales-crm/goals/lead-scoring/failures/embedding-similarity-retrieves-superficially-similar-deal-as-precedent.md) | A Lead-Scoring Agent That Justifies Its Score by Retrieving "Similar Past Deals" via Embedding Search over the Closed-Deal History Pulls a Lexically… | Common |
| [Multi-Agent Handoff Drops Negotiated Payment-Terms Exception Before Deal-Desk Approval](../by-use-case/sales-crm/goals/deal-management/failures/multi-agent-handoff-drops-negotiated-payment-terms-exception-before-deal-desk-approval.md) | An Account Executive's Free-Text Email Negotiation Establishing Extended Payment Terms for an Enterprise Deal Is Not Captured in the Structured… | Common |
| [SDR-to-AE Handoff Drops Unstructured Disqualifying Signal](../by-use-case/sales-crm/goals/pipeline-forecasting/failures/sdr-to-ae-handoff-drops-unstructured-disqualifying-signal.md) | An SDR-Qualification Agent's Chat Transcript with a Prospect Contains a Disqualifying Signal (No Budget This Fiscal Year, Competitor Already… | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Human-side failures

Because this agent talks to customers or patients, also check conversation-level failures: tone, handoff to a person, refusals, and choosing the wrong channel. See the [human-machine interface section](../by-capability/human-machine-interface/).

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in sales and crm agents?

The most documented goal is Quota Achievement (5 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building sales and crm agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)

# Accounts-Payable Invoice Processing Agent: Business Goals, Failure Definitions, and Test List

An agent that reads vendor invoices, matches them to orders and receipts, and prepares or releases payments within set limits.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline. Parts of this agent touch law or regulated practice (flags: E); get legal or expert review before use.

## Scope (a starting point)

**The agent does:**
- Extract vendor, amount, currency, and line items from invoices
- Match them to purchase orders and receipts
- Prepare payments, and release small ones within its authority

**The agent does not:**
- Release payments above its limit or to new vendors without approval
- Change vendor bank details on an email request
- Approve its own exceptions

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Pay the right amount to the right vendor | Every payment matches an approved order, the vendor of record, and the invoice amount in the right currency. | Controller and accounts-payable lead |
| G2 | Never pay twice or outside authority | Each invoice is paid at most once, within the agent's limit and with the approvals required. | Controller with internal audit |
| G3 | Finish the batch, or say exactly what did not finish | Every invoice in a batch ends in a known state: paid, held for a stated reason, or failed with a stated reason. | Accounts-payable lead and platform owner |
| G4 | Keep a complete audit trail and run within budget | Every action has a record of what was read, decided, and done, and spend stays within its budget. | Internal audit and finance operations |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Pay the right amount to the right vendor

| Field | Definition |
|---|---|
| How to measure | Payment accuracy on a sampled review: wrong amount, wrong vendor, wrong currency or unit. Count each separately. |
| A failure is | Characters or decimals misread, the wrong ID or currency used, or a payment prepared for a look-alike vendor. |
| Severity | Critical: a payment to the wrong party or a materially wrong amount. High: a wrong currency or unit caught late. Medium: a formatting error. |
| Hand over to a person when | Low extraction confidence, an amount outside the order, or a new or changed vendor. |

**Failures to test for this goal (from the library):**
- [OCR Confuses Similar-Looking Characters (0/O, 1/l/I, 5/S)](../../by-capability/document-processing/goals/accurate-text-extraction/failures/character-confusion.md): OCR swaps visually similar characters (0/O, 1/l/I, 5/S, 8/B), so extracted IDs and codes look right but are wrong
- [OCR Swaps Decimal Points and Commas in Invoice Amounts](../../by-capability/document-processing/goals/accurate-text-extraction/failures/punctuation-errors.md): OCR misreads punctuation — decimals become commas, currency symbols drop, dashes get interchanged — silently corrupting parsed amounts
- [Wrong Units/Currency](../../cross-cutting/operations/goals/tool-invocation/failures/wrong-unitscurrency.md): Agent sends cents vs dollars, UTC vs local, kg vs grams
- [Wrong Id/Key Usage](../../cross-cutting/operations/goals/tool-invocation/failures/wrong-idkey-usage.md): Agent uses customer ID as account ID, message ID as thread ID, etc

### G2. Never pay twice or outside authority

| Field | Definition |
|---|---|
| How to measure | Duplicate payments and payments above the limit or without a required approval. Target: zero for both. |
| A failure is | A retry repeats a payment, concurrent runs collide, or an approval step is skipped in a handoff. |
| Severity | Critical: a duplicate or unapproved payment. High: a near miss caught by a downstream control. |
| Hand over to a person when | Any amount above the limit; any retry of a payment action. |

**Failures to test for this goal (from the library):**
- [Idempotency Failure](../../cross-cutting/operations/goals/tool-invocation/failures/idempotency-failure.md): Agent repeats a write action and creates duplicates
- [Tool Idempotency Assumption Failure](../../cross-cutting/operations/goals/tool-selection-sequencing/failures/tool-idempotency-assumption-failure.md): An agent retries a tool call after a timeout, an ambiguous error, or a crash-and-resume, assuming that calling it again is safe because…
- [Concurrent State Modification](../../cross-cutting/operations/goals/state-consistency/failures/concurrent-state-modification.md): Two or more agent instances (or an agent and a background job) read the same piece of shared state — a task queue entry, a customer record,…
- [Handoff Approval Skipped](../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-approval-skipped.md): A workflow is designed so that one agent must obtain sign-off from a human or a designated approval agent before handing a task to the next…
- [Handoff Idempotency Violation](../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-idempotency-violation.md): A handed-off task gets executed more than once because the handoff mechanism retries on a suspected failure (timeout, dropped…

### G3. Finish the batch, or say exactly what did not finish

| Field | Definition |
|---|---|
| How to measure | Batches with invoices in an unknown state. Target: zero. Cases where the agent reported success on a failed step. |
| A failure is | A partial batch is reported as complete, a silent tool failure goes unnoticed, or results past the first page are missed. |
| Severity | Critical: an unpaid or failed payment reported as paid. High: invoices lost in a partial run. Medium: slow recovery. |
| Hand over to a person when | Any invoice in an unknown or failed state. |

**Failures to test for this goal (from the library):**
- [Recovery Partial Failure](../../cross-cutting/operations/goals/fault-tolerance/failures/recovery-partial-failure.md): A recovery operation spanning multiple components or subsystems completes successfully for some of them but not others, leaving the overall…
- [Action-Completion Claimed Without Reading the Tool's Status Field](../../cross-cutting/operations/goals/tool-reliability/failures/action-completion-claimed-without-status-check.md): Agent Narrates a Tool-Initiated Action as Complete Based on Having Issued the Call, Not on the Call's Actual Returned Status
- [Silent Failures in Multi-Stage Pipelines](../../cross-cutting/operations/goals/observability-monitoring/failures/silent-failures-in-multi-stage-pipelines.md): Agent Completes Despite Failures in Intermediate Stages, Outputting Incorrect Results
- [Partial Result Misuse](../../cross-cutting/operations/goals/tool-invocation/failures/partial-result-misuse.md): Agent treats partial/incomplete output as complete
- [Pagination Failure](../../cross-cutting/operations/goals/tool-invocation/failures/pagination-failure.md): Agent Reads Only the First Page of a Paginated or Length-Capped Tool Response and Proceeds as if That Page Were the Complete Result Set

### G4. Keep a complete audit trail and run within budget

| Field | Definition |
|---|---|
| How to measure | Actions with no log entry. Target: zero. Spend against budget, and alerts on unusual cost. |
| A failure is | Missing or incomplete logs, no audit trail, budgets alerted on but not enforced, or cost anomalies unnoticed. |
| Severity | High: a payment with no audit trail. Medium: an unexplained cost spike. |
| Hand over to a person when | Any gap in the audit trail; any budget breach. |

**Failures to test for this goal (from the library):**
- [Missing Audit Trail](../../cross-cutting/operations/goals/traceability/failures/missing-audit-trail.md): Agent Actions Not Recorded for Later Review or Compliance
- [Incomplete Action Logging](../../cross-cutting/operations/goals/traceability/failures/incomplete-action-logging.md): Only Some Agent Actions Are Logged, Creating Blind Spots
- [Budget Enforcement Bypass](../../cross-cutting/operations/goals/cost-tracking/failures/budget-enforcement-bypass.md): Agent Exceeds Budget Limits Without Being Stopped
- [Cost Anomaly Blindness](../../cross-cutting/operations/goals/cost-tracking/failures/cost-anomaly-blindness.md): Unusual Cost Patterns Go Undetected

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Invocation](../../cross-cutting/operations/goals/tool-invocation/) | Wrong units, IDs, or retries become wrong or duplicate payments | 12 |
| [Tool Selection Sequencing](../../cross-cutting/operations/goals/tool-selection-sequencing/) | Order and idempotency of calls matter for payments | 8 |
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | A failed payment call must be seen as failed | 19 |
| [Tool Error Handling](../../cross-cutting/operations/goals/tool-error-handling/) | Errors must route to a person, not be swallowed | 2 |
| [Fault Tolerance](../../cross-cutting/operations/goals/fault-tolerance/) | Batches fail partway and must recover cleanly | 20 |
| [Reliability and Resilience](../../cross-cutting/operations/goals/reliability-and-resilience/) | Month-end load and outages | 2 |
| [State Consistency](../../cross-cutting/operations/goals/state-consistency/) | Concurrent runs and replays must not corrupt state | 8 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | Approvals above the limit | 8 |
| [Input Output Handling](../../cross-cutting/operations/goals/input-output-handling/) | Invoices arrive as scans, PDFs, and emails | 22 |
| [Cost Tracking](../../cross-cutting/operations/goals/cost-tracking/) | Spend and model cost need budgets | 6 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Auditors need the full trail | 8 |
| [Version Management](../../cross-cutting/operations/goals/version-management/) | Templates and tool versions change | 22 |
| [Dependency Management](../../cross-cutting/operations/goals/dependency-management/) | ERP and bank APIs change | 23 |
| [Tool Operational Limits](../../cross-cutting/operations/goals/tool-operational-limits/) | Bank and ERP calls have operating limits | 14 |

## Security and governance to check

- [Tool Authorization Limits](../../cross-cutting/security/goals/tool-authorization-limits/) (security)
- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Approval Workflows](../../cross-cutting/governance/goals/approval-workflows/) (governance)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- Payment limits per agent and who approves above them
- Which vendors are pre-approved and how new ones are added
- How changes to vendor bank details are verified out of band
- Retention of invoices and logs

## Related

- [All agents by business goal](../)

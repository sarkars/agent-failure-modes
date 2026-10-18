# Refunds and Billing-Disputes Agent: Business Goals, Failure Definitions, and Test List

An agent that handles refund requests and billing disputes: checks the customer's plan and records, applies policy, and issues or recommends credits within set limits.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline. Parts of this agent touch law or regulated practice (flags: L); get legal or expert review before use.

## Scope (a starting point)

**The agent does:**
- Check the customer's invoices, plan, and prior credits
- Apply the refund or dispute policy for the customer's plan and jurisdiction
- Issue small credits within its limit, and prepare larger ones for approval

**The agent does not:**
- Issue refunds above its limit without approval
- Decide chargebacks or legal disputes
- Waive policy because a customer insists

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Reach the correct outcome under policy | The decision matches the policy that applies to this customer's plan, region, and situation. | Billing operations lead with finance |
| G2 | Stay within monetary authority | No refund or credit is issued above the agent's limit, or for an unverified claim. | Finance controller and billing operations |
| G3 | Explain every decision and keep a record | The customer gets a clear reason, and a reviewer can see what the agent used to decide. | Compliance and billing operations |
| G4 | Treat hardship and vulnerable customers with care | Customers in hardship or distress are recognized and routed to a person trained for it, not handled as a policy lookup. | Head of customer care and compliance |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Reach the correct outcome under policy

| Field | Definition |
|---|---|
| How to measure | Sampled review against a reviewer's decision: agreement rate, and error cost in both directions (refunds wrongly given, and wrongly refused). |
| A failure is | The agent applies the wrong policy, ignores credits already issued, or approves or refuses on a surface match. |
| Severity | Critical: a large wrongful refund, or a wrongful refusal that creates a legal or regulatory problem. High: a wrong policy applied. Medium: a correct outcome explained poorly. |
| Hand over to a person when | Policy is unclear or conflicting, the amount is above the limit, or the customer disputes the outcome. |

**Failures to test for this goal (from the library):**
- [Document-Level Retrieval Mismatch Pulls Wrong Billing-Dispute Template](../../by-use-case/customer-service/goals/refund-and-billing-disputes/failures/document-level-retrieval-mismatch-pulls-wrong-billing-dispute-template.md): A Billing-Dispute Agent That Retrieves a Dispute-Handling Template or Policy Article From a Knowledge Base Via Embedding Similarity to the…
- [Multi-Agent Handoff Drops Partial-Credit-Already-Issued Flag Between Triage and Billing Agent](../../by-use-case/customer-service/goals/refund-and-billing-disputes/failures/multi-agent-handoff-drops-partial-credit-already-issued-between-triage-and-billing-agent.md): A Triage Agent That Learns During Intake That a Customer Has Already Been Issued a Partial Credit for a Disputed Charge by a Prior Agent…

### G2. Stay within monetary authority

| Field | Definition |
|---|---|
| How to measure | Count of money-moving actions above the limit or without verification. Target: zero. Track total value issued against budget. |
| A failure is | The agent issues a credit because a customer asserted something, or exceeds a per-tool or daily budget. |
| Severity | Critical: any unauthorized payout. High: near misses that a limit should have caught. |
| Hand over to a person when | Any amount above the limit, any unverified claim, and any repeated refund to the same customer. |

**Failures to test for this goal (from the library):**
- [Unverified Customer Claim Triggers Autonomous Refund](../../by-use-case/support-services/goals/issue-resolution/failures/unverified-customer-claim-triggers-autonomous-refund.md): An Issue-Resolution Agent Authorized to Auto-Process Refunds Executes the Refund Directly Off the Customer's Narrated Claim Without Calling…

### G3. Explain every decision and keep a record

| Field | Definition |
|---|---|
| How to measure | Share of decisions with a stored rationale and the records consulted. Share of customers asking "why" after the reply. |
| A failure is | The agent gives no reason, a wrong reason, or leaves no record. |
| Severity | High: no record of a money-moving decision. Medium: an unclear explanation. |
| Hand over to a person when | A customer challenges a decision, or a regulator or auditor requests it. |

**Failures to test:** none documented in the library yet for this goal; this is a gap to fill.

### G4. Treat hardship and vulnerable customers with care

| Field | Definition |
|---|---|
| How to measure | Share of flagged hardship conversations that reach a trained person; complaints about tone in billing conversations. |
| A failure is | The agent quotes policy to someone describing hardship, or misses signals of crisis. |
| Severity | Critical: a crisis signal missed. High: hardship handled as a routine dispute. |
| Hand over to a person when | Any hardship or crisis signal. |

**Failures to test:** none documented in the library yet for this goal; this is a gap to fill.

## Conversation-level failures to check

This agent talks to people. Also test these:
- [hollow empathy](../../by-capability/human-machine-interface/goals/emotional-intelligence/failures/hollow-empathy.md)
- [missed crisis signals](../../by-capability/human-machine-interface/goals/vulnerable-users/failures/missed-crisis-signals.md)
- [no de-escalation strategy](../../by-capability/human-machine-interface/goals/difficult-customers/failures/no-de-escalation-strategy.md)

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Financial Limits](../../cross-cutting/operations/goals/tool-financial-limits/) | Credits and refunds are money-moving actions with budgets | 11 |
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | A refund that fails silently, or is reported done when it is not | 19 |
| [State Consistency](../../cross-cutting/operations/goals/state-consistency/) | Credits and refunds must not be applied twice or lost | 8 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | Partial credits must survive a handoff | 10 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | Approvals above the limit must reach a person | 8 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Every money decision needs a record | 8 |

## Security and governance to check

- [Tool Authorization Limits](../../cross-cutting/security/goals/tool-authorization-limits/) (security)
- [Approval Workflows](../../cross-cutting/governance/goals/approval-workflows/) (governance)
- [Tool Compliance Limits](../../cross-cutting/governance/goals/tool-compliance-limits/) (governance)
- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- The refund limit and who approves above it
- Which policy sources are authoritative by plan and region
- What evidence is required before a refund on a customer's claim
- What the agent says when it refuses

## Related

- [All agents by business goal](../)

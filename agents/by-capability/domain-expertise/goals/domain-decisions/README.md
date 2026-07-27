# What Are the Most Common Domain-Specific Decision Failures in AI Agents?

**Domain-decision failures happen when an agent has the right facts in front of it but applies the wrong rule, authority, or judgment to the facts** — approving an exception a policy doesn't allow, treating a critical issue as routine, or deciding a case that should have gone to a human expert. Unlike extraction or planning failures, domain-decision failures are judgment failures: the agent's inputs are often correct, but the domain-specific reasoning layered on top of the facts is wrong, which is why they surface in industries with dense, exception-laden rule sets — finance, healthcare, insurance, legal, and regulated support operations.

## Key Takeaways

- 10 distinct failure patterns affect domain-specific decision-making, split 4 "Rare but Catastrophic" (bad-concession/commitment, critical-field-error, no-should-not-decide-detection, regulatory-threshold-miss) against 6 "Common" (the rest) — the catastrophic quarter concentrates wherever money, compliance deadlines, or decision authority are at stake.
- Every pattern's Prevention section converges on the same architecture: an explicit, versioned, expert-reviewed rule/policy/hierarchy artifact (rule engine, source-of-truth hierarchy, commitment allowlist) that the agent queries, rather than a rule the agent infers from training data or context.
- Detection across all 10 patterns relies on comparing the agent's decision against an independent ground truth — a rule engine's expected output, an expert audit sample, or a source-of-truth database — rather than trusting the agent's own confidence or self-report.
- No domain-decision pattern is fixed by better prompting alone; every Mitigation Strategies section pairs a prevention gate with an escalation/audit loop, because domain rules change over time and drift must be caught in production, not just blocked at design time.

## Scope

- **Extraction & Classification Errors** — [Critical Field Error](failures/critical-field-error.md), [Document-Type Confusion](failures/document-type-confusion.md). The agent gets the raw input wrong (a misread amount, a misclassified document) before any domain judgment is even applied.
- **Rule & Compliance Application** — [Domain Rule Miss](failures/domain-rule-miss.md), [Regulatory Threshold Miss](failures/regulatory-threshold-miss.md), [Source-Of-Truth Confusion](failures/source-of-truth-confusion.md). The agent perceives the facts correctly but runs the facts through the wrong rule, misses a threshold, or trusts the wrong data source over the authoritative one.
- **Authority & Escalation Boundary** — [No 'Should Not Decide' Detection](failures/no-should-not-decide-detection.md), [Bad Concession/Commitment](failures/bad-concessioncommitment.md). The agent oversteps the decision authority it was actually granted — deciding what a human/expert should decide, or promising a term it has no standing to promise.
- **Severity & Business-Context Judgment** — [Risk Severity Misclassification](failures/risk-severity-misclassification.md), [Customer-Emotion Misread](failures/customer-emotion-misread.md), [Business-Context Blindness](failures/business-context-blindness.md). The agent correctly understands the situation but misjudges its human or business stakes — how urgent, how emotionally charged, or how commercially costly it really is.

## When Domain Decisions Matters

- An agent operates in a regulated domain with explicit thresholds, deadlines, or eligibility windows (financial limits, refund windows, compliance triggers) where missing one is a compliance incident, not just a wrong answer
- An agent extracts or classifies structured documents (paystubs, invoices, policies, claims) before making any downstream decision, so an upstream misread or misclassification silently corrupts everything after it
- An agent interacts with emotionally charged or high-stakes customer situations — debt collection, healthcare, complaints, escalations — where correctness alone doesn't guarantee an acceptable outcome

## Cross-Pattern Insight

Every one of the 10 domain-decision patterns treats the fix as an architecture problem, not a smarter-model problem. The recurring shape is: encode the domain's actual rules, thresholds, or source-of-truth hierarchy as a queryable, version-controlled, expert-reviewed artifact (rule engine, threshold validator, source hierarchy, commitment allowlist, abstention classifier); gate every relevant agent decision through it before execution; and independently audit a sample of decisions against expert judgment on a recurring cadence, because rules and thresholds change and drift has to be caught after deployment, not just blocked at design time. The pattern that generalizes furthest is escalation: "no-should-not-decide-detection" is effectively the meta-mitigation for the other nine — an abstention classifier that routes ambiguous, high-risk, or precedent-needed cases to a human before the agent ever reaches a rule-application or severity-judgment error.

## Frequently Asked Questions

### What's the difference between domain rule miss and regulatory threshold miss?
Domain rule miss is about industry-specific rules and their exceptions (e.g., a 60-day return window for defective products versus the standard 30 days); regulatory threshold miss is specifically about numeric limits, deadlines, and eligibility triggers required by compliance (credit limits, refund deadlines, age minimums). Both are fixed the same way — a queryable rule/threshold engine — but regulatory threshold miss carries harder compliance consequences and is rated "Rare but Catastrophic" versus domain rule miss's "Common."

### How is "no should-not-decide detection" different from the other domain-decision failures?
It is a meta-failure: the agent isn't necessarily getting the domain decision itself wrong, it's failing to recognize that the decision was never its call to make. The fix is an abstention classifier and escalation trigger framework that routes ambiguous, high-financial-risk, or precedent-needed cases to a human or domain expert before the agent commits to any decision at all.

### Can better prompting fix domain-decision failures?
No. Every pattern's mitigation strategy is architectural — a rule engine, a source-of-truth hierarchy, an escalation trigger, an audit sample — because the underlying problem is that the correct domain rule or threshold exists outside the model's parametric knowledge and changes over time. Prompting can't keep a rule set current or enforce that a rule engine was actually queried.

### Which patterns matter most for regulated or financial agent deployments?
Regulatory threshold miss, domain rule miss, and source-of-truth confusion are the three most directly tied to compliance exposure, since they govern whether an agent respects legal limits, industry-specific exceptions, and which data source is authoritative when sources disagree.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Bad Concession/Commitment](failures/bad-concessioncommitment.md) | Agent promises a refund, waiver, or SLA term it has no authority to honor |
| [Business-Context Blindness](failures/business-context-blindness.md) | A technically correct answer harms a business metric (LTV, churn, satisfaction) |
| [Critical Field Error](failures/critical-field-error.md) | Agent extracts the wrong amount, date, name, address, or ID |
| [Customer-Emotion Misread](failures/customer-emotion-misread.md) | Agent mishandles empathy in debt collection, healthcare, or complaint scenarios |
| [Document-Type Confusion](failures/document-type-confusion.md) | Agent misclassifies a paystub, W-2, bank statement, invoice, or policy document |
| [Domain Rule Miss](failures/domain-rule-miss.md) | Agent misses an industry-specific rule or its exception |
| [No 'Should Not Decide' Detection](failures/no-should-not-decide-detection.md) | Agent decides a case where a human or domain expert should have decided |
| [Regulatory Threshold Miss](failures/regulatory-threshold-miss.md) | Agent misses a compliance limit, deadline, or eligibility trigger |
| [Risk Severity Misclassification](failures/risk-severity-misclassification.md) | Agent treats a critical issue as minor, or a minor issue as critical |
| [Source-Of-Truth Confusion](failures/source-of-truth-confusion.md) | Agent trusts OCR/RAG text over the authoritative database or source document |

**Total: 10 patterns**

## Related Goals

- [Action Execution](../../../external-actions/goals/action-execution/) — once a domain decision is made, action execution covers the failures in actually executing the decision against external systems
- [Goal Understanding](../../../task-planning/goals/goal-understanding/) — objective and policy conflicts at the task level, one layer above domain-specific rule application
- [Planning](../../../task-planning/goals/planning/) — sequencing and decomposition failures that can precede a domain decision even being reached

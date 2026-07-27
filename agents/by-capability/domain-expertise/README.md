# What Are the Most Common Domain-Expertise Failures in AI Agents?

**AI agents most often fail at domain expertise not by lacking facts, but by misapplying domain-specific judgment to facts they already have** — missing an industry rule's exception, misjudging how severe an issue really is, promising a commitment they have no authority to make, or deciding a case that should have escalated to a human expert instead. Because domain-expertise failures are judgment failures rather than knowledge gaps, they concentrate in regulated, rule-heavy domains — finance, healthcare, insurance, legal, and compliance-sensitive support — where a technically defensible decision can still be the wrong one.

## Key Takeaways

- Domain expertise currently covers 1 goal — Domain Decisions — and 10 failure patterns, spanning extraction and classification errors, rule and compliance application, authority boundaries, and severity/business-context judgment.
- 4 of the 10 patterns (bad-concession/commitment, critical-field-error, no-should-not-decide-detection, regulatory-threshold-miss) are rated "Rare but Catastrophic," concentrated wherever money, compliance deadlines, or decision authority are directly at stake.
- Every pattern's fix is architectural rather than prompt-based: a versioned, expert-reviewed rule engine, threshold validator, or source-of-truth hierarchy that the agent queries and is audited against, not a rule the agent is expected to infer correctly on its own.
- The escalation pattern generalizes across the whole category: "no-should-not-decide-detection" functions as a meta-mitigation, routing ambiguous or high-risk cases to a human before the agent ever reaches a rule-application, severity, or authority error.

## Domain Expertise Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Domain Decisions](goals/domain-decisions/) | Applying industry-specific rules, thresholds, source-of-truth hierarchies, and escalation judgment correctly to a given case | 10 |

**Total: 10 patterns**

## How the Goals Relate

Domain expertise is currently a single-goal category, so there's no internal pipeline to describe — Domain Decisions covers the full arc from misreading a document's fields, through misapplying a rule or threshold, to overstepping decision authority or misjudging severity. If a debugging session narrows to "the agent had the right facts but made the wrong call," Domain Decisions is the goal to check regardless of which stage of that arc the wrong call happened at.

## Frequently Asked Questions

### What's the difference between a domain-expertise failure and a document-processing failure?
Document-processing failures are about getting the raw content of a document wrong — misread characters, lost table structure, hallucinated field values. Domain-expertise failures assume the content was read correctly and are about applying the right industry rule, threshold, or judgment to that correctly-read content. Critical-field-error and document-type-confusion sit at the boundary, since a misclassified or misread document can trigger a domain-decision failure downstream. See [Document Processing](../document-processing/).

### Can a stronger or more knowledgeable model fix domain-expertise failures on its own?
No. Every domain-decision pattern's Prevention section calls for an external, versioned, expert-reviewed rule artifact (rule engine, threshold validator, source hierarchy) rather than relying on the model's parametric knowledge of a domain, because the actual rules, thresholds, and exceptions change over time and are specific to a business's current policy — not general knowledge a model can be expected to have memorized correctly or kept current on.

### Which domain-decision pattern should a developer check first when debugging a wrong agent decision?
Start with what kind of "wrong" it was: if the agent misread the input, check critical-field-error or document-type-confusion; if it applied the wrong rule or trusted the wrong data source, check domain-rule-miss, regulatory-threshold-miss, or source-of-truth-confusion; if it overstepped its authority, check no-should-not-decide-detection or bad-concession/commitment; if it misjudged the stakes, check risk-severity-misclassification, customer-emotion-misread, or business-context-blindness.

## Related Categories

- [Document Processing](../document-processing/) — upstream failures in reading and classifying the documents that domain decisions are made from
- [External Actions](../external-actions/) — downstream failures in executing the action a domain decision produces
- [Task Planning](../task-planning/) — goal- and plan-level failures that operate one layer above domain-specific rule application

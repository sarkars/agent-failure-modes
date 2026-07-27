# What Are the Most Common Clinical Documentation Failures in AI Agents?

**Clinical documentation failures happen when an agent transforms chart data into structured output — a discharge summary, an after-visit note, a billing code — without explicitly grounding each element in what actually occurred during the encounter, so the agent fills gaps with plausible-sounding boilerplate or unverified transformations that the underlying source never supported.** Empty allergy fields become "no known drug allergies," unperformed ROS elements become documented, and billing codes become inflated by the language the agent chose to use rather than the clinical encounter that took place.

## Key Takeaways

- 2 patterns are documented, both rooted in the same mechanism: transformation of source data into structured output without explicit fidelity verification.
- Allergy fields can be empty for two opposite reasons — never populated, or affirmatively confirmed negative — and a query returning zero records collapses both cases unless explicitly distinguished, causing the agent to render an unconfirmed-empty state as a confident "no known allergies" statement.
- E/M billing code derivation from AI-generated documentation creates a two-step liability: first, the agent inflates or deflates the note's language relative to actual encounter content; second, the billing engine derives a code from the inflated or deflated language, and that code reflects not the encounter but the agent's narrative choices.

## Scope

Both clinical-documentation patterns stem from a single root cause: the agent generates or transforms source data without a verification step that confirms the output accurately represents the source. Empty-allergy-field handling conflates two structurally different cases (never-populated vs. confirmed-negative) because the query interface cannot distinguish between never-populated and affirmatively-confirmed-negative, so the output defaults to a confident statement that the source never supported. Upcoding/downcoding happens because the agent optimizes for a complete-sounding note rather than a grounded-in-source note, and downstream billing automation trusts the note's language rather than re-verifying what was actually performed.

## When Clinical Documentation Matters

- After-visit summaries and discharge notes that become the record-of-truth for downstream teams and for the patient
- Billing-code derivation from AI-drafted notes, where the note's language mechanically determines code level
- Care transitions where a prior note's documentation of "no known allergies" silently propagates forward without confirmation

## Cross-Pattern Insight

Both patterns documented here reflect a gap between what an agent can convincingly narrate and what the underlying source actually supports. A model trained to produce well-formed, complete clinical notes tends toward generating template-complete content — "ROS reviewed," "allergies confirmed" — whether or not the encounter transcript supports each claim. The recurring mitigation is the same: ground every generated element in an explicit source signal, and when source-signal is missing or ambiguous, render the output as unverified rather than defaulting to a confident complete-sounding statement.

## Frequently Asked Questions

### How do you catch false "no known drug allergies" statements in AI-generated notes?
Distinguish at query time whether an empty allergy field is a result of "never populated" or "affirmatively confirmed." Require the note-generation step to cite confirmation metadata (date, clinician) for any NKDA statement; absent that metadata, render the allergy history as unverified rather than as confirmed negative.

### Does upcoding from AI documentation differ from billing audits?
Upcoding risk from AI documentation is a superset of billing audit risk: traditional notes were written by clinicians who understand billing implications, so upcoding was mostly inadvertent; AI-generated notes optimize for completeness and fluency, not for billing accuracy, so inflated language becomes a systematic failure mode. See [Documentation-Driven Upcoding/Downcoding Risk](failures/upcoding-downcoding-risk.md).

### Can you prevent note inflation without restricting AI documentation quality?
Yes. Ground every documented element in a source signal (transcript timestamp, structured form field, chart action), and reject generation that infers details without source evidence. Require a clinician to attest that the draft matches what was actually performed, before the note is finalized.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Empty Allergy-Query Result Documented as Confirmed No-Known-Allergies](failures/empty-allergy-query-result-documented-as-confirmed-no-known-allergies.md) | Never-populated allergy field rendered as affirmatively confirmed negative, not flagged as unverified |
| [Documentation-Driven Upcoding/Downcoding Risk](failures/upcoding-downcoding-risk.md) | Agent-generated note language inflates or deflates billing code level independent of actual encounter content |

**Total: 2 patterns**

## Related Goals

- [Compliance & Liability](../compliance-liability/) — covers HIPAA de-identification and informed-consent documentation gaps, a level up from data-fidelity issues
- [Diagnosis Safety](../diagnosis-safety/) — documentation failures cascade into downstream diagnostic reasoning when false prior notes anchor future assessments

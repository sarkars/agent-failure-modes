# Input Default Value Assumption

## Issue
An agent receives an input payload with a missing or null field and silently substitutes what it assumes is a "safe" default (zero, empty string, current date, `false`, the first enum value) instead of treating the absence as an error or asking for clarification. The assumed default is often wrong for the specific business context — a missing `discount_percent` treated as `0` when it should have blocked the order, or a missing `region` treated as `"US"` when the request originated elsewhere — and the agent proceeds to act on that fabricated value as if it were provided.

**Frequency**: Common

**Symptoms**
- Records processed with values the user never supplied and never reviewed
- Downstream reports showing suspicious clustering around common defaults (0, "N/A", today's date, "US")
- Business logic silently branches down the "default" path for a field that was actually required
- No error, warning, or flag anywhere indicating the field was missing at input time
- Discrepancies only surface when someone manually reconciles agent output against the original source request

## Root Cause
Many agent input schemas and the tool/function-calling frameworks that back them mark fields as "optional" for parsing convenience rather than business correctness, and the agent's underlying model has a strong prior toward completing a plausible-looking record rather than halting on ambiguity. When a field is absent, the agent pattern-matches to the most common value it has seen in training or in prior calls within the session, and treats "I can produce a complete-looking object" as success — even though completeness and correctness are different things. The failure is compounded when the schema itself conflates "field can be omitted" with "field has a universally safe default," a distinction the schema author often didn't make explicit.

## Example
```
A procurement agent processes a purchase-order intake form. The form schema
marks "approval_tier" as optional, defaulting to "standard" if absent, on
the assumption that most requests are standard-tier.

A finance team submits a $340,000 equipment order via an integration that,
due to a mapping bug, drops the approval_tier field entirely (it should
have been "executive").

The agent receives the order with no approval_tier, applies the schema
default of "standard", and routes it through the standard approval queue
(single manager sign-off, $50K limit) instead of the executive queue
(three-signature, board-notification required).

The order is approved by a single manager who has no visibility into the
$50K limit being exceeded, because the agent's default made the order
look routine. The gap is discovered five weeks later during a quarterly
spend audit.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of "optional field" defaults in agent input schemas are context-dependent rather than universally safe | Estimated from schema audits of production agent tool definitions |
| Missing-field defaulting is implicated in a notable share of silent data-quality incidents traced back to agent intake pipelines | Typical range observed across incident postmortems |
| Adding explicit "required-if-absent-then-escalate" rules for high-impact fields cuts related incidents substantially | Reported range across teams that added field-criticality tiers |

## Mitigations
1. **Criticality-tiered schemas**: Classify each optional field as "safe-to-default", "must-escalate-if-absent", or "must-reject-if-absent" at schema design time, rather than letting the agent infer criticality at runtime.
2. **Explicit default provenance**: When a default is applied, tag the output record with metadata (`approval_tier: "standard" (defaulted, not provided)`) so downstream consumers and auditors can distinguish supplied values from assumed ones.
3. **Ask-don't-assume for high-stakes fields**: Require the agent to pause and request clarification, rather than default, whenever a missing field feeds into an irreversible or high-value decision.
4. **Upstream schema validation**: Validate incoming payloads against a strict schema before they reach the agent, so mapping bugs that drop fields are caught at the integration boundary instead of silently absorbed by an agent-side default.
5. **Default audit sampling**: Periodically sample records where defaults were applied and manually verify the default was correct for that specific case, feeding discrepancies back into the criticality tiering.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| defaulted_field_rate | Share of processed records where one or more fields were defaulted rather than supplied | Alert if > 10% for any single field |
| high_criticality_default_count | Count of records where a "must-escalate" field was silently defaulted | Alert if > 0 |
| default_reversal_rate | Share of defaulted records later corrected by a human reviewer | Alert if > 5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Critical field defaulted | A field tagged "must-escalate-if-absent" is missing from input and defaulted anyway | High | Halt processing of that record, page data-quality owner, trace upstream source |
| Default rate spike | defaulted_field_rate for any field exceeds its alert threshold within a rolling window | Medium | Investigate upstream integration for a mapping regression |

## Related Patterns
- [Input Schema Evolution](./input-schema-evolution.md) - an upstream schema change is one common cause of fields silently going missing and triggering default assumptions
- [Input Validation Bypass](./input-validation-bypass.md) - both involve the agent accepting input that should have been rejected rather than silently accepted
- [Output Type Coercion Failure](./output-type-coercion-failure.md) - a related failure where an assumed value, once produced, is misinterpreted downstream

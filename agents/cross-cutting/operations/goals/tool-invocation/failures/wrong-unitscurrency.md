# Wrong Units/Currency

## Issue: Agent sends cents vs dollars, UTC vs local, kg vs grams.

**Frequency**: Common

**Symptoms**
- Magnitude/unit errors in action/output.
- Output or tool call is off by a fixed multiplicative factor (100x for cents/dollars, 1000x for grams/kg) that isn't caught because the number still looks plausible.

**Root Cause**
Agent sends cents vs dollars, UTC vs local, kg vs grams.

**Example**
```
A pricing API returns a product's price as a raw integer in cents
(`4999`), with no unit suffix in the field name. The agent reads this
as dollars and displays "$4999" for a product that actually costs
$49.99, and if it also uses the same value to construct a charge, the
customer is billed 100x the intended amount.
```

**Contributing Factors**
- API returns raw integer values in a minor unit (cents, grams) without an explicit unit label in the field name or docs.
- Agent's training/prior exposure biases it toward assuming "natural" units (dollars, kg) unless the schema states otherwise.
- No sanity-range check on the resulting value (e.g. a $4999 latte) before it's surfaced or acted on.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Minor-unit field misread | Return a price/weight field in cents/grams with no explicit unit suffix in the field name | Agent checks the tool schema's documented unit and converts correctly before displaying or acting on it | Agent treats a minor-unit value as the major unit, producing a 100x/1000x magnitude error |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| unit_conversion_error_rate | < 0.5% of numeric fields carrying implicit units | Sample tool calls/outputs involving currency, weight, or time-duration fields and check for magnitude-consistent conversion |

---

## Mitigation Strategies

### Prevention
1. **Explicit Unit Tagging on All Numeric Fields**: Every numeric value flowing between tools and the agent carries an explicit unit annotation (currency code plus minor-unit convention, mass unit, time unit) in its schema/metadata, so a bare number like "100" is never passed around without the agent having to guess its scale.
2. **Conversion Validators at Tool Boundaries**: Each tool's input schema declares its expected unit (e.g., "amount in cents, ISO 4217 currency code required"), and a boundary validator checks incoming values against expected magnitude/format before the call executes.
3. **Single Source of Truth for Unit Conversion**: All unit/currency conversions go through one shared, tested conversion library/function rather than ad hoc arithmetic scattered across prompts or tool-call construction, eliminating inconsistent cents/dollars or kg/g handling between different code paths.

### Detection & Response
1. **Magnitude Sanity Checks Pre-Send**: Before a write call with a monetary/quantity field executes, the value is compared against a plausible range for that field (a "price" over $1,000,000 or under $0.01 for a typical retail item), and outliers are flagged for confirmation rather than silently sent at 100x or 0.01x the intended amount.
2. **Post-Write Reconciliation Against Source**: After a financial or quantity write, the recorded value in the target system is reconciled against the originally-stated user intent (user said "charge $49.99", verify the charge object shows 4999 cents, not 499900); mismatches trigger an immediate reversal workflow.
3. **Cross-System Unit Drift Audit**: Values passed between systems with different unit conventions (internal ledger in cents, display layer in dollars, partner API in a third convention) are periodically sampled and checked for round-trip consistency, catching drift introduced by a recent integration change.

### Architecture Patterns
1. **Strongly-Typed Money/Quantity Objects**: Monetary and physical-quantity values are represented as structured objects (`Money{amount_minor_units, currency_code}`, `Mass{value, unit}`) throughout the codebase and tool schemas, never as bare floats/ints, so unit information travels with the value and can't be silently dropped.
2. **Unit-Aware Serialization Layer**: The layer that serializes agent-constructed arguments into API payloads enforces the target API's declared unit convention automatically, converting from the internal canonical representation, so the agent reasons in one consistent unit system while each downstream tool still gets what it expects.
3. **Idempotent Correction/Reversal Workflow**: Because unit errors on financial writes are high-impact, a fast reversal path (void/refund/adjust) is pre-built and tested so that when a magnitude error is caught, correction is a single automated action rather than a manual support ticket.

### Metrics
1. **magnitude_outlier_flag_rate_percent**: Target: < 0.5% of monetary/quantity writes; Alert threshold: > 2%
2. **post_write_reconciliation_mismatch_rate_percent**: Target: 0%; Alert threshold: > 0.1%
3. **unit_tagged_field_coverage_percent**: Target: 100% of numeric tool-call fields; Alert threshold: < 98%
4. **reversal_workflow_invocation_count_per_week**: Target: < 2; Alert threshold: >= 5

### Alerts
1. **Post-Write Magnitude Mismatch** (P1 - Critical): Condition - reconciliation finds a written value differs from stated user intent by an order-of-magnitude-consistent factor (100x, 1000x). Action: Immediate auto-reversal/hold, notify finance/on-call, audit the conversion path.
2. **Magnitude Outlier Blocked Pre-Send** (P2 - Warning): Condition - the boundary validator flags an outlier value before send. Action: Require explicit confirmation before proceeding, log for pattern review.
3. **Unit Coverage Gap Detected** (P3 - Info): Condition - unit_tagged_field_coverage_percent drops below target after a tool/schema change. Action: File a ticket to add unit metadata to the affected fields.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| unit_magnitude_error_incidents_per_week | > 1 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Implausible Magnitude Detected | Output value for a known-unit field falls outside a sane range (e.g. price > $10,000 for a retail SKU) | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.

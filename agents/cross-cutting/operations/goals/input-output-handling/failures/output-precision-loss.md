# Output Precision Loss

## Issue
An agent generates or serializes a numeric value in a way that loses precision relative to the actual computed or intended value — rounding a currency amount that needed exact cent-level precision, formatting a large integer through a floating-point representation that can't represent it exactly, or truncating decimal places in a scientific/financial figure. The output looks like a reasonable number and passes any type check, but its value is subtly different from the correct one, and that difference compounds when the number feeds further calculation.

**Frequency**: Occasional

**Symptoms**
- Financial or accounting totals that don't reconcile exactly with a source system, off by fractions of a cent that accumulate across many transactions
- Large integer IDs (e.g. 64-bit identifiers) that come back altered after passing through a JSON serialization step, because JSON numbers are commonly parsed as IEEE 754 doubles
- Scientific/measurement values losing significant digits after round-tripping through a formatting or string-conversion step
- Discrepancies that only appear after aggregation (summing many slightly-imprecise values) rather than being visible in any single value
- Reconciliation processes flagging small, consistent-direction differences between an agent-reported total and a system-of-record total

## Root Cause
Several distinct mechanisms cause this, and they're often conflated: (1) floating-point binary representation cannot exactly represent many decimal fractions (0.1 + 0.2 != 0.3 in IEEE 754), so currency and other exact-decimal values silently accumulate rounding error if represented as floats rather than a fixed-point/decimal type; (2) JSON's number type has no distinction between integer and float, and many JSON parsers deserialize all numbers as double-precision floats, which can only exactly represent integers up to 2^53 — beyond that, large IDs silently lose precision during serialization/deserialization; (3) formatting logic that applies a fixed number of decimal places for display purposes gets reused for the value that's actually stored or transmitted, conflating "how many digits to show a human" with "how much precision the underlying computation needs to retain." In all three cases, the loss happens silently because the resulting number is still a syntactically valid number — there's no error, just a wrong value.

## Example
```
A billing-reconciliation agent aggregates thousands of line-item charges,
each represented as a floating-point dollar amount, and reports a daily
total to the finance team:

    total = sum(float(item["amount"]) for item in daily_charges)

Individual charges are values like $19.99, $4.50, $132.87. Represented
as IEEE 754 doubles, many of these don't have an exact binary
representation, and small rounding errors accumulate across the roughly
14,000 line items processed that day. The agent reports a total of
"$287,441.31" when the exact decimal sum, computed by the source
accounting system using fixed-point arithmetic, is "$287,441.28" -- a
three-cent discrepancy.

Three cents is dismissed as noise on any single day, but the same
floating-point summation runs daily, and finance's month-end
reconciliation against the general ledger shows a small, persistently
nonzero variance that takes an analyst most of a day to trace back to
the agent's aggregation step using floats instead of a decimal type.
```

## Statistics
| Finding | Context |
|---------|---------|
| IEEE 754 double-precision floats cannot exactly represent the majority of decimal fractions used in currency values, causing small but nonzero representation error on most such values | Well-established characteristic of binary floating-point arithmetic |
| JSON numbers exceeding 2^53 (~9 quadrillion) commonly lose precision when parsed by JavaScript-based or double-precision-based JSON parsers | Well-established characteristic of the JSON/JS number type |
| Switching currency and large-ID handling to fixed-point decimal types and string-typed large integers eliminates the large majority of precision-loss incidents in financial/ID pipelines | Estimated from the structural nature of the fix relative to the failure mechanism |

## Mitigations
1. **Use fixed-point/decimal types for currency and exact-decimal values**: Represent currency and any value requiring exact decimal arithmetic using a dedicated decimal type (not `float`/`double`) throughout computation, serialization, and storage.
2. **Serialize large integers as strings, not JSON numbers**: For IDs or values that may exceed 2^53, serialize them as strings in JSON payloads rather than native numbers, avoiding silent precision loss in double-precision-based parsers.
3. **Separate display formatting from stored/transmitted precision**: Never let a display-oriented rounding/formatting function (e.g. "show 2 decimal places") also determine the precision of the value that's stored or passed to the next computation step.
4. **Reconciliation checks against a precision-safe source**: For financial aggregation specifically, periodically reconcile agent-computed totals against a system of record computed with exact decimal arithmetic, and alert on any nonzero variance rather than treating small discrepancies as acceptable noise.
5. **Precision-aware testing with known problematic values**: Include test cases with values known to expose floating-point representation error (e.g. repeated additions of 0.1-scale amounts) and large IDs near the 2^53 boundary in routine test suites.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| reconciliation_variance | Absolute difference between agent-computed totals and system-of-record totals over the same period | Alert if != 0 for financial totals |
| large_integer_precision_mismatch_count | Count of large ID values that differ after a serialize/deserialize round-trip | Alert if > 0 |
| float_typed_currency_field_count | Count of currency-bearing fields represented as float/double rather than a decimal type in the codebase | Alert on any presence (track as a standing code-quality metric) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Nonzero financial reconciliation variance | Agent-reported total differs from system-of-record total by any nonzero amount | High | Halt affected report from being finalized, trace aggregation logic for float usage |
| Large ID round-trip mismatch | A large integer ID differs after passing through JSON serialization/deserialization | High | Patch serialization to use string representation, audit for corrupted references |

## Related Patterns
- [Output Type Coercion Failure](./output-type-coercion-failure.md) - a related numeric/type-fidelity failure where a value's type, not just its precision, is altered incorrectly downstream
- [Input Locale Mismatch](./input-locale-mismatch.md) - a related numeric-fidelity failure on the input side, where decimal-separator confusion produces a wrong value that also parses cleanly
- [Output Ordering Nondeterminism](./output-ordering-nondeterminism.md) - both are subtle data-fidelity failures that produce plausible-looking output that only proves wrong under close comparison

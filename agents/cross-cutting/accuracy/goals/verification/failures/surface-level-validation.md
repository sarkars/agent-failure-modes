# Surface-Level Validation

## Issue: Checks formatting but not semantic correctness.

**Frequency**: Common

**Symptoms**
- JSON valid but business data wrong.
- [Add more specific symptoms]

**Root Cause**
Checks formatting but not semantic correctness.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Semantic Validation Layer Beyond Schema Checks**: Implement domain-specific business-rule validators (value range checks, cross-field consistency, referential integrity against source records) that run after schema validation passes, since valid JSON/structure says nothing about whether the values are correct.
2. **Domain Rule Engine for Business Invariants**: Encode known business invariants (e.g., total = sum of line items, dates in valid range, status transitions follow allowed state machine) as an explicit rule engine that every output must pass, separate from and in addition to format validation.
3. **Semantic Test Cases in Eval Suite Distinct from Format Tests**: The eval suite explicitly separates "is this valid JSON/schema" test cases from "is this semantically/business-correct" test cases, so a 100% format-pass rate can never be mistaken for content correctness.

### Detection & Response
1. **Cross-Field Consistency Auditing**: Run automated checks on production outputs for internal consistency (do totals match line items, do referenced IDs exist, are dates logically ordered) independent of schema validity, flagging structurally valid but semantically broken records.
2. **Sampled Semantic Accuracy Review**: Periodically sample schema-valid production outputs for human review against the actual business intent/source data, tracking semantic error rate separately from format error rate.
3. **Business-Rule Violation Rate Tracking**: Monitor the rate at which schema-valid outputs fail domain rule engine checks; a nonzero and growing rate indicates format validation is being used as a false proxy for correctness.

### Architecture Patterns
1. **Two-Stage Validation Pipeline**: Output validation is explicitly split into a syntactic stage (schema/format) and a semantic stage (business rule engine, cross-field checks, source comparison), with both required to pass before an output is accepted — neither stage alone is sufficient.
2. **Business Rule Engine as a Standalone Service**: Domain invariants are maintained in a separate, versioned rule engine (not embedded ad hoc in the agent prompt) so rules can be audited, tested, and evolved independently of the generation logic.
3. **Source-Comparison Semantic Checker**: For outputs derived from source data (extracted fields, computed values), a dedicated checker recomputes or looks up the expected value from the source and compares it to the generated value, catching semantic errors that pass schema validation.

### Metrics
1. **schema_valid_but_semantically_wrong_rate_pct**: Target: < 1%; Alert threshold: > 5%
2. **business_rule_violation_rate_pct**: Target: < 1% of schema-valid outputs; Alert threshold: > 5%
3. **cross_field_consistency_pass_rate_pct**: Target: 100%; Alert threshold: < 98%
4. **semantic_eval_coverage_ratio**: Target: >= 1:1 semantic test cases to format test cases; Alert threshold: < 1:3

### Alerts
1. **Business Rule Violation on Schema-Valid Output** (P1 - Critical): Condition - output passes schema validation but fails a business invariant (totals mismatch, invalid state transition, broken referential integrity). Action: Block output delivery, route to human review, log for rule-engine gap analysis.
2. **Semantic Error Rate Rising** (P2 - Warning): Condition - sampled semantic accuracy review shows error rate above 5% while format-pass rate remains at 100%. Action: Investigate whether recent changes introduced semantic drift, expand semantic eval coverage.
3. **Semantic Test Coverage Gap** (P3 - Info): Condition - semantic-to-format test case ratio falls below 1:3. Action: Schedule eval suite audit to add business-rule-focused cases.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.

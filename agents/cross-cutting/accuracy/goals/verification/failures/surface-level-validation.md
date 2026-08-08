# Surface-Level Validation

## Issue: Checks formatting but not semantic correctness.

**Frequency**: Common

**Symptoms**
- JSON valid but business data wrong.
- Output passes schema/format validation at 100% while a business invariant (line-item totals summing to the invoice total, status transitions following the allowed state machine) is silently violated.
- Engineers treat "the pipeline didn't throw a validation error" as equivalent to "the output is correct," with no separate semantic check ever run.

**Root Cause**
This gap exists because validation is typically built as a single schema/format-checking stage with no separate semantic or business-rule layer on top of it, and business invariants -- totals must reconcile, dates must be logically ordered, status transitions must follow the state machine -- are never explicitly encoded anywhere in the system for a check to enforce. The problem is reinforced at the team level: "valid JSON" and "correct answer" get conflated in dashboards and communication, so a 100% format-pass rate reads as a correctness guarantee, and eval suites mirror this bias by testing format compliance thoroughly while carrying few or no semantic test cases distinct from the format ones.

**Example**
```
An invoice-extraction agent outputs perfectly well-formed JSON: correct field names,
correct types, valid schema. It passes format validation every time. But on one invoice,
it extracts a line-item total of $1,200 while the sum of the individual line items is
actually $1,450 -- it picked up a subtotal field instead of the true total. The schema
validator has nothing to say about this: the JSON is syntactically perfect. Only a
business-rule check (does total equal sum of line items) would have caught it, and no
such check exists in the pipeline.
```

**Contributing Factors**
- Validation logic is built as a single schema/format check, with no separate semantic or business-rule validation stage layered on top.
- Business invariants (totals must reconcile, dates must be logically ordered, status transitions must follow the state machine) are never explicitly encoded anywhere in the system.
- "Valid JSON" and "correct answer" are conflated in team communication and dashboards, so a 100% format-pass rate is mistaken for a correctness guarantee.
- Eval suites test format/schema compliance thoroughly but have few or no semantic test cases distinct from format tests.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Total-vs-line-items reconciliation | Invoice with mismatched subtotal/total fields but valid JSON schema | Business rule engine flags the mismatch, output blocked or routed for review | Schema-valid output ships with a mismatched total |
| Status transition validity | Extracted record showing a status transition not allowed by the state machine | Output rejected by domain rule engine despite valid schema | Schema-valid output with an invalid state transition ships unflagged |
| Semantic vs. format test ratio audit | Full eval suite inventory | At least a 1:1 ratio of semantic to format test cases | Format test cases vastly outnumber semantic/business-correctness cases |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| schema_valid_but_semantically_wrong_rate_pct | < 1% | Sample schema-valid production outputs and check business correctness against source data |
| business_rule_violation_rate_pct | < 1% of schema-valid outputs | Run domain rule engine checks over schema-valid outputs and measure violation rate |
| semantic_eval_coverage_ratio | >= 1:1 semantic test cases to format test cases | Count and classify eval suite test cases by type |

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
| schema_valid_but_semantically_wrong_rate_pct | > 5% |
| business_rule_violation_rate_pct | > 5% of schema-valid outputs |
| cross_field_consistency_pass_rate_pct | < 98% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Business Rule Violation on Schema-Valid Output | Output passes schema validation but fails a business invariant | High |
| Semantic Error Rate Rising | Sampled semantic accuracy review shows error rate above 5% while format-pass rate remains at 100% | Medium |
| Semantic Test Coverage Gap | Semantic-to-format test case ratio falls below 1:3 | Low |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.

# Intermediate Result Corruption

## Issue: Agent misreads/transforms tool output incorrectly.

**Frequency**: Common

**Symptoms**
- Value changes between tool output and final answer.
- [Add more specific symptoms]

**Root Cause**
Agent misreads/transforms tool output incorrectly.

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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent that calls a pricing tool returning structured data, then free-text-summarizes the result into a natural-language response rather than using a typed extraction layer or verbatim pass-through for critical values
- No chain-of-custody diff or tool-output-to-answer consistency check runs before the response is sent
- The pricing tool returns a value with several decimal places and a specific currency

### Trigger Mechanism
1. The user asks for the total cost of an order
2. The pricing tool returns a structured response: `{total: 1234.56, currency: "USD"}`
3. The agent, generating the final answer in free text, misreads or mistransforms the value while composing prose (e.g., transposing digits or dropping a decimal place)
4. The final response is sent to the user with the corrupted value, with no automated check catching the discrepancy

### Example Reproduction Steps
```
1. Tool call: get_order_total(order_id="ORD-99") -> {total: 1234.56,
   currency: "USD"}
2. Agent generates: "Your total comes to $1,234.65" (digits
   transposed: 56 -> 65) or "$123.45" (decimal place dropped)
3. Compare the generated response text against the original tool
   response value -> mismatch detected
4. Check for a typed extraction/verbatim-pass-through step between
   tool output and final generation -> none present; value was
   re-derived through free-text generation
5. Run the tool-output-to-answer consistency check retroactively ->
   flags the mismatch that shipped to the user
```

### Expected Failure State
The customer receives an incorrect total ($1,234.65 or $123.45 instead of the actual $1,234.56) because the value passed through free-text generation rather than a verbatim pass-through from the structured tool response, and no consistency check caught the transcription error before sending. A correctly defended system copies the `total` field directly from the structured tool response into the final output template, or runs a chain-of-custody diff that blocks the send when the generated value doesn't byte-for-byte match (allowing only declared formatting transforms) the original tool output.

## Mitigation Strategies

### Prevention
1. **Structured, Schema-Validated Extraction**: Instead of letting the model freely re-summarize raw tool output in prose, require it to extract critical values (numbers, IDs, dates) into a typed, schema-validated structure (e.g., JSON with declared field types) immediately after the tool call. Schema validation rejects malformed or out-of-range extractions before they propagate further.
2. **Verbatim Pass-Through for Critical Values**: For values that must be reproduced exactly (prices, quantities, account numbers, dates), the pipeline copies the value directly from the structured tool response into the final output template rather than routing it through the model's free-text generation, eliminating the transcription step where corruption occurs.
3. **Chain-of-Custody Diffing**: After each transformation step (tool output → extracted value → final answer), automatically diff the value against its immediate predecessor. Any change other than expected formatting (e.g., currency symbol, rounding within declared precision) blocks the pipeline and requires explicit justification.

### Detection & Response
1. **Tool-Output-to-Answer Consistency Check**: Before sending the final response, re-parse it for any values that correspond to tool-output fields and compare them byte-for-byte (allowing declared formatting transforms) against the original tool response. Mismatches block the send and route to regeneration or human review.
2. **Statistical Drift Monitoring on Numeric Fields**: Track the distribution of transformations applied to numeric fields (e.g., typical rounding, unit conversions) and flag responses where a value's transformation falls outside the normal pattern (e.g., a 10x magnitude change) as likely corruption.
3. **Sampled Human Audit of High-Stakes Transformations**: For domains where corruption has high impact (financial totals, medical dosages, legal dates), route a sample of tool-output-to-answer pairs to human reviewers to catch corruption patterns the automated diff doesn't yet cover.

### Architecture Patterns
1. **Typed Extraction Layer**: A dedicated post-tool-call step parses raw tool output into a strongly-typed intermediate representation (using JSON schema or a typed DTO) before any natural-language generation touches the data, so downstream generation reads from validated structured fields, not re-derives them from prose.
2. **Value Provenance Tagging in Generation**: When the generation step inserts a value sourced from tool output, it tags that span with a provenance pointer (tool_call_id, field_path) in an internal representation, enabling the consistency-check step to trace and verify every numeric/critical value in the final text.
3. **Diff-and-Block Pipeline Stage**: Insert a pipeline stage between "draft answer" and "send answer" that runs the chain-of-custody diff and consistency check; on failure it blocks the send and either triggers regeneration with the corrected value forced in, or escalates to human review.

### Metrics
1. **value_mismatch_rate_percent**: Target: < 0.1% of responses referencing tool output; Alert threshold: > 1%
2. **schema_validation_failure_rate_percent**: Target: < 0.5% of extractions; Alert threshold: > 2%
3. **blocked_send_due_to_diff_failure_count**: Target: tracked baseline; Alert threshold: sudden 3x spike
4. **high_stakes_audit_error_rate_percent**: Target: < 0.2%; Alert threshold: > 1%

### Alerts
1. **Critical Value Mismatch Reached User** (P1 - Critical): Condition - post-send audit or user report confirms a tool-output value was corrupted in the final answer (e.g., wrong price, wrong dosage). Action: Immediate correction sent to user, incident review of the extraction/generation path, add case to regression suite.
2. **Extraction Schema Validation Failures Rising** (P2 - Warning): Condition - schema_validation_failure_rate_percent exceeds 2% over a rolling day. Action: Investigate tool output format changes or extraction prompt drift, patch schema or extraction logic.
3. **Diff-and-Block Stage Blocking Excessively** (P3 - Info): Condition - blocked_send_due_to_diff_failure_count spikes 3x above baseline. Action: Review recent tool or model changes, distinguish genuine corruption catches from false-positive diff rules, tune thresholds.

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

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.

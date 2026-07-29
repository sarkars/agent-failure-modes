# Intermediate Result Corruption

## Issue: Agent misreads/transforms tool output incorrectly.

**Frequency**: Common

**Symptoms**
- Value changes between tool output and final answer.
- Numeric transcription errors (transposed digits, dropped decimal places, unit mismatches) appear only in the free-text response, never in the tool's raw output.
- No automated diff exists between the structured tool response and the final generated text, so corruption ships silently.
- Critical values (prices, IDs, dates) are re-derived through prose generation rather than copied verbatim from structured data.
- Corruption rate correlates with response length or complexity, since longer free-text summarization gives more opportunity for transcription drift.

**Root Cause**
Agent misreads/transforms tool output incorrectly.

**Example**
```
Tool call: get_account_balance(account="AC-4471")
  -> {balance: 8032.10, currency: "USD", as_of: "2026-07-29"}

Agent's generated response: "Your current balance is $8,320.10 as of
July 29." (digits transposed: 032 -> 320)

The customer, trusting the free-text answer, makes a payment decision
based on the wrong balance. No consistency check ever compared the
generated sentence against the original {balance: 8032.10} value
before the response was sent.
```

**Contributing Factors**
- Critical values pass through free-text generation instead of a typed extraction or verbatim pass-through step.
- No schema validation exists between the tool call's structured output and the values the model repeats in prose.
- No chain-of-custody diff runs between successive transformation steps (tool output -> extracted value -> final answer).
- High-precision fields (multi-decimal currency, long IDs, dates in multiple formats) are especially prone to transcription drift during summarization.
- No sampled human audit exists for high-stakes domains (financial totals, medical dosages) to catch corruption patterns automated checks miss.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| High-precision currency pass-through | Tool returns {total: 1234.56, currency: "USD"}, agent asked to summarize the order total in prose | Final response states exactly $1,234.56, matching the tool output byte-for-byte (modulo declared formatting) | Response contains a different numeric value (transposed digits, dropped decimal, wrong magnitude) |
| Multi-value summarization | Tool returns a list of 5 line items with distinct prices; agent asked to summarize the invoice | Every line-item price in the summary matches its source tool-output value exactly | One or more line-item prices in the summary don't match their source values |
| Unit/date reformatting | Tool returns a date as ISO 8601 and a quantity in grams; agent asked to present it in a user-friendly format | Reformatted date/unit is a faithful, declared transform of the original (no value change, only format) | Reformatted value represents a different underlying quantity/date than the source |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_value_mismatch_rate_percent | < 0.5% of eval cases referencing tool output | Run the consistency-check diff against a labeled eval suite of tool-output/response pairs, measure mismatch rate |
| eval_schema_validation_pass_rate_percent | > 99% of extracted values pass schema validation | Run typed extraction over eval tool outputs and measure validation pass rate before generation |
| eval_high_stakes_transcription_accuracy_percent | 100% exact match on high-stakes eval cases (financial/medical values) | Sample high-stakes eval cases, diff generated text against source tool output field-by-field |

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
| value_mismatch_rate_percent | > 1% |
| schema_validation_failure_rate_percent | > 2% |
| high_stakes_audit_error_rate_percent | > 0.2% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Value Mismatch Reached User | Post-send audit or user report confirms a tool-output value was corrupted in the final answer (e.g., wrong price, wrong dosage) | Critical |
| Extraction Schema Validation Failures Rising | schema_validation_failure_rate_percent exceeds 2% over a rolling day | Warning |
| Diff-and-Block Stage Blocking Excessively | blocked_send_due_to_diff_failure_count spikes 3x above baseline | Info |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.

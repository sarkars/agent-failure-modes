# What Are the Most Common Input-Output-Handling Failures in AI Agents?

**Agents receive input from users and upstream systems, and produce output that downstream systems and users consume. Input-output-handling failures occur when input is not validated, output is not sanitized, encodings mismatch, or edge cases in data format (null bytes, special characters, timezones) are not handled, resulting in silent corruption, injection vulnerabilities, or downstream failures that are hard to trace back to input issues.**

## Key Takeaways

1. **Input Validation Bypass Is Silent and Cascading**: Agents that don't validate input accept invalid data (oversized strings, wrong types, malformed dates) that propagates downstream, causing failures in other agents, databases, or external systems. The original bad input is invisible in later failure messages.

2. **Output Hallucination in Structured Formats Is Catastrophic**: When agents generate structured output (JSON, CSV, XML), hallucination (inventing fields or values) produces syntactically valid but semantically wrong output. Downstream systems accept and process the garbage because it's valid format.

3. **Encoding Mismatches Are Silent**: Input or output in different encodings (UTF-8 vs UTF-16, single-byte vs multi-byte) cause character corruption or rejection. Data containing non-ASCII characters is especially vulnerable to encoding bugs.

4. **Edge Cases in Data Format Escape Validation**: Timezone ambiguity, null bytes, quote escaping, locale-specific formatting, and recursion limits are individually rare but collectively common. A comprehensive input/output validation strategy must explicitly handle each category.

## Scope

Input-output-handling failures cluster into five categories:

- **Input Validation Gaps**: Input is oversized, malformed, contains invalid characters, or has wrong schema; agent accepts and processes it anyway. (input-size-not-validated, input-schema-evolution, input-validation-bypass, input-recursion-limit)
- **Format & Encoding Issues**: Input or output uses unexpected encoding (UTF-8 vs UTF-16), locale (en-US vs de-DE), or timezone, causing misinterpretation. (input-encoding-mismatch, input-locale-mismatch, input-timezone-ambiguity, output-encoding-issues)
- **Special Character Handling**: Input contains special characters (null bytes, quotes, backslashes) that agent doesn't escape properly, causing injection or truncation. (input-null-bytes-injection, input-special-character-handling, output-quote-escaping-failure, output-sanitization-bypass)
- **Output Errors**: Output is truncated, hallucinated, inconsistent, or doesn't match promised format; downstream systems consume garbage. (output-hallucination-in-structured-format, output-truncation-silent, output-inconsistency, output-format-not-validated)
- **Default Assumptions**: Agent assumes input has a default value, or doesn't validate output bounds, or makes implicit assumptions about data type conversions. (input-default-value-assumption, output-length-not-enforced, output-precision-loss, output-type-coercion-failure)

## When Input-Output-Handling Matters

1. **Data Pipeline Transformations**: Agents that transform data from one format to another (JSON to CSV, XML to database, user input to query). One agent's output is the next agent's input; corruption propagates through the pipeline.

2. **External API Integration**: Agents calling external APIs that have strict input requirements and return structured output that must be parsed. Encoding mismatches or format violations cause silent API failures.

3. **User-Facing Systems**: Agents that directly consume user input (forms, text, file uploads). User input is maximally unconstrained; validation must be aggressive.

## Cross-Pattern Insight

Input-output-handling is fundamentally about **explicit contracts at system boundaries**. An agent that receives input has no way to know if the input is valid without validation. The previous agent that produced the output has no way to know if downstream agents will accept it without explicit format negotiation. A robust approach requires: (1) input validation at every boundary (validate type, size, encoding, format, required fields); (2) explicit format and encoding negotiation (agree on UTF-8 encoding, timezone-aware date strings, JSON as format); (3) output validation to ensure the agent's output matches the promised format; (4) error handling for validation failures (don't silently truncate or corrupt, explicitly reject invalid input); and (5) regular audits of sample input/output to catch edge cases that validation missed. Without these, garbage input and output propagate through systems silently, and failures manifest far downstream.

## Frequently Asked Questions

**How can an agent validate that input is the right size without rejecting legitimate large inputs?**
Set a maximum input size based on the agent's computational budget, not a fixed number. For example, an agent that can process 100,000 tokens within its time budget should reject input larger than that. Communicate the limit to upstream systems. If legitimate inputs exceed the limit, either increase the limit or split processing into multiple requests.

**Why is output hallucination in structured formats harder to detect than output errors?**
Because syntactically valid output passes basic format checks (valid JSON, valid CSV) but contains inverted or invented fields. A downstream parser accepts it without error. The semantic correctness of the output (does the content match what was requested?) is not verified by format validation. Mitigations: (1) use schemas with required fields and type checking, (2) validate a sample of output against a ground truth, (3) check for suspicious patterns (e.g., all-zero numeric fields, repeated values that shouldn't be repeated).

**What is the difference between timezone ambiguity and locale mismatch?**
Timezone ambiguity occurs when a time string doesn't specify timezone (e.g., "2024-01-01 12:00") and different systems assume different timezones. Locale mismatch occurs when dates/times/numbers use locale-specific formatting (e.g., "01/12/2024" means January 12 in US, December 1 in EU). Both must be handled explicitly: use UTC for all internal timestamps, communicate timezone with date strings ("2024-01-01T12:00Z"), and use locale-independent formats.

**How can an agent avoid silent truncation of output?**
Validate output length before returning it. If the output is required to fit in a certain number of characters or tokens, check length and reject (or truncate explicitly, indicating truncation) rather than silently cutting off. For structured output, validate that all required fields are present. For numeric output, validate precision (decimal places) against specification.

**What should an agent do if input validation fails?**
Fail fast and explicitly. Return a clear error message indicating what validation failed (size, encoding, schema, required field missing) and what the constraint is. Do not silently truncate, convert, or corrupt input. Do not proceed with invalid input hoping it will be handled downstream. Downstream agents will not know to validate what the sending agent accepted.

## Failure Patterns

| Pattern | Description |
|---------|-------------|
| [Input Default Value Assumption](failures/input-default-value-assumption.md) | Agent assumes missing input field has a default value; upstream system didn't provide default, causing silent misinterpretation. |
| [Input Encoding Mismatch](failures/input-encoding-mismatch.md) | Input is in UTF-16 but agent expects UTF-8, or vice versa, causing character corruption. |
| [Input Locale Mismatch](failures/input-locale-mismatch.md) | Input date/number uses locale-specific formatting (en-US vs de-DE); agent misinterprets or rejects it. |
| [Input Null Bytes Injection](failures/input-null-bytes-injection.md) | Input contains null bytes that truncate strings or cause C-string vulnerabilities. |
| [Input Recursion Limit](failures/input-recursion-limit.md) | Nested input structure (nested arrays, objects, or references) exceeds agent's recursion limit, causing stack overflow or timeout. |
| [Input Schema Evolution](failures/input-schema-evolution.md) | Upstream system adds or removes input fields; downstream agent doesn't adapt, causing schema mismatch. |
| [Input Size Not Validated](failures/input-size-not-validated.md) | Agent accepts input that exceeds its computational budget or memory capacity. |
| [Input Special Character Handling](failures/input-special-character-handling.md) | Input contains quotes, backslashes, or other special characters that aren't properly escaped. |
| [Input Timezone Ambiguity](failures/input-timezone-ambiguity.md) | Input timestamp doesn't specify timezone; agent and upstream system assume different timezones. |
| [Input Validation Bypass](failures/input-validation-bypass.md) | Input validation is disabled, bypassed, or incomplete; invalid input is processed. |
| [Output Encoding Issues](failures/output-encoding-issues.md) | Output is encoded in a different encoding than downstream system expects. |
| [Output Format Not Validated](failures/output-format-not-validated.md) | Output is not checked to match promised format (JSON schema, CSV headers, XML structure). |
| [Output Hallucination in Structured Format](failures/output-hallucination-in-structured-format.md) | Agent generates plausible-looking but false fields in structured output (JSON, CSV). |
| [Output Inconsistency](failures/output-inconsistency.md) | Multiple invocations of the same agent with the same input produce different outputs. |
| [Output Injection Vulnerability](failures/output-injection-vulnerability.md) | Output contains unsanitized user input that's then interpreted as code or commands downstream. |
| [Output Length Not Enforced](failures/output-length-not-enforced.md) | Output is longer than downstream system can accept (character limit, token limit, file size). |
| [Output Ordering Nondeterminism](failures/output-ordering-nondeterminism.md) | Output ordering is inconsistent across runs (e.g., JSON object field order, list order). |
| [Output Precision Loss](failures/output-precision-loss.md) | Output converts high-precision numeric values to lower precision (float32 to float16), losing information. |
| [Output Quote Escaping Failure](failures/output-quote-escaping-failure.md) | Output contains quotes or backslashes that aren't properly escaped for CSV/JSON/SQL. |
| [Output Sanitization Bypass](failures/output-sanitization-bypass.md) | Output sanitization is incomplete; dangerous content (HTML, SQL, shell commands) escapes and is executed. |
| [Output Truncation Silent](failures/output-truncation-silent.md) | Output is truncated to fit a size limit without indicating truncation occurred. |
| [Output Type Coercion Failure](failures/output-type-coercion-failure.md) | Output is silently converted to a different type (string to number, boolean to int) losing information or causing type errors downstream. |

**Total: 22 patterns**

## Related Goals

- [Agent-Handoffs-Delegation](../agent-handoffs-delegation/README.md) — handoff payloads are input/output between agents; malformed handoffs are input-output-handling failures
- [Dependency-Management](../dependency-management/README.md) — API contract violations (wrong input format, unexpected output format) are input-output-handling failures
- [Data-Pipeline-Integration](../data-pipeline-integration/README.md) — schema evolution and encoding mismatches are pipeline integration failures that stem from input-output handling
- [Observability-Monitoring](../observability-monitoring/README.md) — input/output handling failures often go undetected; visibility into data flow is critical
- [Security](../security) — input injection, output sanitization, and type coercion are security concerns alongside functional correctness

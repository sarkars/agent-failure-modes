# Output Type Coercion Failure

## Issue
An agent produces output whose values are of one type — a string, a loosely-formatted number, a mixed-case boolean word — and the downstream system consuming that output performs an implicit type coercion while deserializing or ingesting it, silently converting the value into something semantically different rather than rejecting it. Because the coercion happens inside the consumer's parsing/deserialization layer rather than inside the agent, the agent has no visibility into the mismatch and no chance to correct it; the corrupted value simply propagates into the receiving system as if it were correct.

**Frequency**: Common

**Symptoms**
- A numeric-looking string field (e.g., an ID like `"007"` or `"00042"`) loses its leading zeros or padding after being coerced to an integer downstream
- A field the agent emits as an empty string, `"null"` (as text), or `"N/A"` gets coerced to `false`, `0`, or `NULL` by a downstream loose-typing consumer, changing its meaning from "not applicable" to "explicitly false/zero"
- Boolean-like strings such as `"yes"`, `"no"`, `"Y"`, `"true"` are coerced inconsistently depending on the consumer's truthiness rules (e.g., any non-empty string, including `"no"`, evaluates as truthy)
- Downstream records show values whose type matches the destination schema but whose value doesn't match what the agent actually generated, with no error anywhere in the pipeline
- The same agent output produces different downstream values depending on which consumer (database client, spreadsheet import, another service's parser) ingests it, because each applies its own coercion rules

## Root Cause
Language runtimes and data-ingestion layers commonly perform automatic type coercion when a value doesn't match the expected type exactly — JavaScript's loose equality and implicit string-to-number conversion, SQL drivers casting strings into numeric or boolean columns, spreadsheet importers auto-detecting and reformatting cell types — and this coercion is designed for human-authored or already-validated input, not for values coming from a generative model whose output format is only a soft convention. The agent's output schema (if one exists at all) typically documents the intended type but nothing enforces that the actual generated string is unambiguous under every consumer's coercion rules; a value that's perfectly clear to a human reader (an ID with leading zeros, an explicit "N/A") can be silently reinterpreted the moment it crosses into a system with its own implicit type rules. Because the coercion produces a validly-typed value in the destination schema, no exception is raised and no validation step downstream of the agent is positioned to catch that the value's meaning changed in transit.

## Example
```
A data-entry agent extracts structured fields from scanned intake
forms and emits them as JSON: {"employee_id": "00417", "is_veteran":
"N/A", "years_service": "3.0"}.

A downstream HR system ingests this JSON directly into database
columns: employee_id (INTEGER), is_veteran (BOOLEAN), years_service
(INTEGER). The database driver coerces "00417" to the integer 417,
silently dropping the leading zeros that were significant to the
badge-numbering scheme. It coerces the string "N/A" to boolean true
(any non-empty string is truthy in the driver's cast logic),
incorrectly recording every unresolved veteran-status field as
"is a veteran." It coerces "3.0" to integer 3, dropping the fractional
part that mattered for pro-rated benefits calculations.

None of these coercions raise an error - each produces a validly
typed value for its column. The mis-recorded veteran status is only
discovered months later during a benefits-eligibility audit that
manually cross-checks a sample of records against source documents.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of structured-output ingestion pipelines rely on the destination system's implicit type coercion rather than validating agent output against an explicit schema before ingestion | Estimated from review of typical agent-to-database integration pipelines |
| Loose-typing consumers (dynamically typed languages, permissive database drivers, spreadsheet importers) show measurably higher rates of silent value corruption on agent-generated fields than statically validated pipelines | Typical range observed comparing schema-validated vs. non-validated ingestion paths |
| Sentinel/placeholder values (e.g., "N/A", "TBD", empty string) are disproportionately represented among coercion-corrupted fields relative to their share of all generated values | Typical finding in production data-quality audits of agent-populated records |

## Mitigations
1. **Explicit output schema with strict typing**: Define the agent's output schema with concrete types (integer, boolean, string) and have the agent emit values in the destination's native type rather than as loosely-formatted strings that require downstream interpretation.
2. **Validate before ingest, not during**: Run an explicit schema-validation step immediately after generation, before the value reaches any consumer's implicit coercion layer, so type mismatches are caught and rejected at the source rather than silently reinterpreted downstream.
3. **Reserve unambiguous sentinels**: Define and enforce an explicit, typed representation for "not applicable"/"unknown" (a dedicated nullable field or enum value) rather than relying on free-text placeholders like "N/A" that different consumers coerce differently.
4. **Preserve format-significant fields as strings end-to-end**: For values where formatting carries meaning (zero-padded IDs, fixed-decimal amounts), declare the destination column/field as string/text explicitly rather than letting a numeric-looking value fall through to automatic numeric casting.
5. **Coercion-diff testing**: As part of integration testing, run representative agent outputs through each actual downstream consumer and diff the ingested value against the generated value, to catch consumer-specific coercion behavior before it reaches production.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| schema_validation_reject_rate | Share of agent outputs rejected by explicit schema validation prior to ingestion | Investigate if it rises sharply, but treat a rate of 0% with no validation step configured as a bigger risk signal |
| sentinel_value_coercion_rate | Rate at which known placeholder values (N/A, empty string, TBD) appear in agent output for fields later ingested by a loosely-typed consumer | Alert if > 0.5% of records contain unvalidated sentinel values in typed fields |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Ingested value diverges from generated value | Automated diff between agent-generated field and post-ingestion stored value detects a mismatch beyond expected formatting normalization | High | Halt ingestion for affected field, add explicit typing/validation, backfill affected records |
| Unvalidated ingestion path detected | A consumer ingests agent output directly without passing through the schema-validation step | Medium | Route the consumer through the validation layer before next deploy |

## Related Patterns
- [Silent Type Coercion](../../tool-reliability/failures/silent-type-coercion.md) - the input-side counterpart, where a tool silently coerces mistyped arguments the agent passes in, rather than a downstream consumer coercing the agent's output
- [Output Precision Loss](./output-precision-loss.md) - a related but narrower failure specifically about numeric precision being lost during serialization, as opposed to broader type reinterpretation
- [Input Default Value Assumption](./input-default-value-assumption.md) - a related input-side pattern where missing/ambiguous values are silently defaulted rather than coerced
- [Output Format Not Validated](./output-format-not-validated.md) - broader unvalidated-output pattern that this is one specific, type-focused instance of

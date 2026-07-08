# Wrong Argument Format

## Issue: Agent sends invalid JSON, enum, type, or schema.

**Frequency**: Occasional

**Symptoms**
- Tool returns schema validation error.
- [Add more specific symptoms]

**Root Cause**
Agent sends invalid JSON, enum, type, or schema.

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
1. **Client-Side Schema Validation Before Send**: Every tool call is validated against its JSON Schema (types, enums, required shape) on the client/orchestrator side before it is transmitted, catching malformed arguments locally instead of burning an API round-trip on a 400 error.
2. **Constrained Decoding for Structured Arguments**: Where the underlying model supports it, tool-call argument generation uses constrained/grammar-guided decoding (JSON mode, enum-constrained sampling) so the model is structurally prevented from emitting invalid types or out-of-enum values in the first place.
3. **Schema-Embedded Few-Shot Examples**: Tool descriptions include concrete valid-argument examples (correct enum casing, date format, nesting) directly adjacent to the schema, reducing the chance the model infers a plausible-but-wrong format.

### Detection & Response
1. **Schema Validation Error Classification**: Tool-call failures are parsed to distinguish schema/validation errors from other failure types (auth, rate-limit, missing param) using structured error codes, enabling this specific failure mode to be tracked and trended independently.
2. **Repair-Loop Success Rate Tracking**: When a schema error triggers an automatic repair retry (re-prompting the agent with the specific validation error), the system tracks how often the repair succeeds on the first retry versus requires multiple attempts, surfacing tools/schemas that are chronically hard for the model to satisfy.
3. **Enum/Type Drift Monitoring**: The tool's live schema (enums, types) is compared against what's embedded in the agent's tool-description cache; drift after an API version bump is a common silent cause of a sudden spike in format errors and is flagged automatically.

### Architecture Patterns
1. **Validate-Then-Send Gateway**: A shared gateway validates every outgoing tool-call payload against the tool's current JSON Schema and rejects it with a structured, model-readable error before the call reaches the external API, keeping validation logic centralized rather than duplicated per tool.
2. **Structured Repair Loop**: On a validation failure, the orchestrator feeds the specific schema violation (field, expected type/enum, actual value) back to the agent as a targeted correction prompt, capped at N attempts, rather than replaying the full original error blob.
3. **Typed SDK/Codegen Layer**: Tool argument construction goes through a generated typed client (from the tool's OpenAPI/JSON Schema) rather than free-form JSON assembly, so many format errors are caught by the type system before the network call is even made.

### Metrics
1. **schema_validation_error_rate_percent**: Target: < 2% of tool calls; Alert threshold: > 5%
2. **repair_loop_first_retry_success_rate_percent**: Target: > 80%; Alert threshold: < 50%
3. **schema_drift_incidents_per_month**: Target: 0 undetected; Alert threshold: > 0
4. **calls_exhausting_repair_budget_percent**: Target: < 1%; Alert threshold: > 3%

### Alerts
1. **Repair Loop Exhausted** (P2 - Warning): Condition - a tool call fails schema validation N times in a row without successful repair. Action: Surface a clear failure to the user, log full argument history for prompt/schema debugging.
2. **Schema Drift Detected** (P2 - Warning): Condition - the live API schema differs from the cached tool-description schema. Action: Auto-refresh cached schema, notify tool owner, re-run validation regression tests.
3. **Validation Error Rate Spike** (P3 - Info): Condition - schema_validation_error_rate_percent exceeds threshold for a specific tool over 1 hour. Action: Review recent prompt or tool-description changes, check for upstream schema changes.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.

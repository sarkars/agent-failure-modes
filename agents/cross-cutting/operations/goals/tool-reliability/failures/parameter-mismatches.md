# Parameter Type Mismatches

> **⚠️ DEPRECATED — Largely Mitigated**: Strict JSON-schema / structured-output
> tool-calling modes (now standard in major model tool-use APIs) constrain the
> model to emit schema-conformant types at generation time, closing most of
> the failure path described below. Still relevant for legacy integrations
> without strict-mode enforcement. For tool-side leniency (the tool itself
> silently coercing bad input after a valid call), see `silent-type-coercion.md`,
> which is not mitigated by this and remains current.

## Issue: Agent Passes Wrong Parameter Types to Tools

**Frequency**: Very Common

**Symptoms**
- Tools receive string instead of integer (or vice versa)
- Arrays passed as single values
- Dates in wrong format
- Nested objects flattened incorrectly

**Root Cause**
LLMs generate text and must format tool parameters correctly. Type mismatches occur when:
- Schema not clearly communicated to model
- Model infers types incorrectly
- Implicit type coercion fails
- Complex nested types confuse the model

**Example**
```
Tool schema: { "user_id": integer, "active": boolean }

Agent call: { "user_id": "12345", "active": "true" }

Result: Tool fails or silently processes wrong types
```

**Key Statistic**
37% of tool calls have silent parameter mismatches according to developer analysis.

---

## Test Scenario & Reproduction

### Scenario Setup
- A legacy tool integration without strict/structured tool-calling mode enabled
- No runtime type-validation or coercion-with-logging layer at the tool boundary
- Schema communicates types only loosely (e.g., via description, not enforced JSON Schema types)

### Trigger Mechanism
1. Configure the agent's model/SDK to call the tool in free-form (non-strict) mode
2. Prompt the agent in a way likely to produce a string-typed value for an integer field (e.g., referencing an ID conversationally)
3. Inspect the actual tool call payload for type mismatches

**Example Reproduction Steps:**
```
1. Define a tool schema: { "user_id": integer, "active": boolean } without strict mode enabled
2. Ask the agent to "check if user 12345 is active"
3. Capture the raw tool call arguments
4. Check whether user_id arrived as "12345" (string) instead of 12345 (integer), or active as "true" (string) instead of true (boolean)
5. Measure: type-mismatch rate across repeated trials against the 37% historical baseline
```

### Expected Failure State
- Tool call arrives with string-typed values for integer/boolean fields
- No validation layer rejects or logs the coercion before the call reaches the underlying system
- Tool either fails outright or silently processes the wrong type, producing an incorrect result

---

## Mitigation Strategies

Note: as flagged in the deprecation notice above, strict JSON-schema tool-calling modes now close most of this failure path at generation time by constraining the model to emit schema-conformant types. The strategies below are scoped to the residual surface: legacy integrations without strict-mode enforcement, and defense-in-depth for when strict mode is unavailable or misconfigured.

### Prevention
1. **Enable strict/structured tool-calling mode wherever the model API supports it**: This is the primary fix — it prevents the `user_id: "12345"` / `active: "true"` type-mismatch shown in the example from being generated at all, rather than catching it after the fact. Trade-off: some legacy models or self-hosted setups don't support strict mode, leaving those integrations exposed to the original failure path.
2. **For non-strict-mode legacy integrations, add a runtime type-coercion-with-logging layer**: Safely convert unambiguous mismatches (string `"12345"` to int `12345`) while logging every coercion event, since these integrations can't rely on generation-time constraints. Trade-off: coercion can mask a genuinely malformed call as a "successful" one, hiding an underlying prompt or schema problem instead of surfacing it.
3. **Runtime type validation as a fallback safety net even with strict mode enabled**: Strict mode reduces but doesn't guarantee zero mismatches (proxies, older SDK versions, or manual API calls can bypass it), so keep a validation layer that fails fast with a clear error rather than assuming strict mode is universally in effect. Trade-off: redundant validation adds a small latency cost to every call even when strict mode is already working correctly.

### Detection & Response
1. **Strict-mode coverage audit**: Track what fraction of tool calls in production actually go through strict/structured-output enforcement vs. legacy free-form generation; any gap is exactly where this failure mode still lives.
2. **Type-mismatch rate on the legacy path**: For integrations not yet migrated to strict mode, monitor the type-mismatch rate directly — the historical baseline cited here is 37% of tool calls, so track whether the legacy subset trends toward or away from that figure.
3. **Coercion event logging**: Every time the fallback coercion layer silently converts a type, log input type, output type, and tool name — a concentration of coercions on one tool signals its schema description needs strict-mode migration or clearer type examples.

### Architecture Patterns
1. **Structured-output / strict JSON schema enforcement**: Use the model provider's native strict tool-calling mode (function calling with schema enforcement) as the default for all new integrations; deployment consideration — requires auditing which model/SDK versions in the fleet actually support it, since older pinned versions may silently fall back to lenient mode.
2. **Schema-first migration path for legacy tools**: Prioritize migrating tools still on free-form generation to strict mode by type-mismatch frequency (highest-offending tools first), rather than a blanket rewrite; deployment consideration — migration can break callers that depended on the old lenient coercion behavior.
3. **Type-coercion layer as a bridge, not a destination**: Where strict mode genuinely can't be enabled (e.g., a frozen legacy model), keep a well-tested coercion layer, but track it as technical debt with a migration target rather than a permanent architecture. deployment consideration — teams often treat the bridge as done and never complete the migration to strict mode.

### Metrics
1. **strict_mode_coverage_rate**: Target > 95% of tool calls issued under strict/structured-output enforcement; Alert if < 80% for any integration.
2. **legacy_path_type_mismatch_rate**: Target < 5% (down from the 37% historical baseline) for tools still on the legacy path; Alert if it exceeds 20%.
3. **silent_coercion_rate**: Target < 1% of legacy-path calls requiring silent type coercion; Alert if > 5% over a week (signals a specific tool needs strict-mode migration).

### Alerts
1. **Strict Mode Coverage Regression** (P1): Condition - strict_mode_coverage_rate drops below 80% for an integration that was previously migrated. Action: check for an SDK downgrade or model-endpoint change that disabled strict mode, restore configuration immediately.
2. **Legacy Type Mismatch Spike** (P2): Condition - legacy_path_type_mismatch_rate exceeds 20% for a specific tool. Action: prioritize that tool for strict-mode migration, add explicit type examples to its schema in the interim.
3. **Coercion Concentration on Single Tool** (P3): Condition - one tool accounts for > 50% of all silent_coercion events. Action: review that tool's parameter schema and description for ambiguous type expectations, migrate to strict mode.

## References

- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Analysis finding 37% of tool calls have parameter mismatches
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Best practices for designing agent-friendly tool schemas
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research paper on multi-agent system failure modes

# Missing Required Parameter

## Issue: Agent omits ID, date range, filter, auth scope, or tenant.

**Frequency**: Occasional

**Symptoms**
- Tool error mentions missing field.
- Agent retries the same call with the same omission, or fabricates a placeholder value instead of asking.

**Root Cause**
Agent omits ID, date range, filter, auth scope, or tenant.

**Example**
```
A user mentions their tenant/workspace name in turn 2 of a long support
conversation. By turn 15, that detail has scrolled out of the model's
active context. The agent calls list_tickets() without a tenant_id, and
the tool silently defaults to the caller's default workspace, returning
zero relevant results instead of erroring or asking the user to confirm.
```

**Contributing Factors**
- Required fields live in earlier conversation turns that have been summarized or truncated out of context.
- Tool description doesn't mark fields as required distinctly from optional ones, so the model treats them as equally droppable.
- No preflight schema validation before the call reaches the live API, so omissions surface only as generic downstream errors.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Context-drop omission | Push tenant_id/date range into an early turn, then extend conversation past the context window before the agent issues the call | Agent re-derives or explicitly asks for the missing field rather than omitting it or guessing | Call is sent without a required field, or with a fabricated/default value |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| missing_parameter_error_rate | < 1% of tool calls | Classify tool-call failures by structured error code and track the share attributed to missing required fields |

---

## Mitigation Strategies

### Prevention
1. **Preflight Schema Diff Check**: Before invocation, the orchestrator diffs the constructed call payload against the tool's required-field schema; any required field that is absent or null blocks the call and forces the agent to either supply it or explicitly ask the user, rather than letting the API reject it downstream.
2. **Context-to-Parameter Binding Rules**: Common required fields (tenant_id, auth scope, date range) are auto-populated from session/request context rather than left for the model to infer or type out, removing the chance the agent silently drops them when composing the call.
3. **Clarification-Before-Call Policy**: When a required parameter has no derivable value from context or conversation, the agent is instructed (via system prompt and tool description) to ask the user rather than guess or omit; the tool-calling policy refuses to synthesize a placeholder value for missing IDs/scopes.

### Detection & Response
1. **Missing-Field Error Classification**: Tool-call failures are parsed and classified specifically as "missing required parameter" (versus auth/rate-limit/other errors) using the API's structured error code, so this failure mode is tracked distinctly rather than lumped into generic tool errors.
2. **Repeated-Omission Pattern Alert**: If the same required field is missing across multiple calls to the same tool within a session, that signals a systemic prompt/schema gap rather than a one-off, and triggers a flag for prompt/tool-schema review rather than just a retry.
3. **Scope/Tenant Omission Cross-Check**: For multi-tenant or scoped systems, any write or read call missing tenant/auth scope is treated as a security-relevant event (not just a functional bug) and logged to a separate security-review queue in addition to the standard error log.

### Architecture Patterns
1. **Required-Field Gateway Validation**: A validation layer in front of each tool enforces the tool's JSON-schema `required` array before the call reaches the underlying API, returning a structured "missing_parameter: <field>" error back to the agent loop instead of a generic 400, enabling targeted self-correction.
2. **Context Injection Service**: A middleware service auto-injects session-scoped defaults (current tenant, authenticated user's scope, default date range) into every outgoing tool call before the schema check runs, so the agent only needs to supply parameters it genuinely controls.
3. **Parameter Completion Retry Loop**: On a missing-parameter error, the orchestrator re-prompts the agent with the specific missing field name and its schema description (not the raw API error), capped at N retries before escalating to the user for clarification.

### Metrics
1. **missing_parameter_error_rate_percent**: Target: < 1% of tool calls; Alert threshold: > 3%
2. **auto_injected_context_field_coverage_percent**: Target: 100% of tenant/scope/date fields auto-filled; Alert threshold: < 95%
3. **clarification_prompts_for_missing_params_per_session**: Target: < 0.2 average; Alert threshold: > 1 average
4. **repeated_field_omission_incidents_per_week**: Target: 0; Alert threshold: >= 3 (same field, same tool)

### Alerts
1. **Scope/Tenant Parameter Omitted** (P1 - Critical): Condition - a call executed or was attempted without a required tenant_id or auth scope. Action: Block call, alert security/on-call, audit whether any data crossed tenant boundaries.
2. **Missing-Parameter Error Spike** (P2 - Warning): Condition - missing_parameter_error_rate_percent exceeds threshold for a given tool over 1 hour. Action: Page tool owner, check recent schema or prompt changes.
3. **Repeated Field Omission** (P3 - Info): Condition - same required field missing 3+ times in a week for one tool. Action: File a prompt/schema improvement ticket, add an explicit example to the tool description.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| missing_parameter_error_rate_percent | > 3% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Scope/Tenant Parameter Omitted | Call executed or attempted without a required tenant_id or auth scope | Critical |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.

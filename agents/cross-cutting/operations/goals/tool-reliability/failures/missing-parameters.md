# Missing Required Parameters

## Issue: Agent Omits Required Tool Parameters

**Frequency**: Common

**Symptoms**
- Tool calls fail with "missing required field" errors
- Agent assumes defaults that don't exist
- Partial tool calls that can't execute
- Agent "forgets" parameters mentioned in conversation

**Root Cause**
- Tool schema not clearly marking required vs. optional
- Long context causing agent to lose track of requirements
- Ambiguous parameter names
- Agent conflating similar tools with different requirements

**Example**
```
Tool: send_email(to: required, subject: required, body: required, cc: optional)

Agent call: send_email(to: "user@example.com", body: "Hello!")

Missing: subject (required)

Result: Email not sent, user thinks message was delivered
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Tool schema (`send_email`) marks required fields only in prose/description, not in a structural `required` array
- No reject-before-execute validation gate at the tool boundary
- Conversation context is long enough that an earlier-mentioned parameter (e.g., subject) may be lost

### Trigger Mechanism
1. Ask the agent to send an email over a multi-turn conversation where the subject is mentioned early and the send request comes many turns later
2. Observe whether the agent's assembled tool call includes all required fields
3. Check whether a missing field causes a silent failure or a loud, user-visible error

**Example Reproduction Steps:**
```
1. Tell the agent early in conversation: "The subject should be 'Meeting Reminder'"
2. After several unrelated turns, ask: "Send that email to user@example.com with body 'Hello!'"
3. Inspect the actual send_email(...) call the agent issues for a subject field
4. If subject is missing, check whether the agent's response to the user claims success or reports the failure
5. Measure: % of long-conversation send requests that drop a required field
```

### Expected Failure State
- The tool call omits the `subject` field despite it being stated earlier in the conversation
- The tool either fails silently or the agent's user-facing message claims the email was sent
- No validation gate blocked the malformed call before it reached the underlying system

---

## Mitigation Strategies

### Prevention
1. **Reject-before-execute validation at the tool boundary**: Check every required field is present before `send_email` (or any tool) touches the underlying system, so a call missing `subject` fails loudly instead of silently sending a subject-less message or, worse, not sending at all while the user believes it did. Trade-off: strict rejection means genuinely edge-case-valid calls (e.g., an intentionally empty subject) also get blocked unless explicitly modeled as optional-with-empty-allowed.
2. **Disambiguate required vs. optional in the schema itself, not just prose**: Use JSON Schema's `required` array (or Pydantic's non-`Optional` fields) rather than describing requiredness only in a docstring, since the root cause calls out "tool schema not clearly marking required vs. optional" as a primary driver — the model reads the schema structure more reliably than free text buried in a description. Trade-off: retrofitting strict schemas onto existing lenient tools can break callers that previously relied on omitted fields defaulting silently.
3. **Re-surface required parameters mentioned earlier in long conversations**: When a tool call is being assembled after many turns, inject a reminder of that tool's required fields into context immediately before the call, addressing the specific root cause that "long context causing agent to lose track of requirements" — the agent "forgets" a subject it was told minutes ago. Trade-off: adds a context-injection step to every tool call, increasing prompt size and latency slightly.

### Detection & Response
1. **Missing-parameter error rate by tool and field**: Log which specific required field (e.g., `subject` on `send_email`) triggers "missing required field" most often; a concentration on one field across many calls points to an ambiguous or easily-overlooked parameter name rather than random agent error.
2. **Silent-success-without-required-field audits**: Since the example shows the failure mode is the email not being sent while the user believes it was delivered, specifically audit for cases where a tool call fails validation but the agent's subsequent message to the user implies success anyway.
3. **Parameter completeness rate trend**: Track the percentage of tool calls that pass required-field validation on the first attempt per tool; a downward trend after a schema or prompt change signals the change made requirements less clear to the model.

### Architecture Patterns
1. **JSON Schema validation gate**: Validate every tool call against its JSON Schema (with `required` explicitly enumerated) before dispatch, returning a structured `{error: "missing_required_field", field: "subject"}` rather than letting the call reach the underlying system partially formed; deployment consideration — needs to run synchronously in the call path, adding a small latency cost per call.
2. **Parameter confirmation step for high-stakes tools**: For tools where a missing field causes a silent user-facing failure (like `send_email` appearing to succeed when it didn't), require the agent to echo back the assembled parameter set before execution; deployment consideration — adds a round-trip that's wasteful for low-stakes, frequently-called tools, so apply selectively.
3. **Sensible-default fallback with explicit disclosure**: Where safe (e.g., a missing `cc` truly optional field), auto-fill defaults; where not safe (a missing `subject`), never silently default — instead fail with a specific, actionable error naming the field. deployment consideration — the line between "safe to default" and "must fail" needs per-field review, not a blanket policy.

### Metrics
1. **missing_required_field_rate** (per tool): Target < 2% of calls; Alert if > 8% over a 1-hour window for any single tool.
2. **field_omission_concentration**: Target: no single required field accounts for > 40% of a tool's missing-field errors; Alert if one field exceeds 60% (signals that field's schema/description needs rework).
3. **post_failure_false_success_rate**: Target: 0% of agent responses claiming success after a validation failure; Alert on any occurrence — this is the exact silent-failure scenario in the example and should page immediately.
4. **first_attempt_validation_pass_rate**: Target > 95%; Alert if it drops below 85% following any schema or prompt change.

### Alerts
1. **False Success After Missing-Parameter Failure** (P1): Condition - a tool call fails required-field validation but the agent's user-facing response implies the action succeeded (e.g., "I've sent your message"). Action: page immediately, this is a user-trust-breaking bug; patch the agent's error-handling prompt so it always surfaces validation failures to the user.
2. **Missing-Field Rate Spike for a Tool** (P2): Condition - missing_required_field_rate exceeds 8% for a tool over 1 hour. Action: review recent schema/prompt changes to that tool, check if the field name or description is ambiguous, consider adding a Field(description=...) with an example.
3. **Validation Pass Rate Regression** (P3): Condition - first_attempt_validation_pass_rate drops more than 10 points after a deployment. Action: diff the schema/prompt change, roll back if the regression is confirmed tied to it.

## References

- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Common tool call errors including missing parameters
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - MCP server configuration mistakes that cause parameter issues

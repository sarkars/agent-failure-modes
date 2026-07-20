# Tool Mutation State Leak

## Issue
A tool call mutates some shared state as a side effect — a global filter, a session variable, an environment setting, a cursor position, an authentication context — that isn't part of its declared return value, and a later, logically unrelated tool call is affected by that leftover mutation without either the agent or the tool's own interface making the dependency visible. The agent has no way to know that calling tool X changed the behavior of tool Y, because the mutation isn't represented anywhere in the tool-call contract.

**Frequency**: Occasional

**Symptoms**
- A tool call returns different results for identical arguments depending on what other tools were called earlier in the session
- Debugging a failing tool call requires tracing back through unrelated prior calls to find the one that changed shared state
- The same task succeeds when run as a fresh session but fails when run as a later step in a longer, multi-task session
- A tool's documented parameters don't explain an observed behavior difference; the explanation turns out to be global/shared state set by a different tool
- Resetting or restarting the agent's session (clearing implicit shared state) makes an otherwise-reproducible bug disappear

## Root Cause
Tool integrations are often built against a shared client, SDK instance, or backend session that carries mutable state across calls for legitimate performance or convenience reasons — connection reuse, cached auth tokens, a "current working directory" or "active filter" concept — but that shared state isn't part of the tool's declared input/output contract that the agent's planner reasons about. The agent treats each tool call as a pure function of its explicit arguments, because that's the abstraction the tool definitions present, while the actual implementation has memory. When one tool's call sets a piece of that hidden shared state, any later tool sharing the same underlying client silently inherits it, producing behavior the agent's plan never accounted for because the plan was built assuming call independence.

## Example
```
An agent has two tools backed by the same underlying database client
instance: set_query_filter(region="APAC") and get_customer_count().
set_query_filter is meant to scope a specific reporting call; internally
it sets a filter attribute on the shared client rather than passing it
as a request parameter.

Step 4 of a task: agent calls set_query_filter(region="APAC") to
answer "how many APAC customers do we have," gets the correct count,
and reports it to the user.

Step 9 of the same session, an unrelated task: agent calls
get_customer_count() with no filter argument, intending to answer
"how many total customers do we have." Because the underlying client
still has region="APAC" set from step 4 and get_customer_count()
reuses the same client without resetting it, the call silently returns
the APAC-only count instead of the global total.

The agent reports the APAC count as the global total customer count.
Nothing in the tool call or its response indicates a filter was
applied; the discrepancy is only caught a week later when someone
cross-checks the reported number against the billing system's total.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of "same call, different result" bug reports in long-running agent sessions trace to hidden shared mutable state between tools | Typical range observed in production agent telemetry |
| Tools built on shared SDK/client instances are disproportionately affected, compared to tools built as stateless HTTP wrappers | Estimated from architecture review across affected incidents |
| Explicit state-reset-between-calls policies reduce leak-related incidents by an estimated 70-90% | Reported range across teams that added session isolation |

## Mitigations
1. **Stateless tool contracts**: Design tools to take all relevant context as explicit parameters and avoid mutating shared client/session state as a side effect; where a stateful underlying SDK is unavoidable, wrap it so each tool call resets to a known-clean state first.
2. **Per-call isolated execution context**: Use a fresh client/session instance per tool call (or per logical sub-task) rather than one long-lived shared instance, trading some connection-reuse efficiency for correctness.
3. **Explicit state surfacing in tool responses**: If a tool does set persistent context (like a filter or working directory), make that state visible in its return value and require an explicit "current context" parameter on later calls, so the dependency is part of the visible contract rather than hidden.
4. **State audit between tool calls**: Add a lightweight check that inspects known-mutable shared state before and after each tool call and flags unexpected residual state left over for the next call.
5. **Session-scoped reset points**: Reset all known shared mutable state at clear task boundaries (start of a new sub-task, after a task is marked complete) rather than relying on it to be naturally overwritten by the next call's parameters.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| identical_call_divergent_result_rate | Rate at which the same tool call with identical arguments returns different results within a session | Alert if > 0.5% |
| shared_state_residue_count | Count of detected non-default shared state values present at the start of a new tool call that weren't explicitly set by that call | Alert if > 0 |
| session_length_error_correlation | Correlation between session length (number of prior tool calls) and error/anomaly rate | Track as leading indicator |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Divergent result for identical call | The same tool call and arguments produce a materially different result later in the same session | High | Page on-call, audit for shared mutable state between the two calls, add isolation or explicit context parameters |
| Residual state detected pre-call | State audit finds non-default shared state present before a tool call that didn't set it | Medium | Investigate the prior call that left the residue, add a reset point |

## Related Patterns
- [Tool State Dependency Violation](./tool-state-dependency-violation.md) - the inverse failure, where a call depends on state that was never actually set, rather than being affected by state it didn't expect
- [Tool Invocation Ordering Dependency](./tool-invocation-ordering-dependency.md) - ordering issues and mutation leaks often compound, since the leaked state's effect depends on call order
- [Tool Idempotency Assumption Failure](./tool-idempotency-assumption-failure.md) - both involve incorrect assumptions about a tool call's side effects beyond its declared return value

# Tool State Dependency Violation

## Issue
A tool call is written or planned assuming a prior call already established some state it depends on — an authenticated session, a created resource, an uploaded file, a set configuration — but that prior call was never actually made, failed silently, or was skipped by the agent's plan. The dependent call proceeds anyway, either erroring against missing state or, more dangerously, succeeding against a default/fallback state that isn't the one the agent intended.

**Frequency**: Common

**Symptoms**
- A tool call fails with an error referencing state (a session, a resource ID, a file) that the agent's plan assumed already existed
- The agent's plan includes a step that logically requires a setup action, but the trace shows the setup action's tool call was never actually invoked
- A tool succeeds unexpectedly by falling back to a default value instead of erroring, and the agent proceeds as though the intended state was used
- Errors are more frequent in plans generated for edge-case or less common task variants, where the agent is more likely to omit an implicit setup step
- Re-running the same task with an explicit reminder to "first do X" in the prompt fixes the failure, indicating the dependency was never structurally enforced

## Root Cause
An agent's plan is a sequence of tool calls it decides to make, and if the agent's reasoning omits a step it implicitly assumed was unnecessary (because a previous session had that state, because the tool's description didn't make the requirement obvious, or because the planner simply forgot a step while composing a long plan), nothing forces the omission to surface before the dependent call runs. This is the mirror image of an ordering-dependency violation: instead of calling both tools in the wrong order, the agent may not call the prerequisite tool at all, and if the dependent tool degrades gracefully (uses a stale cached session, defaults an unset resource ID to a sentinel value) rather than failing loudly, the missing dependency becomes invisible rather than a hard blocker.

## Example
```
A file-processing agent's task: "convert the uploaded spreadsheet to
PDF and email it to the customer." The correct plan requires three
calls: upload_file(local_path) -> returns file_id, convert_to_pdf
(file_id) -> returns pdf_id, send_email(attachment_id=pdf_id).

The agent, reasoning from a shortened mental model of the task
("convert and email the spreadsheet"), skips the explicit upload_file
call - it had seen a similar task earlier in the session where a file
was already uploaded, and its plan for this new task assumes a file
is already present in the working context.

It calls convert_to_pdf() with no file_id argument. The tool's
implementation, rather than raising a required-argument error, defaults
to the most recently processed file_id in the session's working
storage - which is a file from the earlier task, the one that made the
agent assume this pattern in the first place.

The tool converts the wrong file to PDF and the agent emails it to the
current customer as their requested attachment. The customer receives
someone else's spreadsheet data as a PDF, a data-exposure incident that
prompts a security review of the file-handling tool's default-fallback
behavior.
```

## Statistics
| Finding | Context |
|---------|---------|
| 10-20% of multi-step tool-plan failures involve a prerequisite call being omitted from the plan entirely, rather than called in the wrong order | Typical range observed in production agent telemetry |
| Tools with silent default/fallback behavior for missing required state are estimated to convert a large share of these omissions into silent wrong-execution rather than a loud, catchable error | Estimated from architecture review of affected tool implementations |
| Requiring explicit required-argument validation (no silent defaulting) reduces missing-dependency incidents that reach production with wrong output by an estimated 70-90% | Reported range across teams that removed silent-fallback behavior from dependency-sensitive tools |

## Mitigations
1. **No silent defaults for required state**: Tools that depend on state established by a prior call should raise a clear, explicit error when that state is missing rather than falling back to a stale or sentinel default, converting a silent wrong-execution into a loud, catchable failure.
2. **Explicit precondition declarations checked before execution**: Have each tool declare the state it requires as input (not assumed context), and validate a generated plan against those declarations before execution, rejecting plans that reference undeclared or unestablished state.
3. **Session-scoped state isolation between tasks**: Reset or explicitly scope working state (like "most recently processed file") per logical task rather than letting it persist implicitly across unrelated tasks in the same session, removing the fallback value that made the omission dangerous rather than merely broken.
4. **Plan completeness checks against task decomposition**: Before executing a multi-step plan, verify every step's required inputs are either provided directly or produced by an earlier step in the same plan, flagging any step whose dependency isn't satisfied within the plan itself.
5. **Sensitive-default auditing**: Specifically audit tools with side effects (sending, sharing, external writes) for silent-fallback behavior on missing required arguments, since this is where a missing dependency has the highest cost if it silently succeeds against the wrong state.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| missing_dependency_error_rate | Rate of tool calls failing due to a required prior-call state not being present | Alert if > 1% |
| silent_fallback_invocation_count | Count of tool calls that proceeded using a default/fallback value instead of an explicitly required argument | Alert if > 0 for side-effecting tools |
| plan_precondition_validation_failure_rate | Fraction of generated plans rejected by pre-execution precondition validation | Track as leading indicator of planner completeness |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Side-effecting tool executed against fallback state | A tool with external side effects (send, share, write) runs using a silently-defaulted value instead of explicitly provided state | High | Page on-call, halt further automated actions from that session, notify affected parties if data exposure occurred |
| Elevated missing-dependency error rate | missing_dependency_error_rate exceeds threshold for a specific tool | Medium | Review the planner's handling of that tool's prerequisites, add explicit precondition declarations |

## Related Patterns
- [Tool Invocation Ordering Dependency](./tool-invocation-ordering-dependency.md) - the closely related failure where the prerequisite call is made but in the wrong order, rather than omitted entirely
- [Tool Mutation State Leak](./tool-mutation-state-leak.md) - the inverse failure, where leftover state from an unrelated call is incorrectly used instead of being correctly absent
- [Tool Idempotency Assumption Failure](./tool-idempotency-assumption-failure.md) - both involve incorrect assumptions about what state a prior call did or didn't establish

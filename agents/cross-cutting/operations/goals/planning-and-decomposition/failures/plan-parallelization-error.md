# Plan Parallelization Error

## Issue
A planner, in an effort to reduce total execution time, marks two or more subtasks as safe to run in parallel because they don't appear to reference each other's stated inputs or outputs. In reality, the subtasks share a hidden data or resource dependency — one writes to a location the other reads from, both mutate the same underlying state, or one's precondition is silently established by the other's side effect — and the planner's dependency analysis wasn't deep enough to catch it. The plan itself contains no cycle and looks well-formed; the error is a misclassification made at planning time, before execution, that only manifests as a race condition once the two branches actually run concurrently.

**Frequency**: Occasional

**Symptoms**
- Two subtasks scheduled in parallel intermittently produce different final results depending on which one happens to finish first
- A subtask that reads a resource sometimes sees the pre-update and sometimes the post-update version of data being concurrently written by a "parallel" sibling subtask
- Task success rate for a specific parallel branch pair is lower than either subtask's success rate when run sequentially or in isolation
- Post-incident analysis finds no explicit dependency edge was declared between two subtasks that turn out to share an implicit data or resource dependency
- Re-running the exact same plan against the exact same input produces non-deterministic final state, despite the plan itself being static and identical each time

## Root Cause
Parallelization decisions at planning time are typically made by inspecting each subtask's declared inputs and outputs and concluding two subtasks are independent if neither declares a dependency on the other's declared output. This analysis is only as good as the completeness of what's declared: a subtask that reads or writes to a resource through a side channel not captured in its formal input/output spec (a shared file, a database row referenced by an ID computed at runtime, a cache both branches happen to populate) has a real dependency the planner's static analysis cannot see. Because the planner reasons about task descriptions rather than actual runtime data flow, and because natural-language or loosely-typed task specifications rarely enumerate every resource a step touches, the classification of "independent, therefore parallelizable" is a best-effort inference rather than a verified guarantee — and it fails precisely in the cases where the hidden dependency wasn't obvious enough to describe explicitly when the subtasks were defined.

## Example
```
A document-processing agent decomposes "update the customer record
with the new address and regenerate the welcome letter" into two
subtasks it schedules in parallel, since neither subtask's declared
inputs reference the other's declared outputs: (1) update the
customer's address field in the CRM, (2) generate a welcome letter
using the customer's current profile data.

The planner didn't capture that "generate welcome letter" reads the
customer's address field as part of assembling the letter body - the
subtask's declared input was "customer profile," not the specific
address field, so the dependency was invisible to the planner's
input/output matching.

When the two subtasks race, the letter-generation subtask sometimes
reads the address before the update commits and sometimes after,
depending on execution timing. About half of affected customers
receive a welcome letter addressed to their old address despite the
CRM correctly showing the new one, because the plan's parallelization
decision assumed independence that didn't actually hold.
```

## Statistics
| Finding | Context |
|---|---|
| Subtask pairs marked parallelizable based on declared I/O alone show a non-trivial rate of hidden shared-resource dependencies that only surface under concurrent execution | Typical range observed in production planning systems using static input/output declarations |
| Parallelization-related race conditions are disproportionately concentrated in subtasks that share an underlying data store or resource ID computed at runtime, rather than subtasks operating on fully disjoint inputs | Estimated from incident review of multi-branch agent plans |
| Adding runtime resource-conflict detection (rather than relying solely on planning-time declared I/O) substantially reduces parallelization-related race conditions in comparable systems | Typical improvement range reported after introducing runtime lock/conflict checks |

## Mitigations
1. **Runtime resource-conflict detection, not just planning-time I/O matching**: Track actual resources (database rows, files, cache keys) touched during execution and detect conflicts between concurrently running subtasks, rather than trusting the planner's static independence inference alone.
2. **Conservative parallelization for subtasks sharing an entity**: Treat any two subtasks that operate on the same underlying entity (same customer record, same order, same document) as dependent by default, requiring an explicit proof of independence rather than an absence of a declared conflict.
3. **Explicit resource declarations beyond task-level I/O**: Require subtask definitions to declare the specific resources they read/write (not just a high-level "input"/"output" label), so the planner's dependency analysis has enough granularity to catch shared-resource cases like a single field within a larger record.
4. **Serialize-then-measure fallback**: When independence is uncertain, default to sequential execution and only promote a subtask pair to parallel execution after empirically validating, across repeated runs, that results are consistent regardless of execution order.
5. **Post-execution consistency checks on parallel branches**: For subtasks executed in parallel, add a validation step that checks final state consistency (e.g., the letter was generated using the post-update address), catching violations even when the planning-time dependency analysis missed them.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| parallel_branch_result_variance | Rate at which re-running the same plan with parallel branches produces different final state across runs | Alert if > 0% for any plan involving a shared entity across branches |
| declared_vs_actual_resource_overlap | Difference between resources declared in subtask I/O specs and resources actually touched at runtime, measured via execution tracing | Alert when actual resource overlap is detected between subtasks marked independent |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Race condition detected between parallel subtasks | Runtime tracing detects two concurrently executing subtasks accessing the same resource, at least one as a write | High | Halt the affected plan, fall back to sequential execution, patch the dependency declaration |
| Non-deterministic plan outcome | Identical plan and input produce differing final state across repeated executions | High | Quarantine the plan template pending manual dependency audit |

## Related Patterns
- [Plan Dependency Cycle](./plan-dependency-cycle.md) - a related planning-time dependency error, but one that produces a structurally unexecutable cycle rather than a false independence classification
- [Subgoal Ordering Error](./subgoal-ordering-error.md) - a related failure where sequential (not parallel) subgoals are ordered incorrectly due to an unrecognized implicit precedence constraint
- [Parallel Execution Failures](../../multi-agent-coordination/failures/parallel-execution-failures.md) - the runtime-coordination counterpart, where parallel work is correctly identified but poorly coordinated during execution, as opposed to being incorrectly identified as parallel in the first place
- [Tool Invocation Ordering Dependency](../../tool-selection-sequencing/failures/tool-invocation-ordering-dependency.md) - a related but narrower failure at the individual tool-call level rather than the subtask-decomposition level

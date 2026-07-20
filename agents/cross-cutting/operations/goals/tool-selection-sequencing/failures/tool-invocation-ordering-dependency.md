# Tool Invocation Ordering Dependency

## Issue
Two or more tools must be called in a specific order for the task to succeed — one establishes a precondition, allocates a resource, or authenticates a session that a later tool depends on — but nothing in the tool definitions or the agent's planning logic enforces that order. The agent, reasoning about which tool seems most relevant to the current sub-goal, calls them out of sequence, and the later call either fails outright or, worse, succeeds against stale or wrong preconditions.

**Frequency**: Common

**Symptoms**
- A tool call fails with an error referencing a resource, token, or state that a different tool call was supposed to have created first
- The same multi-tool task succeeds when tools happen to be called in one order and fails silently or loudly when called in another
- Task success rate is sensitive to how the agent's prompt happens to list or describe the tools, since ordering isn't enforced structurally
- Error messages from the failing tool point at a missing precondition ("no active session," "resource not found") rather than a problem with the failing tool's own arguments
- Manually re-running the same task with an explicit ordering hint in the prompt fixes the failure without any code change

## Root Cause
Tool definitions are typically presented to the agent as a flat, independent list — each with its own name, description, and parameters — with no first-class way to express "tool B requires tool A to have run first." The agent infers ordering, if at all, from the natural-language task description and its own world knowledge about typical workflows, which works for common patterns (authenticate before fetching data) but breaks for domain-specific or less obvious dependencies (a "lock_resource" tool that must precede "update_resource," where the tool descriptions alone don't make the dependency clear). Because the dependency lives only in the tool author's head or in documentation the agent doesn't see, the planner has no structural signal to prevent calling the dependent tool first.

## Example
```
A deployment agent has three tools available: create_environment,
provision_database, and deploy_application. provision_database
requires an environment_id that only exists after create_environment
has successfully run; deploy_application requires a database
connection string that only exists after provision_database
completes.

Given the task "deploy the new service to staging," the agent's
planner - reasoning primarily from the word "deploy" in the task and
the tool named deploy_application - calls deploy_application first,
since its description ("deploys an application to a target
environment") looks like the most directly relevant tool for the
stated goal.

deploy_application is called with environment="staging" but no
database connection string (none was ever generated). The tool's
underlying API falls back to a cached connection string from a
previous, now-decommissioned staging environment, and deploys
successfully - against the wrong database. The deployment "succeeds"
with no error, and the misconfiguration surfaces only when the newly
deployed service starts silently writing data to the old, decommissioned
staging database, corrupting data continuity across two environments.
```

## Statistics
| Finding | Context |
|---------|---------|
| 15-30% of multi-tool task failures in workflows with implicit setup/dependency steps trace to an ordering violation rather than a single tool's misuse | Typical range observed in production agent telemetry |
| Ordering violations that fail loudly (explicit precondition errors) are caught in an estimated 70-90% of cases; the remainder silently proceed against stale defaults | Estimated from postmortem review of multi-tool workflows |
| Encoding explicit dependency graphs between tools reduces ordering-violation incidents by an estimated 60-85% | Reported range across teams that added structural dependency declarations |

## Mitigations
1. **Explicit tool dependency graphs**: Define machine-readable prerequisite relationships between tools (tool B declares it requires tool A's output) and have the orchestration layer enforce or at least warn on out-of-order calls, rather than relying on the planner to infer them.
2. **Precondition checks inside tools**: Have dependent tools validate their required inputs exist and are fresh (not silently falling back to a cached/default value) before proceeding, converting a silent wrong-execution into a loud, catchable error.
3. **Composite/wrapper tools for fixed sequences**: For sequences that must always run in a specific order, expose a single composite tool that internally calls the sub-steps in the correct order, removing the ordering decision from the agent's planning step entirely.
4. **Explicit sequencing in task decomposition**: Require the planning step to produce an ordered step list with declared inputs/outputs per step before tool selection, so ordering is reasoned about as a first-class part of planning rather than inferred implicitly per call.
5. **Dependency-aware plan validation**: Before executing a multi-step tool plan, run a validation pass that checks each step's declared required inputs are produced by an earlier step in the plan, rejecting or reordering plans that violate this.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| ordering_violation_error_rate | Rate of tool calls failing with a precondition/missing-dependency error | Alert if > 1% |
| stale_default_fallback_count | Count of tool calls that silently proceeded using a cached/default value instead of a required upstream output | Alert if > 0 |
| plan_reorder_rate | Fraction of generated plans that required reordering by a validation pass before execution | Track as leading indicator of planner ordering weakness |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Tool executed against missing precondition | A dependent tool runs and silently falls back to stale/default state instead of its required upstream output | High | Page on-call, halt dependent downstream actions, audit for data written against the wrong precondition |
| Repeated ordering-violation failures for the same tool pair | ordering_violation_error_rate for a specific tool pair exceeds threshold | Medium | Add an explicit dependency declaration or composite wrapper tool for that pair |

## Related Patterns
- [Tool State Dependency Violation](./tool-state-dependency-violation.md) - the closely related failure where the prerequisite call was believed to have happened but actually didn't
- [Tool Composition Complexity Explosion](./tool-composition-complexity-explosion.md) - ordering constraints are one of the factors that compound the combinatorial planning cost described there
- [Tool Mutation State Leak](./tool-mutation-state-leak.md) - out-of-order calls can also leave mutation side effects that leak into later, unrelated calls

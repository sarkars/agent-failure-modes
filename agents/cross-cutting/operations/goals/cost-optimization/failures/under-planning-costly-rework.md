# Under-Planning Costly Rework

## Issue: Agent Skips Upfront Planning on a Task That Genuinely Needed It, Causing Failed Attempts and Expensive Rework

**Frequency**: Common

**Symptoms**
- Agent jumps directly to execution on multi-step or ambiguous tasks with no upfront consideration of dependencies, ordering, or failure modes
- A task requires 2-3 corrective retries or full restarts after an initial direct-execution attempt fails partway through
- Root-cause review of failed executions shows the failure was foreseeable from information already available before the first action was taken
- Total token cost of the failed-attempt-plus-redo cycle exceeds what a short upfront planning call would have cost

**Root Cause**
In an effort to avoid the token/latency cost of unnecessary planning on simple tasks, some agent architectures default to direct execution unless a task is obviously complex. This under-corrects: tasks that look simple on the surface but have a hidden dependency, ordering constraint, or irreversible-action risk get executed without the brief upfront check that would have caught the issue, and the resulting failure requires a costly redo — often more expensive than the planning step that was skipped, because the redo has to first undo or work around the partial failure before retrying.

**Example**
```
Task: "Migrate customer C-40021's data to the new billing system and
       cancel their old-system subscription."

Direct-execution attempt (no upfront planning):
Step 1: Cancel old-system subscription for C-40021. [Executed immediately]
Step 2: Attempt to migrate data to new system.
Step 3: Migration fails - new-system account for C-40021 doesn't exist yet
         and must be created first, which requires the old subscription's
         billing history as input.

Result: Old subscription is already cancelled, its billing history is
        no longer accessible via the standard lookup, and a manual data
        recovery step is now required before the migration can even
        start. The single skipped planning step turns a straightforward
        two-tool sequence into a multi-hour manual remediation.

Cost comparison:
  Upfront planning call to check for ordering dependency: ~300 tokens
  Failed execution + manual remediation + corrected re-execution: ~15x
  the tokens of the planning call, plus the manual labor cost outside
  the token budget entirely.
```

**Contributing Factors**
- Complexity classifiers that gate planning calls are tuned to minimize false positives (unnecessary planning) without equally weighing false negatives (skipped planning that was needed)
- No dependency/ordering check runs before an irreversible or hard-to-reverse action (cancellation, deletion, migration) even in a direct-execution path
- Task descriptions that read as simple ("migrate and cancel") can hide an implicit ordering requirement not visible from the surface-level request text
- No tracking of "planning was skipped and the task subsequently failed," so the true cost of under-planning stays invisible relative to the visible cost of over-planning

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent uses a direct-execution path by default for tasks not classified as obviously complex
- Task set includes at least one operation with a real, non-obvious ordering/dependency constraint (e.g., cancelling a subscription before migrating data that depends on it)
- No pre-execution dependency check exists on the direct-execution path

### Trigger Mechanism
1. Submit a task with a hidden ordering dependency, phrased simply enough to be classified as "direct execution" by the complexity gate
2. Let the agent execute steps in the order implied by the request's surface phrasing
3. Observe whether the ordering dependency causes a mid-execution failure, and measure the token/time cost of the resulting redo versus a hypothetical upfront planning check

**Example Reproduction Steps:**
```
1. Configure a task: "Migrate customer C-40021's data to the new billing
   system and cancel their old-system subscription," where migration
   actually requires reading old-subscription billing history first
2. Submit the task to the agent's default (no-upfront-planning) path
3. Log the execution order the agent chooses and whether it cancels
   before confirming migration prerequisites are met
4. If the ordering causes a failure, record the total tokens and steps
   needed to detect the failure, attempt recovery, and complete a
   corrected re-execution
5. Separately, run the same task through a path with a brief upfront
   dependency-check planning call, and compare total cost end-to-end
6. Compute the cost ratio between the under-planned-and-recovered path
   and the planned path
```

### Expected Failure State
- The direct-execution path cancels the old subscription before confirming the new-system account and data dependencies are satisfied, matching the ordering failure in the example
- Total tokens (failed execution + detection + manual/automated recovery + corrected re-execution) substantially exceed the cost of a short upfront planning call that would have surfaced the dependency
- No pre-execution check exists for ordering dependencies on irreversible actions in the direct-execution path
- The failure was foreseeable: the dependency (migration needs old billing history) was available information before step 1 executed

---

## Mitigation Strategies

### Prevention
1. **Mandatory dependency check before irreversible actions, even on the direct-execution path**: Regardless of whether full planning runs, require a lightweight check specifically for hard-to-reverse actions (cancellation, deletion, migration, financial transfer) that verifies prerequisite steps aren't being skipped or ordered incorrectly, addressing the exact failure in the example without requiring full upfront planning for every task. Trade-off: this check itself costs some tokens on every direct-execution task, though far less than a full planning call, and much less than a failed-execution recovery.
2. **Complexity classifier tuned for asymmetric risk, not just token minimization**: Since the root cause is a classifier optimized to avoid unnecessary planning without weighing the cost of skipped-necessary planning, incorporate an explicit "does this task include any irreversible or hard-to-reverse action" signal into the classifier, routing such tasks to at least a minimal planning check regardless of apparent surface simplicity. Trade-off: this raises the planning rate somewhat, trading some of the cost savings from [Unnecessary Planning Step](./unnecessary-planning-step.md) mitigations for reduced rework risk.
3. **Reversibility-first execution ordering**: When a task involves both reversible and irreversible steps, default to attempting reversible/verifiable steps first (confirm migration prerequisites are met) before executing irreversible ones (cancel the old subscription), so a hidden ordering problem surfaces during a cheap, undoable step rather than after a costly one. Trade-off: requires the agent (or its harness) to classify individual steps by reversibility, which may not always be available from tool metadata.

### Detection & Response
1. **Skipped-planning-then-failed correlation tracking**: Log which tasks were routed to direct execution (planning skipped) and subsequently required a corrective retry or manual remediation; a task type showing a pattern of this correlation is a candidate for tightening the complexity classifier for that type specifically.
2. **Rework-cost-versus-planning-cost comparison**: For any task that fails and requires redo after a direct-execution attempt, compute the total redo cost and compare it against what an upfront planning call for that task type would have cost; a consistent pattern of redo cost exceeding hypothetical planning cost justifies moving that task type to mandatory planning.
3. **Ordering-dependency post-mortems**: When a mid-execution failure is traced to a missed ordering/dependency issue, treat it as a distinct incident category (not generic tool failure) and track its recurrence rate, since it specifically indicates under-planning rather than an unrelated tool or data problem.

### Architecture Patterns
1. **Tiered pre-execution check**: Insert a minimal, fast dependency/ordering check (far cheaper than full planning) between the complexity classifier and direct execution, specifically scanning for known-risky action types (cancel, delete, migrate, transfer) and their common prerequisite patterns, rather than an all-or-nothing planning-versus-no-planning decision. Deployment consideration: the check's rule set needs to be maintained as new risky action types are added to the agent's tool surface.
2. **Dry-run/simulation pass for irreversible-action tasks**: For tasks containing at least one irreversible action, run a simulated/dry-run pass through the intended step sequence (without executing side effects) to surface ordering problems before any real action fires, catching the exact failure in the example without committing to full planning-call overhead for every task. Deployment consideration: requires tools to support a dry-run or preview mode, which not all APIs offer.
3. **Automatic rollback-then-retry on detected ordering failure**: When an ordering dependency failure is detected mid-execution, attempt an automated rollback of the already-executed irreversible step (if a compensating action exists) before re-planning and retrying, reducing the manual-remediation tail of the cost rather than only addressing prevention. Deployment consideration: requires every risky action to have a defined compensating/rollback action, which isn't always possible (e.g., a sent notification can't be recalled).

### Metrics
1. **direct_execution_failure_requiring_redo_rate**: Target < 3% of direct-execution tasks require a corrective retry or manual remediation; Alert if > 10%.
2. **redo_cost_to_hypothetical_planning_cost_ratio**: Target < 3x; Alert if > 10x (matching the ~15x ratio in the example as the failure ceiling).
3. **irreversible_action_without_dependency_check_rate**: Target 0% of tasks execute an irreversible action without a prerequisite check; Alert if > 0%.
4. **ordering_dependency_incident_rate**: Target < 1% of multi-step tasks; Alert if > 5% for a given task type.

### Alerts
1. **Irreversible-Action-Ordering-Failure** (P1): Condition - a task executes an irreversible action (cancel/delete/migrate/transfer) and subsequently fails due to a missed prerequisite. Action: attempt automated rollback/compensation if available, escalate to human review, and add the task type to the mandatory-dependency-check list.
2. **Redo-Cost-Exceeds-Planning-Cost** (P2): Condition - redo_cost_to_hypothetical_planning_cost_ratio exceeds 10x for a task type over a rolling week. Action: move that task type from direct-execution to mandatory (even minimal) upfront planning.

## References

- [Implementing Prompt Compression to Reduce Agentic Loop Costs](https://machinelearningmastery.com/implementing-prompt-compression-to-reduce-agentic-loop-costs/) - broader framing of planning-cost trade-offs, including cases where skipping planning costs more than it saves
- [Related Pattern: Unnecessary Planning Step](./unnecessary-planning-step.md) - the inverse failure, where planning runs when it isn't needed; both patterns are resolved by the same underlying need for an accurate, risk-aware complexity classifier rather than a token-minimization-only one

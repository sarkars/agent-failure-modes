# Sequencing Errors

## Issue: Agent Calls Tools in Wrong Order

**Frequency**: Common

**Symptoms**
- Dependent tool called before prerequisite
- Data fetched after it's needed
- Transactions started but not committed
- Cleanup runs before operation completes

**Root Cause**
- Agent doesn't understand tool dependencies
- Async operations confuse ordering
- Agent optimizes for speed over correctness
- Missing dependency documentation

**Example**
```
Task: Create user and send welcome email

Agent sequence:
1. send_welcome_email(user_id: ???)  # User doesn't exist yet!
2. create_user(name: "Alice")

Result: Email fails, user created without notification
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Two tools with an implicit dependency (`send_welcome_email` needs a `user_id` that only `create_user` produces) documented only externally, not in the tool description
- No return-value chaining or plan-before-execute step enforced
- No prerequisite-violation check inside `send_welcome_email`

### Trigger Mechanism
1. Give the agent a compound task requiring both tools in a specific order
2. Observe the actual order of tool invocations the agent chooses
3. Check whether the dependent tool is called before its prerequisite exists

**Example Reproduction Steps:**
```
1. Ask the agent: "Create a user named Alice and send her a welcome email"
2. Capture the full sequence of tool calls the agent issues
3. Check whether send_welcome_email is called with a valid, real user_id from create_user's output, or a placeholder/missing value
4. If called out of order, check the agent's final response to the user for whether it discloses the email failure
5. Measure: % of trials where the agent sequences the calls incorrectly
```

### Expected Failure State
- `send_welcome_email` is invoked before `create_user`, with a missing or invalid `user_id`
- The email tool call fails, but the user is created regardless
- Agent's final response does not clearly disclose that the welcome email failed

---

## Mitigation Strategies

### Prevention
1. **Force dependency satisfaction through required-parameter chaining**: Make `send_welcome_email` require a `user_id` that can only come from `create_user`'s return value, so the exact ordering bug in the example — calling `send_welcome_email(user_id: ???)` before the user exists — becomes a hard validation failure ("user_id required") instead of a silent no-op with a placeholder value. Trade-off: tightly coupling tool signatures to expected call order reduces flexibility for legitimately independent operations that happen to share a parameter name.
2. **Document prerequisites directly in the tool description, not just in external docs**: State explicitly in `send_welcome_email`'s docstring "Requires an existing user_id — call create_user first if the user doesn't exist yet," since the root cause is that the agent "doesn't understand tool dependencies" and the LLM only sees the tool description at call-planning time, not separate documentation. Trade-off: descriptions grow longer and must be kept in sync as dependencies change.
3. **Require an explicit plan-before-execute step for multi-tool tasks**: Have the agent output an ordered plan ("1. create_user, 2. send_welcome_email using the returned user_id") before executing any calls, catching the reversed ordering in review/validation before either tool actually runs. Trade-off: adds a planning round-trip that's unnecessary overhead for simple, single-tool tasks.

### Detection & Response
1. **Prerequisite-violation logging at the tool layer**: Have `send_welcome_email` (and similarly dependent tools) explicitly check whether its `user_id` argument refers to a real, existing record and log a structured "prerequisite not met" event rather than merely failing — this distinguishes ordering bugs from unrelated invalid-input errors.
2. **Planned-vs-actual sequence comparison**: Where a planning step is used, diff the agent's stated plan against the tools it actually invoked in practice; a mismatch (plan said create_user first, execution called send_welcome_email first) is a direct signal of a sequencing regression, potentially from a prompt change.
3. **Cross-tool failure-rate correlation**: Track failure rate of `send_welcome_email` specifically in sessions where it's the first tool called in the transcript vs. sessions where `create_user` precedes it — a much higher failure rate in the "called first" cohort confirms the sequencing dependency is being violated in production.

### Architecture Patterns
1. **Saga/orchestration pattern for multi-step workflows**: Model "create user then send welcome email" as an explicit saga with defined steps and compensating actions (e.g., if email fails, don't roll back user creation, but do retry the email step), rather than leaving ordering to ad hoc agent tool selection; deployment consideration — sagas add orchestration-layer complexity and are overkill for workflows with only two loosely-coupled steps.
2. **Single composite tool for tightly-coupled sequences**: Where two operations are almost always performed together in a fixed order (create_user → send_welcome_email), expose a single `create_user_with_welcome_email` tool that enforces the correct internal ordering, removing the sequencing decision from the agent entirely; deployment consideration — reduces flexibility for callers who legitimately want to create a user without immediately emailing them.
3. **Return-value chaining as the only valid input path**: Design the tool schema so the only way to obtain a valid `user_id` for `send_welcome_email` is from `create_user`'s output (e.g., an opaque token rather than a guessable ID format), making out-of-order calls structurally impossible rather than merely discouraged; deployment consideration — opaque/unguessable IDs complicate debugging and manual testing.

### Metrics
1. **prerequisite_violation_rate**: Target < 1% of dependent-tool calls; Alert if > 5% over a 24-hour window for any tool pair with a known dependency.
2. **plan_execution_mismatch_rate**: Target < 3% of planned sequences deviating from actual execution order; Alert if > 10%.
3. **first-call-failure-rate for dependent tools**: Target: failure rate for a dependent tool called first in a session should not exceed 2x its failure rate when called after its prerequisite; Alert if the ratio exceeds 5x.

### Alerts
1. **Prerequisite Violation Spike** (P2): Condition - prerequisite_violation_rate for a known dependent tool pair exceeds 5% over 24 hours. Action: review recent prompt or tool-description changes for that pair, strengthen the dependency documentation or add return-value chaining.
2. **Plan/Execution Divergence** (P2): Condition - plan_execution_mismatch_rate exceeds 10%. Action: audit transcripts for the specific divergence pattern, check whether a recent prompt change weakened the planning step's influence on execution.
3. **Silent User-Facing Sequencing Failure** (P1): Condition - a dependent tool call fails due to a missing prerequisite (e.g., email fails because user_id doesn't exist) but the agent's response to the user implies success. Action: page immediately — this directly mirrors the example's "email fails, user created without notification" outcome and is a trust-breaking bug.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on task ordering and sequencing failures
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Analysis of multi-agent coordination failures

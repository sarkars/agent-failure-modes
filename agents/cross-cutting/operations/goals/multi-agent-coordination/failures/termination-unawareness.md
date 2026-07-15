# Termination Condition Unawareness

## Issue: Agent Doesn't Know When to Stop

**Frequency**: Common (12.4% of MAS failures)

**Symptoms**
- Agent continues working after task is complete
- Agent stops prematurely before completion
- No clear signal that task is finished
- Conflicting signals about completion status

**Root Cause**
Agent is unaware of termination conditions - it doesn't recognize when the task is complete, either continuing unnecessarily or stopping before the job is done. This is especially problematic in multi-agent systems where termination requires coordination.

**Example**
```
Multi-agent system: Code review pipeline

Task: "Review and approve the PR if it passes all checks"

Agent trace:
Reviewer Agent: "Code looks good, tests pass. Approved."
CI Agent: "All checks passed."
Merger Agent: "Ready to merge."

[Task is complete - but no agent terminates]

Reviewer Agent: "Let me check the code again..."
CI Agent: "Running tests again..."
Merger Agent: "Checking merge status..."

Result: System continues running indefinitely
        Task was complete but agents didn't stop
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Termination unawareness accounts for 12.4% of failures
- Part of "System Design Issues" category (44.2% total)
- Often leads to resource exhaustion

**Termination Failures**
- **Over-execution**: Continuing after task complete
- **Under-execution**: Stopping before task complete
- **Ambiguous state**: Unclear if task is done
- **Coordination failure**: Agents disagree on completion

**Contributing Factors**
- Vague success criteria in task definition
- No explicit termination signals
- Completion conditions buried in long prompts
- Multi-agent consensus required but not achieved
- State not clearly indicating "done"

## Mitigation Strategies

### Prevention
1. **Explicit, machine-checkable termination criteria per agent**: In the code review example, all three agents (Reviewer, CI, Merger) individually reached a completion state ("Approved," "checks passed," "ready to merge") but none of them recognized that the *combination* constituted done, so they each kept re-checking. Define the terminal condition as an explicit conjunction of each agent's completion signal (reviewer_approved AND ci_passed AND merge_ready) checked by a coordinator, not left to each agent to infer independently. Trade-off: an explicit conjunction can be brittle if one agent's signal format changes or a new required check is added without updating the termination logic.
2. **Dedicated termination signal distinct from status narration**: The agents' outputs ("Code looks good... Approved," "All checks passed") read like completion statements but were never wired to an actual stop mechanism — they were just narrated status, not machine-actionable termination events. Require agents to emit a structured, dedicated "DONE" event (separate from free-text status commentary) that a supervising process listens for and uses to halt further activity, rather than parsing prose for completion intent. Trade-off: requires retrofitting agents that currently only produce narrative output with a structured signal channel.
3. **Idle-recheck suppression after first completion signal**: After the trio reports success, the example shows each agent going back to "Let me check the code again..." / "Running tests again..." / "Checking merge status..." — a redundant re-verification loop with no new information. Once an agent's own success criteria are met once, suppress that agent's re-invocation for the same task unless new input arrives (e.g., a new commit), rather than letting it loop on "checking" indefinitely. Trade-off: suppressing re-checks risks missing a legitimate state change (e.g., a late-arriving failing test) if the suppression window is too aggressive.

### Detection & Response
1. **Repeated-checking-behavior detector**: The specific failure signature here is agents re-running the same verification action ("check the code again," "running tests again") after having already reported success. Pattern-match consecutive agent actions against their own prior "success" statement, and flag any agent that re-performs an already-passed check without new input as exhibiting termination unawareness.
2. **All-signals-green-but-no-stop monitor**: Since the underlying bug is that reviewer/CI/merger all independently signaled done but the system kept running, track the conjunction of individual completion signals against actual system halt — if all three go green and activity continues past that point, that gap itself is the alertable condition.
3. **Resource-usage-without-progress correlation**: The example's system "continues running indefinitely" post-completion, meaning compute is spent with the task state static. Correlate token/compute spend against task-state deltas; flat state with rising spend after a completion signal was already emitted is a strong termination-unawareness signal specific to this file's failure.

### Architecture Patterns
1. **Consensus/quorum-based termination protocol for multi-agent completion**: Rather than each of Reviewer, CI, and Merger deciding independently whether to keep going, require a quorum check — the task is only "done" (and all agents halted) when a designated coordinator confirms all three specific signals are present, mirroring how consensus-deadlock's tie-break logic works but for completion rather than voting. Deployment consideration: the coordinator itself must have a hard timeout, or it becomes the new point of indefinite waiting.
2. **Heartbeat-plus-completion-event supervisor**: Give each agent (Reviewer, CI, Merger) a heartbeat that reports "still working" vs. "done, no further action needed," monitored by a lightweight supervisor that terminates the pipeline the instant all three report "done" rather than relying on the agents to self-regulate their own re-invocation. Deployment consideration: adds a supervisor process that must be kept in sync with however many agents participate in a given pipeline.
3. **Timeout fallback bounded by expected pipeline duration**: As a backstop for cases where the consensus/heartbeat mechanism itself fails to catch the all-green state, force termination after a duration well beyond the pipeline's typical completion time (e.g., 3x median review-CI-merge cycle time) so a stuck "checking again" loop cannot run indefinitely even if the primary termination signal is missed. Deployment consideration: the timeout must be tuned per pipeline type or it either fires too early (killing legitimately slow runs) or too late (allowing significant resource waste, as noted in the 12.4%-of-failures statistic).

### Metrics
1. **post_completion_activity_duration**: Target 0 seconds of agent activity after all completion signals are present; Alert if any agent acts more than 10 seconds past the all-green point.
2. **redundant_recheck_rate**: Target < 2% of completed tasks show a repeated verification action after success was already reported; Alert if > 8%.
3. **termination_signal_conjunction_latency**: Target < 5 seconds between the last individual agent's completion signal and system-wide halt; Alert if > 30 seconds.
4. **timeout_fallback_trigger_rate**: Target < 1% of pipelines relying on the timeout fallback rather than the primary termination signal; Alert if > 5%, indicating the primary consensus/heartbeat mechanism is unreliable.

### Alerts
1. **All Signals Green, No Halt** (P1): Condition - all required per-agent completion signals (reviewer_approved, ci_passed, merge_ready) are present but the pipeline has not terminated within the expected latency window. Action: force immediate termination via the coordinator and log the gap for root-cause analysis of why the conjunction check didn't fire.
2. **Redundant Re-check Loop** (P2): Condition - an agent re-performs a verification action it already reported as passed, with no new input since that report. Action: suppress further invocation of that agent for the current task and surface the loop for review.
3. **Timeout Fallback Fired** (P2): Condition - the hard timeout terminates a pipeline instead of the primary completion signal. Action: page the on-call owner of that pipeline to investigate why the consensus/heartbeat termination mechanism failed to fire in time.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.5: Unaware of Termination Conditions (12.4%)
- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion from over-execution
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination termination issues

# Reasoning-Action Mismatch

## Issue: Agent's Reasoning Doesn't Match Its Actions

**Frequency**: Common (13.2% of MAS failures)

**Symptoms**
- Agent explains one plan but executes another
- Stated intentions don't match tool calls
- Reasoning is correct but actions are wrong
- Logical analysis followed by illogical action

**Root Cause**
Agent exhibits a mismatch between its reasoning and its actions. The agent may reason correctly about what should be done, but then execute different actions. This disconnect between "thinking" and "doing" is a fundamental failure in agent execution.

**Example**
```
Task: "Delete the oldest backup file to free space"

Agent reasoning:
"I need to find the oldest backup file. Let me list files
by date. The files are:
- backup_2024_01.tar (oldest)
- backup_2024_06.tar
- backup_2024_12.tar (newest)
The oldest file is backup_2024_01.tar, so I should delete that."

Agent action:
delete_file("backup_2024_12.tar")

Result: Newest backup deleted instead of oldest
        Reasoning was correct, action was wrong
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Reasoning-action mismatch accounts for 13.2% of failures
- Part of "Inter-Agent Misalignment" category
- One of the most common failure modes

**Mismatch Patterns**
- **Parameter swap**: Right function, wrong parameters
- **Target confusion**: Correct analysis, wrong target
- **Inverted logic**: Reasoning correct, action opposite
- **Partial execution**: Plan complete, execution partial

**Contributing Factors**
- Disconnect between language generation and tool calling
- Copy-paste errors in parameter extraction
- Context confusion during action formulation
- Model limitations in grounding reasoning to actions
- Long reasoning chains losing thread

## Mitigation Strategies

### Prevention
1. **Reasoning-to-parameter binding**: Require the final action's parameters to be mechanically extracted from the explicitly stated conclusion in the reasoning (e.g., bind the delete argument directly to the file identified as "oldest" in the reasoning trace: `backup_2024_01.tar`) rather than letting the model independently regenerate the parameter at the action-call step, which is where the swap to `backup_2024_12.tar` occurred. Trade-off: requires structured reasoning output the binding step can parse reliably, which adds prompt/format constraints.
2. **Pre-execution action-intent diff**: Before executing, automatically diff the target named in the reasoning conclusion against the target in the actual tool call and block execution on any mismatch, directly catching the "target confusion" pattern from the example. Trade-off: adds a verification pass to every tool call, with associated latency cost.
3. **Structured output forcing explicit parameter extraction**: Force the model to emit its conclusion as a structured field (e.g., `{"target_file": "backup_2024_01.tar"}`) immediately after reasoning, rather than free-text reasoning followed by a separately-generated tool call, reducing the chance of "copy-paste errors in parameter extraction" named as a contributing factor. Trade-off: constrains the model's reasoning format, which can reduce reasoning quality for genuinely complex judgment calls.

### Detection & Response
1. **Stated-intent-vs-executed-action comparison**: For every action, programmatically compare the entity/parameter named in the immediately preceding reasoning text against what was actually passed to the tool call, flagging any divergence (this alone would have caught the backup-file mismatch).
2. **User "I said X but you did Y" correction tracking**: Specifically tag and count user corrections that describe a mismatch between stated intent and executed action, distinguishing this from other error types like wrong reasoning entirely.
3. **Irreversible-action extra scrutiny**: Apply heightened verification specifically to irreversible actions like file deletion, since a reasoning-action mismatch on a delete operation (as in the example) is unrecoverable, unlike a mismatch on a read-only action.

### Architecture Patterns
1. **Pre-execution review step**: Surface the planned action (target, parameters) alongside the reasoning conclusion for confirmation — human or automated — before execution, specifically for destructive operations, catching cases like deleting the wrong backup before it happens. Deployment consideration: adds a checkpoint that must be fast enough not to break agentic flow for routine actions.
2. **Consistency-check middleware**: Insert a lightweight verification layer between reasoning generation and tool execution that re-derives the expected action from the reasoning text and compares it to the actual call, similar to a chain-of-verification pass. Deployment consideration: the verifier itself must be reliable or it introduces new failure surface.
3. **Action-verification confirmation loop**: After generating a tool call, have the model explicitly restate "this action targets X because Y" and check that Y matches the earlier reasoning's conclusion, catching inverted-logic and parameter-swap patterns before the call fires. Deployment consideration: adds token overhead per action; most valuable when reserved for higher-stakes tool calls.

### Metrics
1. **reasoning_action_consistency_rate**: Target: > 99% of executed actions match the conclusion stated in immediately preceding reasoning; Alert if < 97% over rolling 200 actions.
2. **irreversible_action_mismatch_rate**: Target: 0 reasoning-action mismatches on irreversible actions (delete, send, purchase); Alert on any single confirmed incident.
3. **parameter_swap_incident_rate**: Target: < 1% of multi-candidate actions (choosing among several named entities) show a parameter swap; Alert if > 3% over rolling 100 actions.
4. **pre_execution_block_rate**: Target: pre-execution diff checks block < 2% of actions (indicates mismatches are rare, not that the checker is mis-calibrated); Alert if > 8%, which suggests either a systemic mismatch problem or checker miscalibration.

### Alerts
1. **Irreversible Action Mismatch Blocked** (P1): Condition - pre-execution diff detects a mismatch between reasoning conclusion and action target on a destructive/irreversible operation. Action: block execution immediately, surface both the reasoning and the attempted action to a human for resolution, and log for pattern analysis.
2. **Consistency Rate Degradation** (P2): Condition - reasoning_action_consistency_rate drops below 97% over a rolling 200-action window. Action: review recent mismatches for a common pattern (parameter swap vs. target confusion vs. inverted logic) and adjust the binding/extraction mechanism accordingly.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 2.6: Reasoning-Action Mismatch (13.2%)
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Execution vs planning failures
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - Grounding failures

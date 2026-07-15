# Goal Drift

## Issue: Agent Loses Focus on Original Objective

**Frequency**: Common

**Symptoms**
- Agent pursues tangential subtasks
- Original goal forgotten mid-execution
- Final output doesn't match request
- Agent goes down rabbit holes

**Root Cause**
- Interesting subtasks distract from main goal
- Long task chains lose sight of objective
- Agent optimizes for immediate step, not end goal
- No explicit goal tracking mechanism

**Example**
```
Original goal: "Write a function to parse CSV files"

Agent actions:
1. Researches CSV parsing approaches ✓
2. Discovers edge case in UTF-8 encoding
3. Deep dives into Unicode standards
4. Researches international character sets
5. Writes essay on history of text encoding
6. ...never writes the CSV parser

Result: Hours spent, original task incomplete
```

## Mitigation Strategies

### Prevention
1. **Explicit goal state persisted across steps**: Maintain the original objective ("write a function to parse CSV files") as a persistent, re-readable state object rather than relying on it staying in context, so a long tangent like the UTF-8/Unicode deep-dive doesn't cause the goal itself to fall out of the agent's working context. Trade-off: adds bookkeeping overhead for genuinely short, single-step tasks.
2. **Subtask depth/time limits**: Cap how many levels deep a tangential investigation (e.g., "edge case in UTF-8" leading to "Unicode standards" leading to "essay on text encoding history") can go before forcing a return to the main task. Trade-off: an overly aggressive cap can cut off genuinely necessary investigation of a real edge case.
3. **Goal-relevance gate before each new subtask**: Before starting any new subtask, require an explicit check of whether it's necessary to complete the stated goal, rejecting subtasks like "researches international character sets" that don't serve "write a CSV parser." Trade-off: the relevance check itself can be gamed by an agent rationalizing tangents as necessary.

### Detection & Response
1. **Action-to-goal relevance scoring**: Continuously score each action's relevance to the stated goal and flag sustained drops (as would occur once the agent moved from CSV parsing to encoding history) rather than waiting for task completion to notice.
2. **Time-without-progress alerting**: Track elapsed time/steps since the last artifact directly matching the goal's deliverable (e.g., no CSV-parsing code written) and alert once it exceeds a threshold.
3. **Final-output-vs-original-request diff**: At task end, explicitly diff the delivered output against the original request; a mismatch (essay delivered instead of function) is a clear post-hoc drift signal to feed back into prevention tuning.

### Architecture Patterns
1. **Goal restatement checkpoints**: Periodically re-inject the original objective verbatim into the agent's context at fixed intervals (e.g., every N tool calls) so a multi-step tangent can't silently displace it — directly addresses the "no explicit goal tracking mechanism" root cause. Deployment consideration: too-frequent restatement wastes tokens on long-running tasks.
2. **Time-boxed subtask execution**: Wrap each subtask (e.g., "research edge case") in a hard time/step budget; when exceeded, force a decision point to either conclude the subtask or abandon it and return to the main goal. Deployment consideration: budgets need to be calibrated per task type or legitimate deep investigations get cut short.
3. **Progress checkpoint verification**: Require the agent to periodically state concretely what progress it has made toward the deliverable (not just what it has learned), which would have surfaced that zero lines of the CSV parser existed after the Unicode detour. Deployment consideration: needs a clear, checkable definition of "progress" per task type.

### Metrics
1. **goal_relevance_score**: Target: > 90% of actions score as directly relevant to stated goal; Alert if < 70% sustained over 5 consecutive actions.
2. **task_completion_rate_within_budget**: Target: > 95% of tasks produce the requested deliverable within the allotted step/time budget; Alert if < 80% over rolling 50 tasks.
3. **tangent_depth**: Target: max 2 levels of sub-investigation before forced goal-relevance check; Alert on any chain exceeding 4 levels.
4. **deliverable_match_rate**: Target: > 98% of final outputs match the original request's deliverable type; Alert on any mismatch (e.g., prose delivered instead of code).

### Alerts
1. **Zero Progress Timeout** (P1): Condition - no goal-relevant artifact produced within the task's time/step budget (e.g., no parser code after extended research). Action: terminate the current subtask chain, restate the original goal, and force the agent to produce a minimal viable deliverable first.
2. **Deliverable Mismatch** (P2): Condition - final output type doesn't match the requested deliverable type. Action: reject the output, restate the goal, and re-run with tangent limits tightened.

## References
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Goal adherence failures
- [Medium: Why AI Agents Keep Failing](https://medium.com/data-science-collective/why-ai-agents-keep-failing-in-production-cdd335b22219) - Goal drift patterns

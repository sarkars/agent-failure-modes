# Step Repetition

## Issue: Agent Repeats Same Steps Without Progress

**Frequency**: Common (15.7% of MAS failures)

**Symptoms**
- Same tool calls executed multiple times
- Identical reasoning patterns repeated
- No progress despite continued activity
- Output loops without variation

**Root Cause**
Agent repeats the same steps without making progress toward task completion. Unlike infinite loops which may involve retry logic, step repetition involves the agent genuinely re-executing identical steps as if it hasn't done them before.

**Example**
```
Task: "Find and summarize the Q3 sales report"

Agent trace:
Turn 1: search_files("Q3 sales report") → Found: report.pdf
Turn 2: read_file("report.pdf") → [contents]
Turn 3: search_files("Q3 sales report") → Found: report.pdf  [REPEAT]
Turn 4: read_file("report.pdf") → [contents]                 [REPEAT]
Turn 5: search_files("Q3 sales report") → Found: report.pdf  [REPEAT]
Turn 6: read_file("report.pdf") → [contents]                 [REPEAT]
...

Result: Agent never proceeds to summarization
        Burns tokens repeating discovery steps
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Step repetition accounts for 15.7% of failures
- One of the most common failure modes
- Part of "System Design Issues" category
- Major contributor to resource exhaustion

**Repetition Patterns**
- **Discovery loops**: Repeatedly finding same information
- **Verification loops**: Re-checking already confirmed facts
- **Setup loops**: Re-initializing already configured state
- **Query loops**: Re-asking same questions

**Contributing Factors**
- Agent loses track of completed steps
- No memory of previous actions
- Context window doesn't include recent actions
- Lack of progress tracking mechanism
- Missing state management

## Mitigation Strategies

### Prevention
1. **Visible action history injected into context**: The example shows the agent re-running `search_files("Q3 sales report")` and `read_file("report.pdf")` three times as if it "hasn't done them before" — maintain an explicit, always-visible log of completed tool calls and their results in the agent's working context so it can check "have I already done this?" before issuing a duplicate call. Trade-off: the history log itself consumes context tokens, which must be weighed against the far larger cost of repeated discovery loops.
2. **Idempotency check before re-executing a step**: Before calling a tool, check whether an identical call (same tool + same parameters) already succeeded earlier in the task, and if so, reuse the cached result instead of re-invoking, directly targeting the "Discovery loops" and "Verification loops" patterns named in the file. Trade-off: requires reliable call-signature matching (tool name + normalized parameters), which can miss near-duplicate calls with slightly different parameter formatting.
3. **State/progress summarization at intervals**: Since the root cause includes "context window doesn't include recent actions" causing the agent to lose track, periodically inject a compact progress summary ("found report.pdf, read contents, next step: summarize") into context so the completed-steps state survives even if raw history gets truncated. Trade-off: summarization adds a periodic processing step and risks compressing away details needed later.

### Detection & Response
1. **Identical-call detection in short sequence**: Since step repetition is defined as "genuinely re-executing identical steps," flag any tool call with the same name and parameters as one issued within the last N turns — the example's alternating search_files/read_file repeats 3x would trip this immediately.
2. **Progress-state stagnation despite token spend**: Track a task-progress indicator (e.g., stage reached: discovery → read → summarize) against ongoing token usage; per the MAST finding that this is a "major contributor to resource exhaustion," flat progress state combined with rising token spend is the core signature to alert on.
3. **Repetition-rate baseline per task type**: Given step repetition accounts for 15.7% of MAS failures per the MAST study, track the rate of detected repeated-call incidents per task type and treat any task type trending above the historical baseline as needing investigation into its state-management/context design.

### Architecture Patterns
1. **Explicit action-history ledger**: A structured, append-only ledger of (tool, parameters, result, timestamp) maintained outside the raw conversation context and always summarized into the prompt, addressing "no memory of previous actions" and "lack of progress tracking mechanism" named as contributing factors. Deployment consideration: ledger must be kept compact (e.g., deduped/truncated) so it doesn't itself become a token-explosion source.
2. **Repetition-detecting middleware**: A tool-call interceptor that hashes each (tool, params) pair and compares against a per-task set of already-executed calls, short-circuiting with the cached result on a match rather than letting the call reach the underlying API — this operationalizes "Repetition detection" as enforced infrastructure rather than a prompt-level suggestion. Deployment consideration: needs a cache-invalidation policy for calls whose results can legitimately change (e.g., re-reading a file that may have been updated).
3. **Step-limit circuit breaker per action signature**: Cap the number of times any single (tool, parameters) combination can execute within one task (e.g., max 2), forcing an escalation or state-repair step once the cap is hit rather than looping indefinitely, directly bounding the discovery-loop pattern in the example. Deployment consideration: the cap must be tuned per tool — some legitimately need more than 2 calls (e.g., paginated reads).

### Metrics
1. **repeated_call_rate**: Target < 2% of tool calls within a task are exact repeats of an earlier call; Alert if > 15.7% (matching the MAST-reported failure prevalence as the ceiling to catch before it becomes systemic).
2. **turns_without_progress**: Target < 3 consecutive turns with no state-stage advancement; Alert if > 6 consecutive turns (as in the example's repeated search/read cycle).
3. **discovery_loop_incidence**: Target < 5% of tasks exhibiting a detected discovery-loop pattern (same search+read pair repeating); Alert if > 20% for a given task template.
4. **token_spend_per_completed_stage**: Target stable or declining as task progresses; Alert if token spend continues accruing with zero stage advancement for more than 5 turns.

### Alerts
1. **Repeated-Call-Detected** (P2): Condition - the same (tool, parameters) signature executes 3+ times within a single task. Action: halt further identical calls, inject the cached result and an explicit "already completed" state marker into context, and force the agent to proceed to the next stage.
2. **Progress-Stagnation** (P2): Condition - turns_without_progress exceeds 6 for an active task. Action: trigger a state-summary re-injection and, if stagnation persists after that, escalate to human review per the resource-exhaustion escalation path.
3. **Task-Template-Repetition-Rate-Elevated** (P3): Condition - a specific task template's repeated_call_rate trends above the 15.7% MAST baseline over a rolling week. Action: review that template's context/state-management design for missing action-history visibility.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.3: Step Repetition (15.7% of failures)
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Loop detection
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Cost impact of repetition

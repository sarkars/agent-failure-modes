# No Long-Horizon Evaluation

## Issue: Multi-step degradation is missed.

**Frequency**: Common

**Symptoms**
- Single-turn tests pass; workflow fails.
- Agent contradicts a fact it established earlier in the same session (forgets a stated constraint, repeats a step the user already confirmed as done) once a conversation runs past a handful of turns.
- Task completion rate for long sessions (10+ turns) is measurably lower than for short sessions, but the eval suite -- built entirely from single-turn or 2-3 turn cases -- never surfaces the gap.

**Root Cause**
The blind spot exists because eval suites are built almost entirely from short, isolated exchanges, so nothing in the test process ever runs a trajectory long enough to exercise compounding drift. The underlying architecture makes this worse by relying on unbounded context accumulation rather than explicit state checkpointing, letting facts and constraints silently fall out of effective attention as a conversation grows, and production monitoring rarely breaks out quality or completion rate by session length, so even after launch there's no visibility into the degradation. Long-horizon scenarios are also expensive and slow to construct relative to single-turn cases, so under release-schedule pressure they consistently lose out to cheaper, shorter test cases.

**Example**
```
A trip-planning agent walks a user through a 15-turn itinerary-building conversation:
picking a destination, dates, flights, then hotels. By turn 12, the agent recommends a
hotel in a city different from the one confirmed at turn 2 -- the original destination
context has drifted out of its effective attention as the conversation grew. Every
single-turn eval case passes because each was tested as an isolated 1-2 turn exchange;
none exercised a full 12+ turn trajectory, so this compounding drift was never caught
before launch.
```

**Contributing Factors**
- Eval suite is built entirely from short, isolated single-turn or few-turn exchanges, with no long-running trajectory scenarios.
- Agent architecture relies on unbounded context accumulation rather than explicit state checkpointing, so drift compounds silently as conversations lengthen.
- No production monitoring breaks out quality/completion rate by session length, so long-horizon degradation has no visibility even after launch.
- Long-horizon scenarios are expensive/slow to construct and run, so they get deprioritized in favor of cheaper single-turn test cases under release-schedule pressure.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| 12+ turn trajectory consistency | Full itinerary-building conversation from destination through hotel booking | Agent's turn-12 recommendation matches turn-2 confirmed destination | Agent contradicts an earlier-established fact later in the session |
| Long-session task completion | Simulated 15-turn multi-step workflow end-to-end | Task completes successfully at a rate comparable to short-session cases | Completion rate drops sharply as workflow length increases |
| State checkpoint recall | Ask the agent to restate a constraint established 10 turns earlier | Agent correctly recalls the constraint | Agent forgets, contradicts, or repeats an already-completed step |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| quality_degradation_slope_per_turn | ~0 (no significant downward trend) | Score each turn in a trajectory eval and regress quality against turn number |
| workflow_completion_rate_by_length_bucket_pct | < 10 point drop from short to long bucket | Bucket eval trajectories by turn count, compare completion rate across buckets |
| long_horizon_eval_coverage_count | >= 20 multi-turn scenarios in regression suite | Count trajectory-level scenarios (10+ turns) maintained in the eval suite |

---

## Mitigation Strategies

### Prevention
1. **Multi-Turn Trajectory Eval Suite**: Build eval cases that span full multi-step workflows (not single-turn Q&A), scoring both the final outcome and intermediate state consistency at each step, so compounding drift across turns is caught before shipping.
2. **Long-Horizon Regression Benchmarks**: Maintain a fixed set of long-running task scenarios (e.g., 10+ turn conversations, multi-day workflows with state persistence) re-run on every release to catch degradation that only appears after several steps.
3. **State Consistency Checkpointing in Design**: Require the agent architecture to explicitly checkpoint and validate critical state (task progress, accumulated facts, user intent) at defined intervals during long workflows, rather than relying on unbounded context accumulation that silently drifts.

### Detection & Response
1. **Turn-by-Turn Quality Degradation Tracking**: Score each turn in production multi-turn sessions and plot quality/accuracy against turn number; alert if there's a statistically significant downward trend as sessions lengthen.
2. **Workflow Completion Rate by Length Bucket**: Track task completion/success rate bucketed by workflow length (number of steps/turns); a completion rate that drops sharply past a certain length indicates long-horizon degradation invisible to single-turn evals.
3. **Context Drift Detection**: Monitor for signals of context drift in long sessions (contradicting earlier statements, forgetting established facts, repeating already-completed steps) via automated consistency checks against session history.

### Architecture Patterns
1. **Trajectory-Level Eval Harness**: Eval infrastructure runs full multi-step scenarios end-to-end (simulating user turns, tool calls, and state transitions) rather than isolated single-turn prompts, scoring trajectory-level success and per-step consistency.
2. **State Summarization and Checkpointing Layer**: The architecture periodically summarizes and re-anchors critical state into a compact, explicit representation (rather than raw growing context) to bound drift over long horizons, with each checkpoint eval-tested independently.
3. **Session Replay and Diff Tooling**: Tooling replays a full production session and diffs agent-stated facts/decisions turn-by-turn against ground truth or earlier turns, used both for debugging and to mine new long-horizon eval cases.

### Metrics
1. **quality_degradation_slope_per_turn**: Target: ~0 (no significant downward trend); Alert threshold: statistically significant negative slope
2. **workflow_completion_rate_by_length_bucket_pct**: Target: < 10 point drop from short to long bucket; Alert threshold: > 25 point drop
3. **context_drift_incident_rate_pct**: Target: < 2% of long sessions; Alert threshold: > 8%
4. **long_horizon_eval_coverage_count**: Target: >= 20 multi-turn scenarios in regression suite; Alert threshold: < 10

### Alerts
1. **Long-Horizon Completion Rate Collapse** (P1 - Critical): Condition - workflow completion rate for the long-length bucket drops more than 25 points below the short-length bucket. Action: Block release, run the trajectory-level eval suite to isolate the failing step range.
2. **Context Drift Spike** (P2 - Warning): Condition - context drift incident rate exceeds 8% of long sessions in a monitoring window. Action: Review state-summarization logic, add drift cases to the long-horizon eval suite.
3. **Quality Degradation Trend Detected** (P2 - Warning): Condition - turn-by-turn quality shows a statistically significant downward slope in production sampling. Action: Investigate context window management, prioritize long-horizon regression fix.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| workflow_completion_rate_by_length_bucket_pct | > 25 point drop long vs. short bucket |
| context_drift_incident_rate_pct | > 8% of long sessions |
| quality_degradation_slope_per_turn | Statistically significant negative slope |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Long-Horizon Completion Rate Collapse | Workflow completion rate for the long-length bucket drops more than 25 points below the short-length bucket | High |
| Context Drift Spike | Context drift incident rate exceeds 8% of long sessions in a monitoring window | Medium |
| Quality Degradation Trend Detected | Turn-by-turn quality shows a statistically significant downward slope in production sampling | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
